# -*- coding: utf-8 -*-

import sys
import logging
import json
import utils
from utils import ArticleParser, Data
import requests
import re
from html.parser import HTMLParser

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)

cities = {
    "石家庄市": "shijiazhuang",
    "唐山市": "tangshan",
    "秦皇岛市": "qinhuangdao",
    "邯郸市": "handan",
    "邢台市": "xingtai",
    "保定市": "baoding",
    "张家口市": "zhangjiakou",
    "承德市": "chengde",
    "沧州市": "cangzhou",
    "廊坊市": "langfang",
    "衡水市": "hengshui",
}

base_url = "http://hebwst.gov.cn/"
root_url = base_url + "index.do?templet=new_list&cid=14"
api_prefix = "/api/v1/provinces/hebei"


def parse_list_html(raw):
    pattern = re.compile(r"(?s)<td class='sy_new_list' height=32>(.*?)<\/td>")
    pattern_title = re.compile(r".*\d+年\d+月\d+日.*肺炎疫情.*")

    p = ArticleParser()
    for m in pattern.finditer(raw):
        p.feed(m.groups()[0])
    p.close()

    latest_url = ""
    for res in p.get_articles():
        if pattern_title.match(res["title"]) is not None:
            latest_url = base_url + res["href"]
            break
    return latest_url


def parse_content_html(raw):
    pattern = re.compile(r"(?s)<div class='con_wz'>(.*)</div>")
    pattern_data = re.compile(r"[，、]([\u4E00-\u9FA5]+)(\d+)例")

    m = pattern.search(raw)
    content = m.groups()[0]
    res = {}
    for i in pattern_data.finditer(content[content.rfind("确诊病例中"):]):
        if i.groups()[0] in cities.keys():
            name = i.groups()[0]
            id = cities[name]
            if id not in res.keys():
                d = Data(name, id)
                d.Confirmed = int(i.groups()[1])
                res[id] = d
    return res


def main_handler(event, content):
    if "requestContext" not in event.keys():
        return utils.gen_response({"errorCode": 4001, "errorMsg": "event is not come from api gateway"})
    if event["requestContext"]["path"] != api_prefix + "/cities/{cityName}" and event["requestContext"]["path"] != api_prefix:
        return utils.gen_response({"errorCode": 4002, "errorMsg": "request is not from setting api path"})

    list_page = requests.get(root_url)
    latest_url = parse_list_html(list_page.text)

    content_page = requests.get(latest_url)
    all_data = parse_content_html(content_page.text)

    if event["requestContext"]["path"] == api_prefix + "/cities/{cityName}":
        city = event["pathParameters"]["cityName"]
        if city not in all_data.keys():
            return utils.gen_response({"errorCode":4003, "errorMsg":"article is not found"})
        return utils.gen_response(utils.serialize(all_data[city]))
    return utils.gen_response(utils.serialize(list(all_data.values())))
