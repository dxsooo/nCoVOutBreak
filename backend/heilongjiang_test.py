# -*- coding: utf-8 -*-

import unittest
import heilongjiang
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/heilongjiang_list_sample.html',encoding='utf-8') as f:
            res = heilongjiang.parse_list_html(f.read())
            self.assertEqual(
                "http://wsjkw.hlj.gov.cn/index.php/Home/Zwgk/show/newsid/7975/navid/42/stypeid/", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/heilongjiang_content_sample.html',encoding='utf-8') as f:
            province, city = heilongjiang.parse_content_html(f.read())
            self.assertEqual("黑龙江", province.ProvinceName)
            self.assertEqual(476, province.Confirmed)
            self.assertEqual(123, province.Healed)
            self.assertEqual("哈尔滨市", city['haerbin'].CityName)
            self.assertEqual(194, city['haerbin'].Confirmed)


if __name__ == '__main__':
    unittest.main()
