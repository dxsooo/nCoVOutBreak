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
    "东莞市": "dongguan"
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

def main_handler(event,content):
    if "requestContext" not in event.keys():
        return {"errorCode":410,"errorMsg":"event is not come from api gateway"}

    list_page = requests.get(root_url)
    latest_url = parse_list_html(list_page.text)

    content_page = requests.get(latest_url)
    all_data = parse_content_html(content_page.text)

    province, city = utils.parse_path(event["requestContext"]["path"])
    if province is None:
        return {"errorCode":411,"errorMsg":"request is not from setting api path"}

    if city is not None:
        # get the city only
        # if city not in list
        # return {"errorCode":412,"errorMsg":"article is not found"}
        pass
    return utils.serialize(all_data)