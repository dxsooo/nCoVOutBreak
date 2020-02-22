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
    "南宁市": "nanning",
    "柳州市": "liuzhou",
    "桂林市": "guilin",
    "梧州市": "wuzhou",
    "北海市": "beihai",
    "崇左市": "chongzuo",
    "来宾市": "laibin",
    "贺州市": "hezhou",
    "玉林市": "yulin",
    "百色市": "baise",
    "河池市": "hechi",
    "钦州市": "qinzhou",
    "防城港市": "fangchenggang",
    "贵港市": "guigang",
}


root_url = "http://wsjkw.gxzf.gov.cn/xxgks/yqxx/ssyqdt/"
provinceKey = "guangxi"
provinceName = "广西"
api_prefix = "/api/v1/provinces/" + provinceKey


def parse_list_html(raw):
    pattern = re.compile(r"(<li>(.*?)<\/li>)")
    pattern_title = re.compile(r".*肺炎疫情情况")

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
    pattern = re.compile(r"(?s)<div class=\"news_show_conter\">(.*)<\/div>")
    m = pattern.search(raw)
    content = m.groups()[0]

    province = ProvinceData(provinceName, provinceKey)
    pattern_confirm = re.compile(r"累计.*?确诊病例(\d+)例")
    cm = pattern_confirm.search(content)
    if cm is not None:
        province.Confirmed = int(cm.groups()[0])
    pattern_heal = re.compile(r"累计出院病例(\d+)例")
    hm = pattern_heal.search(content)
    if hm is not None:
        province.Healed = int(hm.groups()[0])
    pattern_dead = re.compile(r"累计死亡病例(\d+)例")
    dm = pattern_dead.search(content)
    if dm is not None:
        province.Dead = int(dm.groups()[0])

    city = {}
    pattern_data = re.compile(r"[、>]([\u4E00-\u9FA5]+)(\d+)例")
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

    http = urllib3.PoolManager()
    list_page = http.request("get", root_url)
    latest_url = parse_list_html(list_page.data.decode('gbk'))
    if len(latest_url) == 0:
        return utils.gen_response({"errorCode": 5001, "errorMsg": "failed to crawl data"})

    content_page = http.request("get", latest_url)
    p, city_data = parse_content_html(content_page.data.decode('gbk'))

    if event["requestContext"]["path"] == api_prefix + "/cities/{cityName}":
        city = event["pathParameters"]["cityName"]
        if city not in city_data.keys():
            return utils.gen_response({"errorCode": 4003, "errorMsg": "not found"})
        return utils.gen_response(utils.serialize(city_data[city]))

    p.Cities = list(city_data.values())
    return utils.gen_response(utils.serialize(p))
