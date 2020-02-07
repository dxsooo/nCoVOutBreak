# -*- coding: utf-8 -*-

import re
from html.parser import HTMLParser
import json


class ArticleParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.articles = []
        self.temp_article = None

    def handle_starttag(self, tag, attrs):
        article = {}
        for attr in attrs:
            article[attr[0]] = attr[1]
        if 'href' in article.keys():
            if 'title' in article.keys():
                self.articles.append(article)
            else:
                self.temp_article = article
    
    def handle_data(self, data):
        if self.temp_article is not None:
            article = self.temp_article
            article['title'] = data
            self.articles.append(article)
            self.temp_article = None

    def get_articles(self):
        return self.articles


class CityData:
    Confirmed = 0
    Healed = 0
    Dead = 0
    CityName = ""
    CityKey = ""

    def __init__(self, city_name, city_key):
        self.CityName = city_name
        self.CityKey = city_key


class ProvinceData:
    Confirmed = 0
    Healed = 0
    Dead = 0
    ProvinceName = ""
    ProvinceKey = ""
    Cities = []

    def __init__(self, province_name, province_key):
        self.ProvinceName = province_name
        self.ProvinceKey = province_key


def serialize(data):
    if isinstance(data, list):
        return [serialize(x) for x in data]
    if isinstance(data, CityData):
        return {
            "city": data.CityName,
            "id": data.CityKey,
            "confirmed": data.Confirmed,
            "healed": data.Healed,
            "dead": data.Dead,
        }
    if isinstance(data, ProvinceData):
        return {
            "province": data.ProvinceName,
            "id": data.ProvinceKey,
            "confirmed": data.Confirmed,
            "healed": data.Healed,
            "dead": data.Dead,
            "cities": serialize(data.Cities)
        }


def gen_response(body):
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, ensure_ascii=False)
    }


def remove_preposition(s):
    preposition_strs = ["其中"]
    res = s
    for prep in preposition_strs:
        if prep in s:
            res = s[s.find(prep)+len(prep):]
            break
    return res
