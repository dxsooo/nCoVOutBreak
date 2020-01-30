# -*- coding: utf-8 -*-

import re
from html.parser import HTMLParser
import json


class ArticleParser(HTMLParser):
    articles = []

    def handle_starttag(self, tag, attrs):
        article = {}
        for attr in attrs:
            article[attr[0]] = attr[1]
        if 'title' in article.keys() and 'href' in article.keys():
            self.articles.append(article)

    def get_articles(self):
        return self.articles


class Data:
    Confirmed = 0
    Healed = 0
    Dead = 0
    CityName = ""
    CityKey = ""

    def __init__(self, city_name, city_key):
        self.CityName = city_name
        self.CityKey = city_key


def serialize(data):
    if isinstance(data, list):
        return [serialize(x) for x in data]
    if isinstance(data, Data):
        return {
            "city": data.CityName,
            "id": data.CityKey,
            "confirmed": data.Confirmed,
            "healed": data.Healed,
            "dead": data.Dead,
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
