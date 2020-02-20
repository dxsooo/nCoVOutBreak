# -*- coding: utf-8 -*-

import unittest
import jiangsu
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/jiangsu_list_sample.html',encoding='utf-8') as f:
            res = jiangsu.parse_list_html(f.read())
            self.assertEqual(
                "http://wjw.jiangsu.gov.cn/art/2020/2/20/art_7290_8978359.html", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/jiangsu_content_sample.html',encoding='utf-8') as f:
            province, city = jiangsu.parse_content_html(f.read())
            self.assertEqual("江苏", province.ProvinceName)
            self.assertEqual(631, province.Confirmed)
            self.assertEqual(325, province.Healed)
            self.assertEqual("南京市", city['nanjing'].CityName)
            self.assertEqual(93, city['nanjing'].Confirmed)


if __name__ == '__main__':
    unittest.main()
