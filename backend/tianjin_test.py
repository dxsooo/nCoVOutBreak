# -*- coding: utf-8 -*-

import unittest
import tianjin
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/tianjin_list_sample.html',encoding='utf-8') as f:
            res = tianjin.parse_list_html(f.read())
            self.assertEqual(
                res, "http://wsjk.tj.gov.cn/art/2020/2/19/art_87_71167.html")

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/tianjin_content_sample.html',encoding='utf-8') as f:
            province, city = tianjin.parse_content_html(f.read())
            self.assertEqual(province.ProvinceName, "天津")
            self.assertEqual(province.Confirmed, 128)
            self.assertEqual(province.Healed, 48)
            self.assertEqual(city['nankai'].CityName, "南开区")
            self.assertEqual(city['nankai'].Confirmed, 6)


if __name__ == '__main__':
    unittest.main()
