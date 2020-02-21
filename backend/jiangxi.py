# -*- coding: utf-8 -*-

import sys
import logging
import utils
from utils import ArticleParser, CityData, ProvinceData
import urllib3
import re

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)

cities = {
    "南昌市": "nanchang",
    "景德镇市": "jingdezhen",
    "萍乡市": "pingxiang",
    "九江市": "jiujiang",
    "新余市": "xinyu",
    "鹰潭市": "yingtan",
    "赣州市": "ganzhou",
    "吉安市": "jian",
    "宜春市": "yichun",
    "抚州市": "fuzhou",
    "上饶市": "shangrao",
}


base_url = "http://hc.jiangxi.gov.cn"
root_url = base_url + "/ztxx/xxgzbdgrdfyyqfk/yqtb/index.shtml"
provinceKey = "jiangxi"
provinceName = "江西"
api_prefix = "/api/v1/provinces/" + provinceKey


def parse_list_html(raw):
    pattern = re.compile(r"(?s)<li>(.*?)<\/li>")
    pattern_title = re.compile(r".*肺炎疫情情况")

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
    pattern = re.compile(r"(?s)<!--<\$\[CONTENT\]>start-->(.*)<\/div>")
    m = pattern.search(raw)
    content = m.groups()[0]

    province = ProvinceData(provinceName, provinceKey)
    pattern_confirm = re.compile(r"累计.*?确诊病例(\d+)例")
    cm = pattern_confirm.search(content)
    if cm is not None:
        province.Confirmed = int(cm.groups()[0])
    pattern_heal = re.compile(r"累计.*?出院病例(\d+)例")
    hm = pattern_heal.search(content)
    if hm is not None:
        province.Healed = int(hm.groups()[0])
    pattern_dead = re.compile(r"累计.*?死亡病例(\d+)例")
    dm = pattern_dead.search(content)
    if dm is not None:
        province.Dead = int(dm.groups()[0])

    city = {}
    pattern_data = re.compile(r"[，、]([\u4E00-\u9FA5]+)(\d+)例")
    for i in pattern_data.finditer(content[content.rfind("确诊病例中"):]):
        name = i.groups()[0]
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
