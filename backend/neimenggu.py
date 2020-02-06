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
    "呼和浩特市": "huhehaote",
    "包头市": "baotou",
    "乌海市": "wuhai",
    "赤峰市": "chifeng",
    "通辽市": "tongliao",
    "鄂尔多斯市": "eerduosi",
    "呼伦贝尔市": "hulunbeier",
    "巴彦淖尔市": "bayanzhuoer",
    "乌兰察布市": "wulanchabu",
    "兴安盟": "xingan",
    "锡林郭勒盟": "xilinguole",
    "阿拉善盟": "alashan",
}

base_url = "http://wjw.nmg.gov.cn"
root_url = base_url + "/xwzx/gzdt/index.shtml"
provinceKey = "neimenggu"
provinceName = "内蒙古"
api_prefix = "/api/v1/provinces/" + provinceKey


def parse_list_html(raw):
    pattern = re.compile(r"(?s)<li >(.*?)<\/li>")
    pattern_title = re.compile(r"内蒙古自治区新型冠状病毒感染的肺炎疫情情况")

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
    pattern = re.compile(r"(?s)<!------------------------- mian开始 ------------------------->(.*)<!--------责任编辑相关---------->")
    m = pattern.search(raw)
    content = m.groups()[0]

    province = ProvinceData(provinceName, provinceKey)
    pattern_confirm = re.compile(r"累计.*?确诊.*?(\d+)例")
    cm = pattern_confirm.search(content)
    if cm is not None:
        province.Confirmed = int(cm.groups()[0])
    pattern_heal = re.compile(r".*?(\d+)例已痊愈出院")
    for hm in pattern_heal.finditer(content):
        province.Healed += int(hm.groups()[0])

    city = {}
    pattern_data = re.compile(r">([\u4E00-\u9FA5]+)(\d+)例")
    for i in pattern_data.finditer(content[content.rfind("累计报告"):content.rfind("疑似病例")]):
        name = utils.remove_preposition(i.groups()[0])
        if '盟' in name[:-1]:
            name = name[:name.find('盟')+1]
        if '市' in name[:-1]:
            name = name[:name.find('市')+1]
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
