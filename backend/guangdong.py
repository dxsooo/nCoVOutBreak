# -*- coding: utf-8 -*-

import sys
import logging
import json
import utils
from utils import ArticleParser, Data
import requests
import re
from html.parser import HTMLParser

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)

cities = {
    "广州市": "guangzhou",
    "深圳市": "shenshen",
    "佛山市": "foshan",
    "东莞市": "dongguan",
    "中山市": "zhongshan",
    "珠海市": "zhuhai",
    "江门市": "jiangmeng",
    "肇庆市": "zhaoqin",
    "惠州市": "huizhou",
    "汕头市": "shantou",
    "潮州市": "chaozhou",
    "揭阳市": "jieyang",
    "汕尾市": "shanwei",
    "湛江市": "zhanjiang",
    "茂名市": "maoming",
    "阳江市": "yangjiang",
    "云浮市": "yunfu",
    "韶关市": "shaoguan",
    "清远市": "qingyuan",
    "梅州市": "meizhou",
    "河源市": "heyuan"
}

root_url = "http://wsjkw.gd.gov.cn/zwyw_yqxx/index.html"


def parse_list_html(raw):
    pattern = re.compile(r"<li>(.*?)<\/li>")
    pattern_1 = re.compile(r".*\d+年\d+月\d+日\d+时.*肺炎疫情.*")

    p = ArticleParser()
    for m in pattern.finditer(raw):
        p.feed(m.groups()[0])

    latest_url = ""
    for res in p.get_articles():
        if pattern_1.match(res["title"]) is not None:
            latest_url = res["href"]
            break
    return latest_url


def parse_content_html(raw):
    pattern = re.compile(r"(?s)<!--文章start-->(.*)<!--文章end-->")
    pattern_data = re.compile(r"[，、]([\u4E00-\u9FA5]+)(\d+)例")
    m = pattern.search(raw)
    content = m.groups()[0]
    res = []
    for i in pattern_data.finditer(content[content.rfind("确诊病例中"):]):
        if i.groups()[0] in cities.keys():
            name = i.groups()[0]
            d = Data(name, cities[name])
            d.Confirmed = int(i.groups()[1])
            res.append(d)
    return res


def main_handler(event, content):
    if "requestContext" not in event.keys():
        return utils.gen_response({"errorCode": 410, "errorMsg": "event is not come from api gateway"})

    list_page = requests.get(root_url)
    latest_url = parse_list_html(list_page.text)

    content_page = requests.get(latest_url)
    all_data = parse_content_html(content_page.text)

    province, city = utils.parse_path(event["requestContext"]["path"])
    if province is None:
        return utils.gen_response({"errorCode": 411, "errorMsg": "request is not from setting api path"})

    if city is not None:
        # get the city only
        # if city not in list
        # return {"errorCode":412,"errorMsg":"article is not found"}
        pass
    return utils.gen_response(utils.serialize(all_data))
