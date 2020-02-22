# -*- coding: utf-8 -*-

import unittest
import ningxia
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/testdata/ningxia_list_sample.html',
                  encoding='utf-8') as f:
            res = ningxia.parse_list_html(f.read())
            self.assertEqual("http://wsjkw.nx.gov.cn/info/1042/14661.htm", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/testdata/ningxia_content_sample.html',
                  encoding='utf-8') as f:
            province, city = ningxia.parse_content_html(f.read())
            self.assertEqual("宁夏", province.ProvinceName)
            self.assertEqual(71, province.Confirmed)
            self.assertEqual(48, province.Healed)
            self.assertEqual("银川市", city['yinchuan'].CityName)
            self.assertEqual(33, city['yinchuan'].Confirmed)


if __name__ == '__main__':
    unittest.main()
