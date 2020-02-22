# -*- coding: utf-8 -*-

import unittest
import hainan
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/testdata/hainan_list_sample.html',
                  encoding='utf-8') as f:
            res = hainan.parse_list_html(f.read())
            self.assertEqual(
                "http://wst.hainan.gov.cn/swjw/rdzt/yqfk/202002/t20200222_2751504.html", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/testdata/hainan_content_sample.html',
                  encoding='utf-8') as f:
            province, city = hainan.parse_content_html(f.read())
            self.assertEqual("海南", province.ProvinceName)
            self.assertEqual(168, province.Confirmed)
            self.assertEqual(96, province.Healed)
            self.assertEqual("三亚市", city['sanya'].CityName)
            self.assertEqual(54, city['sanya'].Confirmed)


if __name__ == '__main__':
    unittest.main()
