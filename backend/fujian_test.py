# -*- coding: utf-8 -*-

import unittest
import fujian
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/fujian_list_sample.html',encoding='utf-8') as f:
            res = fujian.parse_list_html(f.read())
            self.assertEqual(
                res, "http://wjw.fujian.gov.cn/xxgk/gzdt/wsjsyw/202002/t20200205_5190031.htm")

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/fujian_content_sample.html',encoding='utf-8') as f:
            province, city = fujian.parse_content_html(f.read())
            self.assertEqual(province.ProvinceName, "福建")
            self.assertEqual(province.Confirmed, 205)
            self.assertEqual(province.Healed, 7)
            self.assertEqual(city['fuzhou'].CityName, "福州市")
            self.assertEqual(city['fuzhou'].Confirmed, 55)


if __name__ == '__main__':
    unittest.main()
