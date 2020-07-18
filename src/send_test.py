import unittest

from .send import do_send

class SendTest(unittest.TestCase):
    def test_0(self):
        self.assertEqual("1101000", do_send("0"))
