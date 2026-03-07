import unittest
import time

from task10 import PowerSet
from task10_2 import cartesian_product, intersection_multiple, Bag

class TestPowerSetPut(unittest.TestCase):

    def test_1(self):
        s = PowerSet()
        s.put("a")

        self.assertTrue(s.get("a"))
        self.assertEqual(s.size(), 1)

    def test_2(self):
        s = PowerSet()
        s.put("a")
        s.put("a")

        self.assertTrue(s.get("a"))
        self.assertEqual(s.size(), 1)


class TestPowerSetRemove(unittest.TestCase):

    def test_1(self):
        s = PowerSet()
        s.put("a")
        s.put("b")

        self.assertTrue(s.remove("a"))
        self.assertFalse(s.get("a"))
        self.assertEqual(s.size(), 1)

    def test_2(self):
        s = PowerSet()
        s.put("a")

        self.assertFalse(s.remove("b"))
        self.assertTrue(s.get("a"))
        self.assertEqual(s.size(), 1)


class TestPowerSetIntersection(unittest.TestCase):

    def test_1(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("a")
        set1.put("b")
        set1.put("c")

        set2.put("b")
        set2.put("c")
        set2.put("d")

        result = set1.intersection(set2)

        self.assertEqual(result.size(), 2)
        self.assertFalse(result.get("a"))
        self.assertTrue(result.get("b"))
        self.assertTrue(result.get("c"))
        self.assertFalse(result.get("d"))

    def test_2(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("a")
        set1.put("b")

        set2.put("c")
        set2.put("d")

        result = set1.intersection(set2)

        self.assertEqual(result.size(), 0)
        self.assertFalse(result.get("a"))
        self.assertFalse(result.get("b"))
        self.assertFalse(result.get("c"))
        self.assertFalse(result.get("d"))


class TestPowerSetUnion(unittest.TestCase):

    def test_1(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("a")
        set1.put("b")

        set2.put("b")
        set2.put("c")

        result = set1.union(set2)

        self.assertEqual(result.size(), 3)
        self.assertTrue(result.get("a"))
        self.assertTrue(result.get("b"))
        self.assertTrue(result.get("c"))

    def test_2(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("a")
        set1.put("b")

        result = set1.union(set2)

        self.assertEqual(result.size(), 2)
        self.assertTrue(result.get("a"))
        self.assertTrue(result.get("b"))

    def test_3(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set2.put("a")
        set2.put("b")

        result = set1.union(set2)

        self.assertEqual(result.size(), 2)
        self.assertTrue(result.get("a"))
        self.assertTrue(result.get("b"))


class TestPowerSetDifference(unittest.TestCase):

    def test_1(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("a")
        set1.put("b")
        set1.put("c")

        set2.put("b")

        result = set1.difference(set2)

        self.assertEqual(result.size(), 2)
        self.assertTrue(result.get("a"))
        self.assertTrue(result.get("c"))
        self.assertFalse(result.get("b"))

    def test_2(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("a")
        set1.put("b")

        set2.put("a")
        set2.put("b")

        result = set1.difference(set2)

        self.assertEqual(result.size(), 0)
        self.assertFalse(result.get("a"))
        self.assertFalse(result.get("b"))

    def test_3(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set2.put("a")
        set2.put("b")

        result = set1.difference(set2)

        self.assertEqual(result.size(), 0)
        self.assertFalse(result.get("a"))
        self.assertFalse(result.get("b"))


class TestPowerSetIsSubset(unittest.TestCase):

    def test_1(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("a")
        set1.put("b")
        set1.put("c")

        set2.put("a")
        set2.put("b")

        self.assertTrue(set1.issubset(set2))

    def test_2(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("a")
        set1.put("b")

        set2.put("a")
        set2.put("b")
        set2.put("c")

        self.assertFalse(set1.issubset(set2))

    def test_3(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("a")
        set1.put("b")
        set1.put("c")

        set2.put("a")
        set2.put("d")

        self.assertFalse(set1.issubset(set2))

    def test_4(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("a")
        set1.put("b")
        set1.put("c")

        self.assertTrue(set1.issubset(set2))

    def test_5(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set2.put("a")
        set2.put("b")
        set2.put("c")

        self.assertFalse(set1.issubset(set2))


class TestPowerSetEquals(unittest.TestCase):

    def test_1(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("a")
        set1.put("b")

        set2.put("b")
        set2.put("a")

        self.assertTrue(set1.equals(set2))

    def test_2(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("a")
        set1.put("b")

        set2.put("a")
        set2.put("c")

        self.assertFalse(set1.equals(set2))

    def test_3(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("a")
        set1.put("b")

        set2.put("a")

        self.assertFalse(set1.equals(set2))

    def test_4(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set2.put("a")

        self.assertFalse(set1.equals(set2))

    def test_5(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("a")
        set1.put("b")

        self.assertFalse(set1.equals(set2))

class TestPowerSetPerformance(unittest.TestCase):

    def test(self):
        set1 = PowerSet()
        set2 = PowerSet()

        n = 50000

        for i in range(n):
            set1.put(i)
            set2.put(25000 + i)

        start = time.time()

        set1.intersection(set2)
        set1.union(set2)
        set1.difference(set2)
        set1.issubset(set2)
        set1.equals(set2)

        self.assertLess(time.time() - start, 2.0)

class TestPowerSetCartesianProduct(unittest.TestCase):

    def test_0(self):
        set1 = None
        set2 = None

        result = cartesian_product(set1, set2)

        self.assertEqual(result, None)

    def test_1(self):
        set1 = None
        set2 = PowerSet()

        result = cartesian_product(set1, set2)

        self.assertEqual(result, None)

    def test_2(self):
        set1 = PowerSet()
        set2 = None

        result = cartesian_product(set1, set2)

        self.assertEqual(result, None)

    def test_3(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("1")
        set1.put("2")

        set2.put("a")
        set2.put("b")

        result = cartesian_product(set1, set2)

        self.assertEqual(result.size(), 4)
        self.assertTrue(result.get(("1", "a")))
        self.assertTrue(result.get(("1", "b")))
        self.assertTrue(result.get(("2", "a")))
        self.assertTrue(result.get(("2", "b")))

    def test_4(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("1")
        set1.put("2")

        result = cartesian_product(set1, set2)

        self.assertEqual(result.size(), 0)

    def test_5(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set2.put("a")
        set2.put("b")

        result = cartesian_product(set1, set2)

        self.assertEqual(result.size(), 0)

    def test_6(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("1")
        set2.put("a")

        result = cartesian_product(set1, set2)

        self.assertEqual(result.size(), 1)
        self.assertTrue(result.get(("1", "a")))

    def test_7(self):
        set1 = PowerSet()
        set2 = PowerSet()

        set1.put("1")
        set1.put("2")

        set2.put("a")

        result = cartesian_product(set1, set2)

        self.assertEqual(result.size(), 2)
        self.assertTrue(result.get(("1", "a")))
        self.assertTrue(result.get(("2", "a")))

class TestPowerSetIntersectionMultiple(unittest.TestCase):

    def test_1(self):
        set1 = PowerSet()
        set2 = PowerSet()
        set3 = PowerSet()

        set1.put("a")
        set1.put("b")
        set1.put("c")

        set2.put("b")
        set2.put("c")
        set2.put("d")

        set3.put("b")
        set3.put("c")
        set3.put("e")

        result = intersection_multiple([set1, set2, set3])

        self.assertEqual(result.size(), 2)
        self.assertFalse(result.get("a"))
        self.assertTrue(result.get("b"))
        self.assertTrue(result.get("c"))
        self.assertFalse(result.get("d"))
        self.assertFalse(result.get("e"))

    def test_2(self):
        set1 = PowerSet()
        set2 = PowerSet()
        set3 = PowerSet()

        set1.put("a")
        set1.put("b")

        set2.put("b")
        set2.put("c")

        set3.put("d")
        set3.put("e")

        result = intersection_multiple([set1, set2, set3])

        self.assertEqual(result.size(), 0)
        self.assertFalse(result.get("a"))
        self.assertFalse(result.get("b"))
        self.assertFalse(result.get("c"))
        self.assertFalse(result.get("d"))
        self.assertFalse(result.get("e"))

    def test_3(self):
        set1 = PowerSet()
        set2 = PowerSet()
        set3 = PowerSet()
        set4 = PowerSet()

        set1.put("b")
        set1.put("c")
        set1.put("d")
        set1.put("e")

        set2.put("c")
        set2.put("d")
        set2.put("e")
        set2.put("f")

        set3.put("a")
        set3.put("c")
        set3.put("d")
        set3.put("g")

        set4.put("c")
        set4.put("d")
        set4.put("h")

        result = intersection_multiple([set1, set2, set3, set4])

        self.assertEqual(result.size(), 2)
        self.assertFalse(result.get("a"))
        self.assertFalse(result.get("b"))
        self.assertTrue(result.get("c"))
        self.assertTrue(result.get("d"))
        self.assertFalse(result.get("e"))
        self.assertFalse(result.get("f"))
        self.assertFalse(result.get("g"))
        self.assertFalse(result.get("h"))

    def test_4(self):
        set1 = PowerSet()
        set2 = PowerSet()
        set3 = PowerSet()

        set1.put("a")
        set2.put("a")
        set3.put("a")

        result = intersection_multiple([set1, set2, set3])

        self.assertEqual(result.size(), 1)
        self.assertTrue(result.get("a"))

    def test_5(self):
        set1 = PowerSet()
        set2 = PowerSet()
        set3 = PowerSet()

        set1.put("a")
        set1.put("b")
        set1.put("c")

        set2.put("a")
        set2.put("b")
        set2.put("c")

        set3.put("a")
        set3.put("b")
        set3.put("c")

        result = intersection_multiple([set1, set2, set3])

        self.assertEqual(result.size(), 3)
        self.assertTrue(result.get("a"))
        self.assertTrue(result.get("b"))
        self.assertTrue(result.get("c"))

class TestBag(unittest.TestCase):

    def test_1(self):
        bag = Bag(10)

        bag.put("a")

        result = bag.get_all()

        self.assertEqual(len(result), 1)
        self.assertIn(("a", 1), result)

    def test_2(self):
        bag = Bag(10)

        bag.put("a")
        bag.put("a")
        bag.put("a")

        result = bag.get_all()

        self.assertEqual(len(result), 1)
        self.assertIn(("a", 3), result)

    def test_3(self):
        bag = Bag(10)

        bag.put("a")
        bag.put("b")
        bag.put("a")

        result = bag.get_all()

        self.assertEqual(len(result), 2)
        self.assertIn(("a", 2), result)
        self.assertIn(("b", 1), result)

    def test_4(self):
        bag = Bag(10)

        bag.put("a")
        bag.put("a")
        bag.put("a")

        bag.remove("a")

        result = bag.get_all()

        self.assertEqual(len(result), 1)
        self.assertIn(("a", 2), result)

    def test_5(self):
        bag = Bag(10)

        bag.put("a")

        bag.remove("a")

        result = bag.get_all()

        self.assertEqual(result, [])

    def test_6(self):
        bag = Bag(10)

        bag.put("a")
        bag.put("b")

        bag.remove("c")

        result = bag.get_all()

        self.assertEqual(len(result), 2)
        self.assertIn(("a", 1), result)
        self.assertIn(("b", 1), result)

    def test_7(self):
        bag = Bag(10)

        bag.put("a")
        bag.put("a")
        bag.put("b")
        bag.put("b")
        bag.put("b")
        bag.put("c")

        bag.remove("b")
        bag.remove("a")

        result = bag.get_all()

        self.assertEqual(len(result), 3)
        self.assertIn(("a", 1), result)
        self.assertIn(("b", 2), result)
        self.assertIn(("c", 1), result)

    def test_8(self):
        bag = Bag(3)

        bag.put("a")
        bag.put("b")
        bag.put("c")

        result = bag.get_all()

        self.assertEqual(len(result), 3)
        self.assertIn(("a", 1), result)
        self.assertIn(("b", 1), result)
        self.assertIn(("c", 1), result)

        bag.remove("a")
        bag.remove("b")
        bag.remove("c")

        result = bag.get_all()

        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

        bag.put("a")
        bag.put("b")
        bag.put("c")

        result = bag.get_all()

        self.assertEqual(len(result), 3)
        self.assertIn(("a", 1), result)
        self.assertIn(("b", 1), result)
        self.assertIn(("c", 1), result)