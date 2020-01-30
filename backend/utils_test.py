# -*- coding: utf-8 -*-

import unittest
import utils
from utils import Data
import json


class Test_parse_path(unittest.TestCase):
    def test_parse_path_1(self):
        p, c = utils.parse_path("/api/v1/provinces/guangdong/cities/dongguan")
        self.assertEqual(p, "guangdong")
        self.assertEqual(c, "dongguan")

    def test_parse_path_2(self):
        p, c = utils.parse_path("/api/v1/provinces/guangdong")
        self.assertEqual(p, "guangdong")
        self.assertIsNone(c)


class Test_data_serialize(unittest.TestCase):
    def test_data_serialize(self):
        d = Data("东莞", "dongguan")
        d.Dead = 1
        d.Confirmed = 2
        d.Healed = 3
        dd = utils.serialize(d)
        self.assertDictEqual(
            dd, {"city": "东莞", "id": "dongguan", "confirmed": 2, "dead": 1, "healed": 3})


if __name__ == '__main__':
    unittest.main()
