# -*- coding: utf-8 -*-

import unittest
import shanxi
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/shanxi_list_sample.html',encoding='utf-8') as f:
            res = shanxi.parse_list_html(f.read())
            self.assertEqual(
                res, "http://wjw.shanxi.gov.cn:80/wjywl02/24724.hrh")

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/shanxi_content_sample.html',encoding='utf-8') as f:
            province, city = shanxi.parse_content_html(f.read())
            self.assertEqual(province.ProvinceName, "山西")
            self.assertEqual(province.Confirmed, 90)
            self.assertEqual(province.Healed, 6)
            self.assertEqual(city['jinzhong'].CityName, "晋中市")
            self.assertEqual(city['jinzhong'].Confirmed, 26)


if __name__ == '__main__':
    unittest.main()
