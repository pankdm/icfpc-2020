import unittest

import io
from .parse_modulated import parse

def _parse(s):
    return parse(io.StringIO(s))

class ParseModulatedTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual([], _parse("00"))

    def test_0(self):
        self.assertEqual(0, _parse("010"))

    def test_1(self):
        self.assertEqual(1, _parse("01100001"))

    def test_min1(self):
        self.assertEqual(-1, _parse("10100001"))

    def test_2(self):
        self.assertEqual(2, _parse("01100010"))

    def test_min2(self):
        self.assertEqual(-2, _parse("10100010"))

    def test_16(self):
        self.assertEqual(16, _parse("0111000010000"))

    def test_min16(self):
        self.assertEqual(-16, _parse("1011000010000"))

    def test_255(self):
        self.assertEqual(255, _parse("0111011111111"))

    def test_min256(self):
        self.assertEqual(-256, _parse("101110000100000000"))

    def test_trivial_list(self):
        self.assertEqual([0], _parse("1101000"))

    def test_moar(self):
        self.assertEqual([1, 76800], _parse("110110000111011111100001001011000000000000"))
        self.assertEqual([1, 76790], _parse("110110000111011111100001001010111111011000"))

    def test_empty(self):
        self.skipTest("TODO: should not be blocking on malformed input")
        _parse("01")