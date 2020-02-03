# -*- coding: utf-8 -*-

import unittest
import hebei
import os


class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/hebei_list_sample.html',encoding='utf-8') as f:
            res = hebei.parse_list_html(f.read())
            self.assertEqual(
                res, "http://hebwst.gov.cn/index.do?id=395837&templet=content&cid=14")

    def test_parse_content_html(self):
        with open(os.path.dirname(os.path.abspath(__file__))+'/testdata/hebei_content_sample.html',encoding='utf-8') as f:
            province, city = hebei.parse_content_html(f.read())
            self.assertEqual(province.ProvinceName, "河北")
            self.assertEqual(province.Confirmed, 82)
            self.assertEqual(province.Dead, 1)
            self.assertEqual(city['shijiazhuang'].CityName, "石家庄市")
            self.assertEqual(city['shijiazhuang'].Confirmed, 11)


if __name__ == '__main__':
    unittest.main()
