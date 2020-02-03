# -*- coding: utf-8 -*-

import unittest
import utils
from utils import CityData, ProvinceData
import json


class Test_data_serialize(unittest.TestCase):
    def test_citydata_serialize(self):
        d = CityData("东莞", "dongguan")
        d.Dead = 1
        d.Confirmed = 2
        d.Healed = 3
        dd = utils.serialize(d)
        self.assertDictEqual(
            dd, {"city": "东莞", "id": "dongguan", "confirmed": 2, "dead": 1, "healed": 3})

    def test_provincedata_serialize(self):
        d = ProvinceData("广东", "guangdong")
        d.Dead = 1
        d.Confirmed = 2
        d.Healed = 3
        dd = utils.serialize(d)
        self.assertDictEqual(
            dd, {"province": "广东", "id": "guangdong", "confirmed": 2, "dead": 1, "healed": 3, "cities":[]})


if __name__ == '__main__':
    unittest.main()
