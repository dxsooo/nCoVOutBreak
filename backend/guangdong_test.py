# -*- coding: utf-8 -*-

import unittest
import guangdong
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/guangdong_list_sample.html',encoding='utf-8') as f:
            res = guangdong.parse_list_html(f.read())
            self.assertEqual(
                res, "http://wsjkw.gd.gov.cn/zwyw_yqxx/content/post_2880263.html")

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/guangdong_content_sample.html',encoding='utf-8') as f:
            province, city = guangdong.parse_content_html(f.read())
            self.assertEqual(province.ProvinceName, "广东")
            self.assertEqual(province.Confirmed, 272)
            self.assertEqual(city['guangzhou'].CityName, "广州市")
            self.assertEqual(city['guangzhou'].Confirmed, 63)


if __name__ == '__main__':
    unittest.main()
