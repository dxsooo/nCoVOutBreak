# -*- coding: utf-8 -*-

import unittest
import guizhou
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/guizhou_list_sample.html',encoding='utf-8') as f:
            res = guizhou.parse_list_html(f.read())
            self.assertEqual(
                "http://www.gzhfpc.gov.cn/xwzx_500663/zwyw/202002/t20200222_50658247.html", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/guizhou_content_sample.html',encoding='utf-8') as f:
            province, city = guizhou.parse_content_html(f.read())
            self.assertEqual("贵州", province.ProvinceName)
            self.assertEqual(146, province.Confirmed)
            self.assertEqual(90, province.Healed)
            self.assertEqual("遵义市", city['zunyi'].CityName)
            self.assertEqual(32, city['zunyi'].Confirmed)


if __name__ == '__main__':
    unittest.main()
