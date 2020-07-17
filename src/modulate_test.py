import unittest

import io
from .modulate import modulate

class ModulateTest(unittest.TestCase):
    def test_0(self):
        self.assertEqual("010", modulate(0))

    def test_1(self):
        self.assertEqual("01100001", modulate(1))

    def test_min1(self):
        self.assertEqual("10100001", modulate(-1))

    def test_empty(self):
        self.assertEqual("00", modulate([]))

    def test_trivial_list(self):
        self.assertEqual("1101000", modulate([0]))

    def test_moar(self):
        self.assertEqual("110110000111011111100001001011000000000000", modulate([1, 76800]))


