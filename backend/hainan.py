# -*- coding: utf-8 -*-

import sys
import logging
import utils
from utils import ArticleParser, CityData, ProvinceData
import requests
import re

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)

cities = {
    "海口市": "haikou",
    "三亚市": "sanya",
    "三沙市": "sansha",
    "儋州市": "danzhou",
    "五指山市": "wuzhishan",
    "文昌市": "wenchang",
    "琼海市": "qionghai",
    "万宁市": "wanning",
    "东方市": "dongfang",
    "定安县": "dingan",
    "屯昌县": "tunchang",
    "澄迈县": "chengmai",
    "临高县": "lingao",
    "白沙黎族自治县": "baisha",
    "昌江黎族自治县": "changjiang",
    "琼中黎族苗族自治县": "qiongzhong",
    "乐东黎族自治县": "ledong",
    "陵水黎族自治县": "lingshui",
    "保亭黎族苗族自治县": "baoting",
}

alia_cities = {
    "白沙县": "白沙黎族自治县",
    "昌江县": "昌江黎族自治县",
    "乐东县": "乐东黎族自治县",
    "琼中县": "琼中黎族苗族自治县",
    "陵水县": "陵水黎族自治县",
    "保亭县": "保亭黎族苗族自治县",
}

base_url = "http://wst.hainan.gov.cn/swjw/rdzt/yqfk/"
root_url = base_url + "index.html"
provinceKey = "hainan"
provinceName = "海南"
api_prefix = "/api/v1/provinces/" + provinceKey


def parse_list_html(raw):
    pattern = re.compile(r"<li >(.*?)<\/li>")
    pattern_title = re.compile(r".*肺炎疫情情况")

    p = ArticleParser()
    for m in pattern.finditer(raw):
        p.feed(m.groups()[0])
    p.close()

    latest_url = ""
    for res in p.get_articles():
        if pattern_title.match(res["title"]) is not None:
            latest_url = base_url + res["href"][2:]
            break
    return latest_url


def parse_content_html(raw):
    pattern = re.compile(r"<div>(.*)<\/div>")
    m = pattern.search(raw)
    content = m.groups()[0]

    province = ProvinceData(provinceName, provinceKey)
    pattern_confirm = re.compile(r"累计报告.*?确诊病例(\d+)例")
    cm = pattern_confirm.search(content)
    if cm is not None:
        province.Confirmed = int(cm.groups()[0])
    pattern_heal = re.compile(r"累计报告.*?出院病例(\d+)例")
    hm = pattern_heal.search(content)
    if hm is not None:
        province.Healed = int(hm.groups()[0])
    pattern_dead = re.compile(r"累计报告.*?死亡病例(\d+)例")
    dm = pattern_dead.search(content)
    if dm is not None:
        province.Dead = int(dm.groups()[0])

    city = {}
    pattern_data = re.compile(r"[，、]([\u4E00-\u9FA5]+)(\d+)例")
    for i in pattern_data.finditer(content[content.rfind("确诊病例中"):]):
        name = i.groups()[0]
        if name in alia_cities.keys():
            name = alia_cities[name]
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
    if event["requestContext"]["path"] != api_prefix + "/cities/{cityName}" and event["requestContext"][
        "path"] != api_prefix:
        return utils.gen_response({"errorCode": 4002, "errorMsg": "request is not from setting api path"})

    list_page = requests.get(root_url)
    latest_url = parse_list_html(list_page.content.decode())
    if len(latest_url) == 0:
        return utils.gen_response({"errorCode": 5001, "errorMsg": "failed to crawl data"})

    content_page = requests.get(latest_url)
    p, city_data = parse_content_html(content_page.content.decode())

    if event["requestContext"]["path"] == api_prefix + "/cities/{cityName}":
        city = event["pathParameters"]["cityName"]
        if city not in city_data.keys():
            return utils.gen_response({"errorCode": 4003, "errorMsg": "not found"})
        return utils.gen_response(utils.serialize(city_data[city]))

    p.Cities = list(city_data.values())
    return utils.gen_response(utils.serialize(p))
