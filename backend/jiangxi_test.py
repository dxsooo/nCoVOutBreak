# -*- coding: utf-8 -*-

import unittest
import jiangxi
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/jiangxi_list_sample.html',encoding='utf-8') as f:
            res = jiangxi.parse_list_html(f.read())
            self.assertEqual(
                "http://hc.jiangxi.gov.cn/doc/2020/02/21/139308.shtml", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/jiangxi_content_sample.html',encoding='utf-8') as f:
            province, city = jiangxi.parse_content_html(f.read())
            self.assertEqual("江西", province.ProvinceName)
            self.assertEqual(934, province.Confirmed)
            self.assertEqual(489, province.Healed)
            self.assertEqual("赣州市", city['ganzhou'].CityName)
            self.assertEqual(76, city['ganzhou'].Confirmed)


if __name__ == '__main__':
    unittest.main()
