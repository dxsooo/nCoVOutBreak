# -*- coding: utf-8 -*-

import unittest
import shaanxi
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/testdata/shaanxi_list_sample.html',
                  encoding='utf-8') as f:
            res = shaanxi.parse_list_html(f.read())
            self.assertEqual(
                "http://sxwjw.shaanxi.gov.cn/art/2020/2/22/art_9_68231.html", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/testdata/shaanxi_content_sample.html',
                  encoding='utf-8') as f:
            province, city = shaanxi.parse_content_html(f.read())
            self.assertEqual("陕西", province.ProvinceName)
            self.assertEqual(245, province.Confirmed)
            self.assertEqual(140, province.Healed)
            self.assertEqual("宝鸡市", city['baoji'].CityName)
            self.assertEqual(13, city['baoji'].Confirmed)


if __name__ == '__main__':
    unittest.main()
