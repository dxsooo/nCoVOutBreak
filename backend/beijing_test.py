# -*- coding: utf-8 -*-

import unittest
import beijing
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/beijing_list_sample.html',encoding='utf-8') as f:
            res = beijing.parse_list_html(f.read())
            self.assertEqual(
                res, "http://wjw.beijing.gov.cn/xwzx_20031/xwfb/202001/t20200131_1622025.html")

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/beijing_content_sample.html',encoding='utf-8') as f:
            province, city = beijing.parse_content_html(f.read())
            self.assertEqual(province.ProvinceName, "北京")
            self.assertEqual(province.Confirmed, 139)
            self.assertEqual(province.Healed, 5)
            self.assertEqual(city['haidian'].CityName, "海淀区")
            self.assertEqual(city['haidian'].Confirmed, 27)


if __name__ == '__main__':
    unittest.main()
