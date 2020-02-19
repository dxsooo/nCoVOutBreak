# -*- coding: utf-8 -*-

import unittest
import jilin
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/jilin_list_sample.html',encoding='utf-8') as f:
            res = jilin.parse_list_html(f.read())
            self.assertEqual(
                "http://www.jl.gov.cn/szfzt/jlzxd/yqtb/202002/t20200219_6840295.html", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/jilin_content_sample.html',encoding='utf-8') as f:
            province, city = jilin.parse_content_html(f.read())
            self.assertEqual("吉林", province.ProvinceName)
            self.assertEqual(90, province.Confirmed)
            self.assertEqual(36, province.Healed)
            self.assertEqual("长春市", city['changchun'].CityName)
            self.assertEqual(21, city['siping'].Confirmed)


if __name__ == '__main__':
    unittest.main()
