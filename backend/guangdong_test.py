# -*- coding: utf-8 -*-

import unittest
import utils
import guangdong

class Test_parse_html(unittest.TestCase):
    def test_parse_list_html(self):
        with open('testdata/guangdong_list_sample.html') as f:
            res = guangdong.parse_list_html(f.read())
            self.assertEqual(res, "http://wsjkw.gd.gov.cn/zwyw_yqxx/content/post_2880075.html")

    def test_parse_content_html(self):
        with open('testdata/guangdong_content_sample.html') as f:
            res = guangdong.parse_content_html(f.read())
            self.assertEqual(res[0].CityName, "东莞市")
            self.assertEqual(res[0].Confirmed, 7)
        
if __name__ == '__main__':
    unittest.main()