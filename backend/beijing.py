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
    "东城区": "dongcheng",
    "西城区": "xicheng",
    "朝阳区": "chaoyang",
    "丰台区": "fengtai",
    "石景山区": "shijingshan",
    "海淀区": "haidian",
    "顺义区": "shunyi",
    "通州区": "tongzhou",
    "大兴区": "daxing",
    "房山区": "fangshan",
    "门头沟区": "mentougou",
    "昌平区": "changping",
    "平谷区": "pinggu",
    "密云区": "miyun",
    "怀柔区": "huairou",
    "延庆区": "yanqing",
    "外地来京人员": "waidi"
}

root_url = "http://wjw.beijing.gov.cn/xwzx_20031/xwfb/"
provinceKey = "beijing"
provinceName = "北京"
api_prefix = "/api/v1/provinces/" + provinceKey


def parse_list_html(raw):
    pattern = re.compile(r"(?s)<div class=\"weinei_left_con_line_text\">(.*?)<\/div>")
    pattern_title = re.compile(r".*\d+月\d+日.*肺炎.*")

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
    pattern = re.compile(r"(?s)<!--content begin -->(.*)<!--content end -->")
    m = pattern.search(raw)
    content = m.groups()[0]

    province = ProvinceData(provinceName, provinceKey)
    pattern_confirm = re.compile(r"确诊病例(\d+)例")
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
    pattern_data = re.compile(r"[。，、]([\u4E00-\u9FA5]+)(\d+)例")
    for i in pattern_data.finditer(content[content.rfind("累计确诊"):]):
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
