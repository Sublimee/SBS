import unittest

from task9 import NativeDictionary
from task9_2 import NativeDictionary2
from task9_2 import NativeDictionary3

class TestNativeDictionaryPut(unittest.TestCase):

    def test_1(self):
        d = NativeDictionary(3)

        d.put("a", 1)

        self.assertTrue(d.is_key("a"))
        self.assertEqual(d.get("a"), 1)

    def test_2(self):
        d = NativeDictionary(3)

        d.put("a", 1)
        d.put("a", 2)

        self.assertTrue(d.is_key("a"))
        self.assertEqual(d.get("a"), 2)

    def test_3(self):
        d = NativeDictionary(3)

        d.put("a", 1)
        d.put("a", 2)
        d.put("b", 2)
        d.put("b", 3)
        d.put("c", 3)
        d.put("c", 4)

        self.assertTrue(d.is_key("a"))
        self.assertEqual(d.get("a"), 2)
        self.assertTrue(d.is_key("b"))
        self.assertEqual(d.get("b"), 3)
        self.assertTrue(d.is_key("c"))
        self.assertEqual(d.get("c"), 4)

class TestNativeDictionaryIsKey(unittest.TestCase):

    def test_1(self):
        d = NativeDictionary(3)

        d.put("a", 1)

        self.assertTrue(d.is_key("a"))

    def test_2(self):
        d = NativeDictionary(3)

        d.put("a", 1)

        self.assertFalse(d.is_key("b"))

    def test_3(self):
        d = NativeDictionary(3)

        d.put("a", 1)
        d.put("b", 2)
        d.put("c", 3)

        self.assertTrue(d.is_key("a"))
        self.assertTrue(d.is_key("b"))
        self.assertTrue(d.is_key("c"))
        self.assertFalse(d.is_key("d"))

class TestNativeDictionaryGet(unittest.TestCase):

    def test_1(self):
        d = NativeDictionary(3)

        d.put("a", 1)

        self.assertEqual(d.get("a"), 1)

    def test_2(self):
        d = NativeDictionary(3)

        d.put("a", 1)

        self.assertIsNone(d.get("b"))

    def test_3(self):
        d = NativeDictionary(3)

        d.put("a", 1)
        d.put("b", 2)
        d.put("c", 3)

        self.assertIsNone(d.get("d"))


class TestNativeDictionary2Put(unittest.TestCase):

    def test_1(self):
        d = NativeDictionary2()

        d.put("a", 1)

        self.assertTrue(d.is_key("a"))
        self.assertEqual(d.get("a"), 1)

    def test_2(self):
        d = NativeDictionary2()

        d.put("a", 1)
        d.put("a", 2)

        self.assertTrue(d.is_key("a"))
        self.assertEqual(d.get("a"), 2)

    def test_3(self):
        d = NativeDictionary2()

        d.put("a", 1)
        d.put("a", 2)
        d.put("b", 2)
        d.put("b", 3)
        d.put("c", 3)
        d.put("c", 4)

        self.assertTrue(d.is_key("a"))
        self.assertEqual(d.get("a"), 2)
        self.assertTrue(d.is_key("b"))
        self.assertEqual(d.get("b"), 3)
        self.assertTrue(d.is_key("c"))
        self.assertEqual(d.get("c"), 4)


class TestNativeDictionary2IsKey(unittest.TestCase):

    def test_1(self):
        d = NativeDictionary2()

        d.put("a", 1)

        self.assertTrue(d.is_key("a"))

    def test_2(self):
        d = NativeDictionary2()

        d.put("a", 1)

        self.assertFalse(d.is_key("b"))

    def test_3(self):
        d = NativeDictionary2()

        d.put("a", 1)
        d.put("b", 2)
        d.put("c", 3)

        self.assertTrue(d.is_key("a"))
        self.assertTrue(d.is_key("b"))
        self.assertTrue(d.is_key("c"))
        self.assertFalse(d.is_key("d"))

class TestNativeDictionary2Get(unittest.TestCase):

    def test_1(self):
        d = NativeDictionary2()

        d.put("a", 1)

        self.assertEqual(d.get("a"), 1)

    def test_2(self):
        d = NativeDictionary2()

        d.put("a", 1)

        self.assertIsNone(d.get("b"))

    def test_3(self):
        d = NativeDictionary2()

        d.put("a", 1)
        d.put("b", 2)
        d.put("c", 3)

        self.assertIsNone(d.get("d"))

class TestNativeDictionary2Delete(unittest.TestCase):

    def test_1(self):
        d = NativeDictionary2()

        d.put("a", 1)
        d.delete("a")

        self.assertIsNone(d.get("a"))

    def test_2(self):
        d = NativeDictionary2()

        d.put("a", 1)
        d.put("b", 2)
        d.put("c", 3)

        self.assertEqual(d.get("a"), 1)
        self.assertEqual(d.get("b"), 2)
        self.assertEqual(d.get("c"), 3)

        d.delete("a")
        self.assertIsNone(d.get("a"))
        d.delete("b")
        self.assertIsNone(d.get("b"))
        d.delete("c")
        self.assertIsNone(d.get("c"))

class TestNativeDictionary3Put(unittest.TestCase):

    def test_1(self):
        d = NativeDictionary3(4)

        d.put("00", 1)

        self.assertTrue(d.is_key("00"))
        self.assertEqual(d.get("00"), 1)

    def test_2(self):
        d = NativeDictionary3(4)

        d.put("00", 1)
        d.put("00", 2)

        self.assertTrue(d.is_key("00"))
        self.assertEqual(d.get("00"), 2)

    def test_3(self):
        d = NativeDictionary3(4)

        d.put("00", 1)
        d.put("00", 2)
        d.put("01", 2)
        d.put("01", 3)
        d.put("10", 3)
        d.put("10", 4)

        self.assertTrue(d.is_key("00"))
        self.assertEqual(d.get("00"), 2)
        self.assertTrue(d.is_key("01"))
        self.assertEqual(d.get("01"), 3)
        self.assertTrue(d.is_key("10"))
        self.assertEqual(d.get("10"), 4)

class TestNativeDictionary3IsKey(unittest.TestCase):

    def test_1(self):
        d = NativeDictionary3(4)

        d.put("00", 1)

        self.assertTrue(d.is_key("00"))

    def test_2(self):
        d = NativeDictionary3(4)

        d.put("00", 1)

        self.assertFalse(d.is_key("01"))

    def test_3(self):
        d = NativeDictionary3(4)

        d.put("00", 1)
        d.put("01", 2)
        d.put("10", 3)

        self.assertTrue(d.is_key("00"))
        self.assertTrue(d.is_key("01"))
        self.assertTrue(d.is_key("10"))
        self.assertFalse(d.is_key("11"))

class TestNativeDictionary3Get(unittest.TestCase):

    def test_1(self):
        d = NativeDictionary3(4)

        d.put("00", 1)

        self.assertEqual(d.get("00"), 1)

    def test_2(self):
        d = NativeDictionary3(4)

        d.put("00", 1)

        self.assertIsNone(d.get("01"))

    def test_3(self):
        d = NativeDictionary3(4)

        d.put("00", 1)
        d.put("01", 2)
        d.put("10", 3)

        self.assertIsNone(d.get("11"))
