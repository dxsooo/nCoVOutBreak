# -*- coding: utf-8 -*-

import unittest
import guangxi
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/guangxi_list_sample.html',encoding='utf-8') as f:
            res = guangxi.parse_list_html(f.read())
            self.assertEqual(
                "http://wsjkw.gxzf.gov.cn/zhuantiqu/ncov/ncovyqtb/2020/0222/69155.html", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/guangxi_content_sample.html',encoding='utf-8') as f:
            province, city = guangxi.parse_content_html(f.read())
            self.assertEqual("广西", province.ProvinceName)
            self.assertEqual(249, province.Confirmed)
            self.assertEqual(99, province.Healed)
            self.assertEqual("桂林市", city['guilin'].CityName)
            self.assertEqual(32, city['guilin'].Confirmed)


if __name__ == '__main__':
    unittest.main()
