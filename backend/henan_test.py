# -*- coding: utf-8 -*-

import unittest
import henan
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/henan_list_sample.html',encoding='utf-8') as f:
            res = henan.parse_list_html(f.read())
            self.assertEqual(
                "http://www.hnwsjsw.gov.cn/contents/858/48647.shtml", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/henan_content_sample.html',encoding='utf-8') as f:
            province, city = henan.parse_content_html(f.read())
            self.assertEqual("河南", province.ProvinceName)
            self.assertEqual(1270, province.Confirmed)
            self.assertEqual(802, province.Healed)
            self.assertEqual("焦作市", city['jiaozuo'].CityName)
            self.assertEqual(32, city['jiaozuo'].Confirmed)


if __name__ == '__main__':
    unittest.main()
