# -*- coding: utf-8 -*-

import unittest
import neimenggu
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/neimenggu_list_sample.html',encoding='utf-8') as f:
            res = neimenggu.parse_list_html(f.read())
            self.assertEqual(
                res, "http://wjw.nmg.gov.cn/doc/2020/02/17/292305.shtml")

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/neimenggu_content_sample.html',encoding='utf-8') as f:
            province, city = neimenggu.parse_content_html(f.read())
            self.assertEqual(province.ProvinceName, "内蒙古")
            self.assertEqual(province.Confirmed, 75)
            self.assertEqual(province.Healed, 22)
            self.assertEqual(city['bayanzhuoer'].CityName, "巴彦淖尔市")
            self.assertEqual(city['bayanzhuoer'].Confirmed, 8)


if __name__ == '__main__':
    unittest.main()
