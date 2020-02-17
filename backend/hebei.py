# -*- coding: utf-8 -*-

import sys
import logging
import json
import utils
from utils import ArticleParser, CityData, ProvinceData
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

base_url = "http://wsjkw.hebei.gov.cn/"
root_url = base_url + "index.do?templet=new_list&cid=14"
provinceKey = "hebei"
provinceName = "河北"
api_prefix = "/api/v1/provinces/" + provinceKey


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
    m = pattern.search(raw)
    content = m.groups()[0]

    province = ProvinceData(provinceName, provinceKey)
    pattern_confirm = re.compile(r"累计报告确诊病例(\d+)例")
    cm = pattern_confirm.search(content)
    if cm is not None:
        province.Confirmed = int(cm.groups()[0])
    pattern_heal = re.compile(r"出院(\d+)例")
    hm = pattern_heal.search(content)
    if hm is not None:
        province.Healed = int(hm.groups()[0])
    pattern_dead = re.compile(r"死亡(\d+)例")
    dm = pattern_dead.search(content)
    if dm is not None:
        province.Dead = int(dm.groups()[0])

    city = {}
    pattern_data = re.compile(r"[，、]([\u4E00-\u9FA5]+)(\d+)例")
    for i in pattern_data.finditer(content[content.rfind("确诊病例中"):]):
        if i.groups()[0] in cities.keys():
            name = i.groups()[0]
            id = cities[name]
            if id not in city.keys():
                d = CityData(name, id)
                d.Confirmed = int(i.groups()[1])
                city[id] = d
    return province, city


def main_handler(event, content):
    if "requestContext" not in event.keys():
        return utils.gen_response({"errorCode": 4001, "errorMsg": "event is not come from api gateway"})
    if event["requestContext"]["path"] != api_prefix + "/cities/{cityName}" and event["requestContext"]["path"] != api_prefix:
        return utils.gen_response({"errorCode": 4002, "errorMsg": "request is not from setting api path"})

    list_page = requests.get(root_url)
    latest_url = parse_list_html(list_page.text)
    if len(latest_url) == 0:
        return utils.gen_response({"errorCode": 5001, "errorMsg": "failed to crawl data"})

    content_page = requests.get(latest_url)
    p, city_data = parse_content_html(content_page.text)

    if event["requestContext"]["path"] == api_prefix + "/cities/{cityName}":
        city = event["pathParameters"]["cityName"]
        if city not in city_data.keys():
            return utils.gen_response({"errorCode":4003, "errorMsg":"not found"})
        return utils.gen_response(utils.serialize(city_data[city]))
    
    p.Cities = list(city_data.values())
    return utils.gen_response(utils.serialize(p))