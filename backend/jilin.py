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
    "长春市": "changchun",
    "吉林市": "jilin",
    "四平市": "siping",
    "通化市": "tonghua",
    "白城市": "baicheng",
    "辽源市": "liaoyuan",
    "松原市": "songyuan",
    "白山市": "baishan",
    "延边朝鲜族自治州": "yanbian",
}

alia_cities = {
    "延边州": "延边朝鲜族自治州",
    "公主岭市": "四平市",
    "梅河口市": "通化市"
}

base_url = "http://www.jl.gov.cn/"
root_url = base_url + "szfzt/jlzxd/yqtb/"
provinceKey = "jilin"
provinceName = "吉林"
api_prefix = "/api/v1/provinces/" + provinceKey


def parse_list_html(raw):
    pattern = re.compile(r"<li>(.*?)<\/li>")
    pattern_title = re.compile(r".*肺炎疫情情况通报.*")

    p = ArticleParser()
    for m in pattern.finditer(raw):
        p.feed(m.groups()[0])
    p.close()

    latest_url = ""
    for res in p.get_articles():
        if pattern_title.match(res["title"]) is not None:
            latest_url = root_url + res["href"][2:]
            break
    return latest_url


def parse_content_html(raw):
    pattern = re.compile(r"<p>(.*?累计.*?)<\/p>")
    m = pattern.search(raw)
    content = m.groups()[0]

    province = ProvinceData(provinceName, provinceKey)
    pattern_confirm = re.compile(r"确诊病例(\d+)例")
    cm = pattern_confirm.search(content)
    if cm is not None:
        province.Confirmed = int(cm.groups()[0])
    pattern_heal = re.compile(r"治愈出院(\d+)例")
    hm = pattern_heal.search(content)
    if hm is not None:
        province.Healed = int(hm.groups()[0])
    pattern_dead = re.compile(r"死亡(\d+)例（([\u4E00-\u9FA5]+)）")
    dm = pattern_dead.search(content)
    dc = {}
    if dm is not None:
        province.Dead = int(dm.groups()[0])
        dc[dm.groups()[1]] = int(dm.groups()[0])  # SPECIAL HANDLE

    city = {}
    pattern_data = re.compile(r"[（，、。]([\u4E00-\u9FA5]+)(\d+)例")
    for i in pattern_data.finditer(content):
        name = utils.remove_preposition(i.groups()[0])
        if name in alia_cities.keys():
            name = alia_cities[name]
        if name in cities.keys():
            id = cities[name]
            if id not in city.keys():
                d = CityData(name, id)
                d.Confirmed = int(i.groups()[1])
                city[id] = d
            else:
                city[id].Confirmed += int(i.groups()[1])
    # SPECIAL HANDLE
    for dd in dc.items():
        if dd[0] in cities.keys():
            id = cities[dd[0]]
            if id not in city.keys():
                d = CityData(dd[0], id)
                d.Confirmed = dd[1]
                city[id] = d
            else:
                city[id].Confirmed += dd[1]
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
