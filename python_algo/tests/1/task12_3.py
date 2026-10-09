import unittest

from task12 import NativeCache

class TestNativeCache(unittest.TestCase):

    def test_1(self):
        c = NativeCache(3)

        c.put(1, 1)

        self.assertEqual(c.get_freq(1), 0)
        self.assertEqual(c.get(1), 1)
        self.assertEqual(c.get_freq(1), 1)
        self.assertEqual(c.get_freq(1), 1)

    def test_2(self):
        c = NativeCache(3)

        c.put(1, 1)
        c.put(1, 1)
        c.put(1, 1)

        self.assertEqual(c.get_freq(1), 0)
        self.assertEqual(c.get(1), 1)
        self.assertEqual(c.get_freq(1), 1)

    def test_3(self):
        c = NativeCache(3)

        c.put(1, 1)
        c.put(2, 2)
        c.put(3, 3)

        self.assertEqual(c.get(1), 1)
        self.assertEqual(c.get(2), 2)
        self.assertEqual(c.get(3), 3)
        self.assertEqual(c.get_freq(1), 1)
        self.assertEqual(c.get_freq(2), 1)
        self.assertEqual(c.get_freq(3), 1)

    def test_4(self):
        c = NativeCache(3)

        c.put(1, 1)
        c.put(2, 2)
        c.put(3, 3)
        c.put(4, 4)

        self.assertEqual(c.get(1), 1)
        self.assertEqual(c.get(2), 2)
        self.assertEqual(c.get(3), None)
        self.assertEqual(c.get(4), 4)

        self.assertEqual(c.get_freq(1), 1)
        self.assertEqual(c.get_freq(2), 1)
        self.assertEqual(c.get_freq(3), None)
        self.assertEqual(c.get_freq(4), 1)

    def test_5(self):
        c = NativeCache(3)

        c.put(1, 1)
        c.put(2, 2)
        c.put(3, 3)
        c.put(4, 4)
        c.put(5, 6)
        c.put(6, 6)

        self.assertEqual(c.get(1), 1)
        self.assertEqual(c.get(2), 2)
        self.assertEqual(c.get(3), None)
        self.assertEqual(c.get(4), None)
        self.assertEqual(c.get(5), None)
        self.assertEqual(c.get(6), 6)

    def test_6(self):
        c = NativeCache(3)

        c.put(1, 1)
        c.put(2, 2)
        c.put(3, 3)


        self.assertEqual(c.get(1), 1)
        self.assertEqual(c.get(2), 2)
        self.assertEqual(c.get(3), 3)
        self.assertEqual(c.get(1), 1)
        self.assertEqual(c.get(2), 2)

        c.put(4, 4)

        self.assertEqual(c.get(1), 1)
        self.assertEqual(c.get(2), 2)
        self.assertEqual(c.get(3), None)
        self.assertEqual(c.get(4), 4)

        self.assertEqual(c.get_freq(1), 3)
        self.assertEqual(c.get_freq(2), 3)
        self.assertEqual(c.get_freq(3), None)
        self.assertEqual(c.get_freq(4), 1)