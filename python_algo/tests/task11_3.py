import unittest

from task11 import BloomFilter
from task11_2 import BloomFilterWithRemove

class TestBloomFilter(unittest.TestCase):

    def test(self):
        bf = BloomFilter(32)

        bf.add("0123456789")
        bf.add("1234567890")

        # bf.add("2345678901")
        # bf.add("3456789012")
        # bf.add("4567890123")
        # bf.add("5678901234")
        # bf.add("6789012345")
        # bf.add("7890123456")
        # bf.add("8901234567")
        # bf.add("9012345678")

        self.assertTrue(bf.is_value("0123456789"))
        self.assertTrue(bf.is_value("1234567890"))
        self.assertTrue(bf.is_value("2345678901"))
        self.assertTrue(bf.is_value("3456789012"))
        self.assertTrue(bf.is_value("4567890123"))
        self.assertTrue(bf.is_value("5678901234"))
        self.assertTrue(bf.is_value("6789012345"))
        self.assertTrue(bf.is_value("7890123456"))
        self.assertTrue(bf.is_value("8901234567"))
        self.assertTrue(bf.is_value("9012345678"))

        self.assertFalse(bf.is_value("9123456789"))
        self.assertFalse(bf.is_value("1123456789"))
        self.assertFalse(bf.is_value("0123456780"))

class TestBloomFilterWithRemove(unittest.TestCase):

    def test_1(self):
        bf = BloomFilterWithRemove(32)

        bf.add("hello")
        bf.add("hello")

        self.assertTrue(bf.is_value("hello"))

        bf.remove("hello")
        self.assertTrue(bf.is_value("hello"))

        bf.remove("hello")
        self.assertFalse(bf.is_value("hello"))

    def test_2(self):
        bf = BloomFilterWithRemove(32)

        bf.add("0123456789")
        bf.add("1234567890")

        # bf.add("2345678901")
        # bf.add("3456789012")
        # bf.add("4567890123")
        # bf.add("5678901234")
        # bf.add("6789012345")
        # bf.add("7890123456")
        # bf.add("8901234567")
        # bf.add("9012345678")

        self.assertTrue(bf.is_value("0123456789"))
        self.assertTrue(bf.is_value("1234567890"))
        self.assertTrue(bf.is_value("2345678901"))
        self.assertTrue(bf.is_value("3456789012"))
        self.assertTrue(bf.is_value("4567890123"))
        self.assertTrue(bf.is_value("5678901234"))
        self.assertTrue(bf.is_value("6789012345"))
        self.assertTrue(bf.is_value("7890123456"))
        self.assertTrue(bf.is_value("8901234567"))
        self.assertTrue(bf.is_value("9012345678"))

        self.assertFalse(bf.is_value("9123456789"))
        self.assertFalse(bf.is_value("1123456789"))
        self.assertFalse(bf.is_value("0123456780"))

    def test_3(self):
        bf = BloomFilterWithRemove(32)

        bf.add("0123456789")
        bf.add("1234567890")
        bf.add("2345678901")
        bf.add("3456789012")
        bf.add("4567890123")
        bf.add("5678901234")
        bf.add("6789012345")
        bf.add("7890123456")
        bf.add("8901234567")
        bf.add("9012345678")

        bf.remove("0123456789")
        bf.remove("1234567890")
        bf.remove("2345678901")
        bf.remove("3456789012")
        bf.remove("4567890123")
        bf.remove("5678901234")
        bf.remove("6789012345")
        bf.remove("7890123456")
        bf.remove("8901234567")

        self.assertTrue(bf.is_value("9012345678"))

        self.assertFalse(bf.is_value("9123456789"))
        self.assertFalse(bf.is_value("1123456789"))
        self.assertFalse(bf.is_value("0123456780"))