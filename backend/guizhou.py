# -*- coding: utf-8 -*-

import sys
import logging
import utils
from utils import CityData, ProvinceData
import urllib3
import re

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)

cities = {
    "贵阳市": "guiyang",
    "遵义市": "zunyi",
    "六盘水市": "liupanshui",
    "安顺市": "anshun",
    "毕节市": "bijie",
    "铜仁市": "tongren",
    "黔东南苗族侗族自治州": "qiandongnan",
    "黔南布依族苗族自治州": "qiannan",
    "黔西南布依族苗族自治州": "qianxinan",
}

alia_cities = {
    "黔东南州": "黔东南苗族侗族自治州",
    "黔南州": "黔南布依族苗族自治州",
    "黔西南州": "黔西南布依族苗族自治州",
}

root_url = "http://www.gzhfpc.gov.cn/xwzx_500663/zwyw/"
provinceKey = "guizhou"
provinceName = "贵州"
api_prefix = "/api/v1/provinces/" + provinceKey


def parse_list_html(raw):
    pattern = re.compile(r"(?s)<script type=\"text/javascript\">(.*?)<\/script><\/li>")
    pattern_title = re.compile(r".*\d+年\d+月\d+日.*肺炎疫情.*")

    p_1 = re.compile("var str_1 = \"(.*?)\";")
    p_3 = re.compile("var str_3 = \"(.*?)\";")

    latest_url = ""
    for m in pattern.finditer(raw):
        raw = m.groups()[0]
        mp_1 = p_1.search(raw)
        mp_3 = p_3.search(raw)
        if mp_1 is not None and mp_3 is not None:
            if pattern_title.match(mp_3.groups()[0]) is not None:
                latest_url = root_url + mp_1.groups()[0][2:]
                break

    return latest_url


def parse_content_html(raw):
    pattern = re.compile(r"<div class=\"view TRS_UEDITOR trs_paper_default trs_word trs_key4format\">(.*)<\/div>")
    m = pattern.search(raw)
    content = m.groups()[0]

    province = ProvinceData(provinceName, provinceKey)
    pattern_confirm = re.compile(r"累计.*?病例(\d+)例")
    cm = pattern_confirm.search(content)
    if cm is not None:
        province.Confirmed = int(cm.groups()[0])
    pattern_heal = re.compile(r"累计.*?出院(\d+)例")
    hm = pattern_heal.search(content)
    if hm is not None:
        province.Healed = int(hm.groups()[0])
    pattern_dead = re.compile(r"累计.*?死亡(\d+)例")
    dm = pattern_dead.search(content)
    if dm is not None:
        province.Dead = int(dm.groups()[0])

    city = {}
    pattern_data = re.compile(r"[，；]([\u4E00-\u9FA5]+)(\d+)例")
    for i in pattern_data.finditer(content):
        name = i.groups()[0]
        if name in alia_cities.keys():
            name = alia_cities[name]
        if name in cities.keys():
            id = cities[name]
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
