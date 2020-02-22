# -*- coding: utf-8 -*-

import unittest
import xinjiang
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/testdata/xinjiang_list_sample.html',
                  encoding='utf-8') as f:
            res = xinjiang.parse_list_html(f.read())
            self.assertEqual("http://www.xjhfpc.gov.cn/info/2070/18871.htm", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/testdata/xinjiang_content_sample.html',
                  encoding='utf-8') as f:
            province, city = xinjiang.parse_content_html(f.read())
            self.assertEqual("新疆", province.ProvinceName)
            self.assertEqual(76, province.Confirmed)
            self.assertEqual(22, province.Healed)
            self.assertEqual("吐鲁番市", city['tulufan'].CityName)
            self.assertEqual(2, city['tulufan'].Confirmed)


if __name__ == '__main__':
    unittest.main()
