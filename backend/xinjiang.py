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
    "乌鲁木齐市": "wulumuqi",
    "克拉玛依市": "kelamayi",
    "吐鲁番市": "tulufan",
    "哈密市": "hami",

    "阿克苏地区": "akesu",
    "喀什地区": "kashi",
    "和田地区": "hetian",
    "塔城地区": "tacheng",
    "阿勒泰地区": "aletai",

    "博尔塔拉蒙古自治州": "",
    "克孜勒苏柯尔克孜自治州": "",
    "伊犁哈萨克自治州": "yili",
    "昌吉回族自治州": "changji",
    "巴音郭楞蒙古自治州": "bazhou",

    "石河子市": "shihezi",
    "阿拉尔市": "alaer",
    "图木舒克市": "tumushuke",
    "五家渠市": "wujiaqu",
    "北屯市": "beitun",
    "铁门关市": "tiemenguan",
    "双河市": "shuanghe",
    "可克达拉市": "kekedala",
    "昆玉市": "kunyu",
    "胡杨河市": "huyanghe",
}

alia_cities = {
    "伊犁州": "伊犁哈萨克自治州",
    "昌吉州": "昌吉回族自治州",
    "巴州": "巴音郭楞蒙古自治州",
}

base_url = "http://www.xjhfpc.gov.cn"
root_url = base_url + "/ztzl/fkxxgzbdfygz/yqtb.htm"
provinceKey = "xinjiang"
provinceName = "新疆"
api_prefix = "/api/v1/provinces/" + provinceKey


def parse_list_html(raw):
    pattern = re.compile(r"(?s)<tr id=\"line17117_1\" height=\"20\">(.*?)<\/tr>")
    pattern_title = re.compile(r".*肺炎疫情.*")

    p = ArticleParser()
    for m in pattern.finditer(raw):
        p.feed(m.groups()[0])
    p.close()

    latest_url = ""
    for res in p.get_articles():
        if pattern_title.match(res["title"]) is not None:
            latest_url = base_url + res["href"][5:]
            break
    return latest_url


def parse_content_html(raw):
    pattern = re.compile(r"(?s)<div id=\"vsb_content_1029\">(.*)<\/div>")
    m = pattern.search(raw)
    content = m.groups()[0]

    province = ProvinceData(provinceName, provinceKey)
    pattern_confirm = re.compile(r"累计报告.*?确诊病例(\d+)例")
    cm = pattern_confirm.search(content)
    if cm is not None:
        province.Confirmed = int(cm.groups()[0])
    pattern_heal = re.compile(r"累计治愈出院病例(\d+)例")
    hm = pattern_heal.search(content)
    if hm is not None:
        province.Healed = int(hm.groups()[0])
    pattern_dead = re.compile(r"累计死亡病例(\d+)例")
    dm = pattern_dead.search(content)
    if dm is not None:
        province.Dead = int(dm.groups()[0])

    city = {}
    pattern_data = re.compile(r"[、]([\u4E00-\u9FA5]+)(\d+)例")
    for i in pattern_data.finditer(content[content.rfind("其中"):]):
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
