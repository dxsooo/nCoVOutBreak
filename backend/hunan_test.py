# -*- coding: utf-8 -*-

import unittest
import hunan
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/testdata/hunan_list_sample.html',
                  encoding='utf-8') as f:
            res = hunan.parse_list_html(f.read())
            self.assertEqual(
                "http://wjw.hunan.gov.cn/wjw/xxgk/gzdt/zyxw_1/202002/t20200221_11186924.html", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/testdata/hunan_content_sample.html',
                  encoding='utf-8') as f:
            province, city = hunan.parse_content_html(f.read())
            self.assertEqual("湖南", province.ProvinceName)
            self.assertEqual(1011, province.Confirmed)
            self.assertEqual(638, province.Healed)
            self.assertEqual("岳阳市", city['yueyang'].CityName)
            self.assertEqual(156, city['yueyang'].Confirmed)


if __name__ == '__main__':
    unittest.main()
