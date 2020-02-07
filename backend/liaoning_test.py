# -*- coding: utf-8 -*-

import unittest
import liaoning
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/liaoning_list_sample.html',encoding='utf-8') as f:
            res = liaoning.parse_list_html(f.read())
            self.assertEqual(
                res, "http://wsjk.ln.gov.cn/wst_wsjskx/202002/t20200207_3736122.html")

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/liaoning_content_sample.html',encoding='utf-8') as f:
            province, city = liaoning.parse_content_html(f.read())
            self.assertEqual(province.ProvinceName, "辽宁")
            self.assertEqual(province.Confirmed, 95)
            self.assertEqual(province.Healed, 6)
            self.assertEqual(city['dalian'].CityName, "大连市")
            self.assertEqual(city['dalian'].Confirmed, 14)


if __name__ == '__main__':
    unittest.main()
