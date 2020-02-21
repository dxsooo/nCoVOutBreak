# -*- coding: utf-8 -*-

import unittest
import xizang
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/xizang_list_sample.html',encoding='utf-8') as f:
            res = xizang.parse_list_html(f.read())
            self.assertEqual(
                "http://wjw.xizang.gov.cn/xwzx/wsjkdt/202002/t20200221_132780.html", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/xizang_content_sample.html',encoding='utf-8') as f:
            province, city = xizang.parse_content_html(f.read())
            self.assertEqual("西藏", province.ProvinceName)
            self.assertEqual(1, province.Confirmed)
            self.assertEqual(1, province.Healed)
            self.assertEqual("拉萨市", city['lasa'].CityName)
            self.assertEqual(1, city['lasa'].Confirmed)


if __name__ == '__main__':
    unittest.main()
