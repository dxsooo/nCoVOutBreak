# -*- coding: utf-8 -*-

import unittest
import yunnan
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/yunnan_list_sample.html',encoding='utf-8') as f:
            res = yunnan.parse_list_html(f.read())
            self.assertEqual(
                "http://ynswsjkw.yn.gov.cn/wjwWebsite/web/doc/UU158234523403199682", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/yunnan_content_sample.html',encoding='utf-8') as f:
            province, city = yunnan.parse_content_html(f.read())
            self.assertEqual("云南", province.ProvinceName)
            self.assertEqual(174, province.Confirmed)
            self.assertEqual(107, province.Healed)
            self.assertEqual("大理白族自治州", city['dali'].CityName)
            self.assertEqual(13, city['dali'].Confirmed)


if __name__ == '__main__':
    unittest.main()
