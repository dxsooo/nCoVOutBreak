# -*- coding: utf-8 -*-

import unittest
import qinghai
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/qinghai_list_sample.html',encoding='utf-8') as f:
            res = qinghai.parse_list_html(f.read())
            self.assertEqual(
                "https://wsjkw.qinghai.gov.cn/zhxw/xwzx/2020/02/22/1582332560919.html", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/qinghai_content_sample.html',encoding='utf-8') as f:
            province, city = qinghai.parse_content_html(f.read())
            self.assertEqual("青海", province.ProvinceName)
            self.assertEqual(18, province.Confirmed)
            self.assertEqual(18, province.Healed)
            self.assertEqual("西宁市", city['xining'].CityName)
            self.assertEqual(15, city['xining'].Confirmed)


if __name__ == '__main__':
    unittest.main()
