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
    "和平区": "heping",
    "河东区": "hedong",
    "河西区": "hexi",
    "南开区": "nankai",
    "河北区": "hebei",
    "红桥区": "hongqiao",
    "滨海新区": "binhaixin",
    "东丽区": "dongli",
    "西青区": "xiqing",
    "津南区": "jinnan",
    "北辰区": "beichen",
    "武清区": "wuqing",
    "宝坻区": "baodi",
    "宁河区": "ninghe",
    "静海区": "jinghai",
    "蓟州区": "jizhou",
    "外地来津人员": "waidi"
}

root_url = "http://wsjk.tj.gov.cn/col/col87/index.html"
provinceKey = "tianjin"
provinceName = "天津"
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
    pattern = re.compile(r"<!--ZJEG_RSS.content.begin-->(.*)<!--ZJEG_RSS.content.end-->")
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
    for i in pattern_data.finditer(content[content.find("确诊病例中"):]):
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

    list_page = requests.get(root_url)
    latest_url = parse_list_html(list_page.content.decode())
    if len(latest_url) == 0:
        return utils.gen_response({"errorCode": 5001, "errorMsg": "failed to crawl data"})

    content_page = requests.get(latest_url)
    p, city_data = parse_content_html(content_page.content.decode())

    if event["requestContext"]["path"] == api_prefix + "/cities/{cityName}":
        city = event["pathParameters"]["cityName"]
        if city not in city_data.keys():
            return utils.gen_response({"errorCode":4003, "errorMsg":"not found"})
        return utils.gen_response(utils.serialize(city_data[city]))
    
    p.Cities = list(city_data.values())
    return utils.gen_response(utils.serialize(p))
