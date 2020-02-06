# -*- coding: utf-8 -*-

import sys
import logging
import json
import utils
from utils import ArticleParser, CityData, ProvinceData
import urllib3
import re
from html.parser import HTMLParser

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)

cities = {
    "太原市": "taiyuan",
    "大同市": "datong",
    "朔州市": "shuozhou",
    "忻州市": "xinzhou",
    "阳泉市": "yangquan",
    "吕梁市": "lvliang",
    "晋中市": "jinzhong",
    "长治市": "changzhi",
    "晋城市": "jincheng",
    "临汾市": "linfen",
    "运城市": "yuncheng",
}

root_url = "http://wjw.shanxi.gov.cn/yqfbl05/index.hrh"
provinceKey = "shanxi"
provinceName = "山西"
api_prefix = "/api/v1/provinces/" + provinceKey


def parse_list_html(raw):
    pattern = re.compile(r"<li>(.*?)<\/li>")
    pattern_title = re.compile(r".*\d+年\d+月\d+日.*肺炎疫情.*")

    p = ArticleParser()
    for m in pattern.finditer(raw):
        p.feed(m.groups()[0])
    p.close()

    latest_url = ""
    for res in p.get_articles():
        if pattern_title.match(res["title"]) is not None:
            latest_url = res["href"]
            break
    return latest_url


def parse_content_html(raw):
    pattern = re.compile(r"(?s)<div class=\"ze-art\" style=\"width: 100%;\">(.*)<\/div>")
    m = pattern.search(raw)
    content = m.groups()[0]

    province = ProvinceData(provinceName, provinceKey)
    pattern_confirm = re.compile(r"累计.*?确诊.*?(\d+)例")
    cm = pattern_confirm.search(content)
    if cm is not None:
        province.Confirmed = int(cm.groups()[0])
    pattern_heal = re.compile(r"累计治愈出院(\d+)例")
    hm = pattern_heal.search(content)
    if hm is not None:
        province.Healed = int(hm.groups()[0])

    city = {}
    pattern_data = re.compile(r"([\u4E00-\u9FA5]+)(\d+)例")
    for i in pattern_data.finditer(content[content.rfind("累计报告"):content.rfind("累计治愈")]):
        name = utils.remove_preposition(i.groups()[0])
        if name in cities.keys():
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

    http = urllib3.PoolManager()
    list_page = http.request("get", root_url)
    latest_url = parse_list_html(list_page.data.decode())
    if len(latest_url) == 0:
        return utils.gen_response({"errorCode": 5001, "errorMsg": "failed to crawl data"})

    content_page = http.request("get", latest_url)
    p, city_data = parse_content_html(content_page.data.decode())

    if event["requestContext"]["path"] == api_prefix + "/cities/{cityName}":
        city = event["pathParameters"]["cityName"]
        if city not in city_data.keys():
            return utils.gen_response({"errorCode": 4003, "errorMsg": "not found"})
        return utils.gen_response(utils.serialize(city_data[city]))

    p.Cities = list(city_data.values())
    return utils.gen_response(utils.serialize(p))
