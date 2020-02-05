# -*- coding: utf-8 -*-

import unittest
import beijing
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/beijing_list_sample.html',encoding='utf-8') as f:
            res = beijing.parse_list_html(f.read())
            self.assertEqual(
                res, "http://wjw.beijing.gov.cn/xwzx_20031/xwfb/202002/t20200205_1625206.html")

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/beijing_content_sample.html',encoding='utf-8') as f:
            province, city = beijing.parse_content_html(f.read())
            self.assertEqual(province.ProvinceName, "北京")
            self.assertEqual(province.Confirmed, 253)
            self.assertEqual(province.Healed, 24)
            self.assertEqual(province.Dead, 1)
            self.assertEqual(city['dongcheng'].CityName, "东城区")
            self.assertEqual(city['dongcheng'].Confirmed, 6)


if __name__ == '__main__':
    unittest.main()
