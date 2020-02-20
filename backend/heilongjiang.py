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
    "哈尔滨市": "haerbin",
    "齐齐哈尔市": "qiqihaer",
    "牡丹江市": "mudanjiang",
    "佳木斯市": "jiamusi",
    "大庆市": "daqing",
    "鸡西市": "jixi",
    "双鸭山市": "shuangyashan",
    "伊春市": "yichun",
    "七台河市": "qitaihe",
    "鹤岗市": "hegang",
    "绥化市": "suihua",
    "黑河市": "heihe",
    "大兴安岭地区": "daxinganling",
}


base_url = "http://wsjkw.hlj.gov.cn"
root_url = base_url + "/index.php/Home/Zwgk/all/typeid/42"
provinceKey = "heilongjiang"
provinceName = "黑龙江"
api_prefix = "/api/v1/provinces/" + provinceKey


def parse_list_html(raw):
    pattern = re.compile(r"<li>(.*?)<\/li>")
    pattern_title = re.compile(r"最新疫情通报...")

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
    pattern = re.compile(r"(?s)<div class=\"danye\">(.*?)<\/div>")
    m = pattern.search(raw)
    content = m.groups()[0]

    province = ProvinceData(provinceName, provinceKey)
    pattern_confirm = re.compile(r"确诊病例(\d+)例")
    cm = pattern_confirm.findall(content)
    if len(cm) > 0:
        province.Confirmed = max([int(x) for x in cm])
    pattern_heal = re.compile(r"出院病例(\d+)例")
    hm = pattern_heal.findall(content)
    if len(hm) > 0:
        province.Healed = max([int(x) for x in hm])
    pattern_dead = re.compile(r"死亡病例(\d+)例")
    dm = pattern_dead.findall(content)
    if len(dm) > 0:
        province.Dead = max([int(x) for x in dm])

    city = {}
    pattern_data = re.compile(r"[、：]([\u4E00-\u9FA5]+)(\d+)例")
    for i in pattern_data.finditer(content):
        name = i.groups()[0]
        print(name)
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
