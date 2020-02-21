# -*- coding: utf-8 -*-

import unittest
import anhui
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/anhui_list_sample.html',encoding='utf-8') as f:
            res = anhui.parse_list_html(f.read())
            self.assertEqual(
                "http://wjw.ah.gov.cn/news_details_55203.html", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/anhui_content_sample.html',encoding='utf-8') as f:
            province, city = anhui.parse_content_html(f.read())
            self.assertEqual("安徽", province.ProvinceName)
            self.assertEqual(988, province.Confirmed)
            self.assertEqual(500, province.Healed)
            self.assertEqual("安庆市", city['anqing'].CityName)
            self.assertEqual(83, city['anqing'].Confirmed)


if __name__ == '__main__':
    unittest.main()
