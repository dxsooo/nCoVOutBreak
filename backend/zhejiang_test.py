# -*- coding: utf-8 -*-

import unittest
import zhejiang
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/zhejiang_list_sample.html',encoding='utf-8') as f:
            res = zhejiang.parse_list_html(f.read())
            self.assertEqual(
                "http://www.blueskyinfo.com.cn/wjwApp/webinfo/infoDetail.do?infoIds"
                "=E3BE035E1EEA087FC952B932BF6EAAAF2CC43EF6984396B3C0F5FEF1265A8EAD89B6F61A83D8B50D", res)

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/zhejiang_content_sample.html',encoding='utf-8') as f:
            province, city = zhejiang.parse_content_html(f.read())
            self.assertEqual("浙江", province.ProvinceName)
            self.assertEqual(1175, province.Confirmed)
            self.assertEqual(609, province.Healed)
            self.assertEqual("杭州市", city['hangzhou'].CityName)
            self.assertEqual(169, city['hangzhou'].Confirmed)


if __name__ == '__main__':
    unittest.main()
