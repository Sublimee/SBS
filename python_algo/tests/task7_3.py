import unittest

from task7 import OrderedList, OrderedStringList
from task7_2 import merge, max_duplicates, contains_sublist


class TestCompare(unittest.TestCase):

    def test(self):
        ol = OrderedList(True)
        ol.compare(1, 2)
        self.assertEqual(-1, ol.compare(1, 2))
        self.assertEqual(0, ol.compare(1, 1))
        self.assertEqual(1, ol.compare(2, 1))


class TestAddAsc(unittest.TestCase):

    def test_1(self):
        ol = OrderedList(True)
        ol.add(1)
        assert_order(self, ol, [1])

    def test_2(self):
        ol = OrderedList(True)
        ol.add(1)
        ol.add(2)
        assert_order(self, ol, [1, 2])

    def test_3(self):
        ol = OrderedList(True)
        ol.add(2)
        ol.add(1)
        assert_order(self, ol, [1, 2])

    def test_4(self):
        ol = OrderedList(True)
        ol.add(5)
        ol.add(6)
        ol.add(4)
        ol.add(7)
        ol.add(3)
        ol.add(8)
        assert_order(self, ol, [3, 4, 5, 6, 7, 8])

    def test_5(self):
        ol = OrderedList(True)
        ol.add(2)
        ol.add(1)
        ol.add(1)
        ol.add(2)
        assert_order(self, ol, [1, 1, 2, 2])

    def test_6(self):
        ol = OrderedList(True)
        ol.add(3)
        ol.add(2)
        ol.add(1)
        ol.add(0)
        assert_order(self, ol, [0, 1, 2, 3])


class TestAddDesc(unittest.TestCase):

    def test_1(self):
        ol = OrderedList(False)
        ol.add(1)
        assert_order(self, ol, [1])

    def test_2(self):
        ol = OrderedList(False)
        ol.add(1)
        ol.add(2)
        assert_order(self, ol, [2, 1])

    def test_3(self):
        ol = OrderedList(False)
        ol.add(2)
        ol.add(1)
        assert_order(self, ol, [2, 1])

    def test_4(self):
        ol = OrderedList(False)
        ol.add(5)
        ol.add(6)
        ol.add(4)
        ol.add(7)
        ol.add(3)
        ol.add(8)
        assert_order(self, ol, [8, 7, 6, 5, 4, 3])

    def test_5(self):
        ol = OrderedList(False)
        ol.add(2)
        ol.add(1)
        ol.add(1)
        ol.add(2)
        assert_order(self, ol, [2, 2, 1, 1])

    def test_6(self):
        ol = OrderedList(False)
        ol.add(3)
        ol.add(2)
        ol.add(1)
        ol.add(0)
        assert_order(self, ol, [3, 2, 1, 0])

    def test_7(self):
        ol = build_ordered_list([3, 2, 1, 0], False)
        assert_order(self, ol, [3, 2, 1, 0])
        ol = build_ordered_list([0, 1, 2, 3], False)
        assert_order(self, ol, [3, 2, 1, 0])
        ol = build_ordered_list([0, 2, 1, 3], False)
        assert_order(self, ol, [3, 2, 1, 0])
        ol = build_ordered_list([0, 1, 2, 3], False)
        assert_order(self, ol, [3, 2, 1, 0])


class TestFindAsc(unittest.TestCase):

    def test_1(self):
        ol = OrderedList(True)
        self.assertIsNone(ol.find(10))

    def test_2(self):
        ol = build_ordered_list([1, 2, 3], True)
        self.assertIsNone(ol.find(99))

    def test_3(self):
        ol = build_ordered_list([7], True)
        node = ol.find(7)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 7)
        self.assertIs(node, ol.head)
        self.assertIs(node, ol.tail)
        assert_order(self, ol, [7])

    def test_4(self):
        ol = build_ordered_list([7, 8, 9], True)
        node = ol.find(7)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 7)
        self.assertIs(node, ol.head)
        self.assertIsNot(node, ol.tail)
        assert_order(self, ol, [7, 8, 9])

    def test_5(self):
        ol = build_ordered_list([7, 8, 9], True)
        node = ol.find(9)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 9)
        self.assertIsNot(node, ol.head)
        self.assertIs(node, ol.tail)
        assert_order(self, ol, [7, 8, 9])

    def test_6(self):
        ol = build_ordered_list([1, 2, 3, 2, 4], True)
        node = ol.find(2)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 2)
        self.assertIs(node, ol.head.next)
        assert_order(self, ol, [1, 2, 2, 3, 4])


class TestFindDesc(unittest.TestCase):

    def test_1(self):
        ol = OrderedList(False)
        self.assertIsNone(ol.find(10))

    def test_2(self):
        ol = build_ordered_list([1, 2, 3], False)
        self.assertIsNone(ol.find(99))

    def test_3(self):
        ol = build_ordered_list([7], False)
        node = ol.find(7)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 7)
        self.assertIs(node, ol.head)
        self.assertIs(node, ol.tail)
        assert_order(self, ol, [7])

    def test_4(self):
        ol = build_ordered_list([7, 8, 9], False)
        node = ol.find(7)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 7)
        self.assertIs(node, ol.tail)
        self.assertIsNot(node, ol.head)
        assert_order(self, ol, [9, 8, 7])

    def test_5(self):
        ol = build_ordered_list([7, 8, 9], False)
        node = ol.find(9)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 9)
        self.assertIs(node, ol.head)
        self.assertIsNot(node, ol.tail)
        assert_order(self, ol, [9, 8, 7])

    def test_6(self):
        ol = build_ordered_list([1, 2, 3, 2, 4], False)
        node = ol.find(2)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 2)
        self.assertIs(node, ol.head.next.next)
        assert_order(self, ol, [4, 3, 2, 2, 1])


class TestDeleteAsc(unittest.TestCase):

    def test_1(self):
        ol = build_ordered_list([], True)
        ol.delete(42)
        self.assertIsNone(ol.head)
        self.assertIsNone(ol.tail)
        self.assertEqual(to_array(ol), [])

    def test_2(self):
        ol = build_ordered_list([42], True)
        ol.delete(42)
        self.assertIsNone(ol.head)
        self.assertIsNone(ol.tail)
        self.assertEqual(to_array(ol), [])
        assert_order(self, ol, [])

    def test_3(self):
        ol = build_ordered_list([42, 43], True)
        ol.delete(42)
        self.assertEqual(ol.head.value, 43)
        self.assertEqual(ol.tail.value, 43)
        self.assertEqual(to_array(ol), [43])
        assert_order(self, ol, [43])

    def test_4(self):
        ol = build_ordered_list([42, 43], True)
        ol.delete(43)
        self.assertEqual(ol.head.value, 42)
        self.assertEqual(ol.tail.value, 42)
        self.assertEqual(to_array(ol), [42])
        assert_order(self, ol, [42])

    def test_5(self):
        ol = build_ordered_list([42, 42, 43], True)
        ol.delete(42)
        self.assertEqual(to_array(ol), [42, 43])
        self.assertEqual(ol.head.value, 42)
        self.assertEqual(ol.tail.value, 43)
        assert_order(self, ol, [42, 43])

    def test_6(self):
        ol = build_ordered_list([42, 43, 43], True)
        ol.delete(43)
        self.assertEqual(to_array(ol), [42, 43])
        self.assertEqual(ol.head.value, 42)
        self.assertEqual(ol.tail.value, 43)
        assert_order(self, ol, [42, 43])

    def test_7(self):
        ol = build_ordered_list([1, 2, 3, 2], True)
        ol.delete(2)
        self.assertEqual(to_array(ol), [1, 2, 3])
        self.assertEqual(ol.head.value, 1)
        self.assertEqual(ol.tail.value, 3)
        assert_order(self, ol, [1, 2, 3])

    def test_8(self):
        ol = build_ordered_list([2, 2, 3, 4], True)
        ol.delete(2)
        self.assertEqual(to_array(ol), [2, 3, 4])
        self.assertEqual(ol.head.value, 2)
        self.assertEqual(ol.tail.value, 4)
        assert_order(self, ol, [2, 3, 4])

    def test_9(self):
        ol = build_ordered_list([10, 20, 30], True)
        ol.delete(10)
        self.assertEqual(to_array(ol), [20, 30])
        self.assertEqual(ol.head.value, 20)
        self.assertEqual(ol.tail.value, 30)
        assert_order(self, ol, [20, 30])

    def test_10(self):
        ol = build_ordered_list([10, 20, 30], True)
        ol.delete(30)
        self.assertEqual(to_array(ol), [10, 20])
        self.assertEqual(ol.head.value, 10)
        self.assertEqual(ol.tail.value, 20)
        assert_order(self, ol, [10, 20])

    def test_11(self):
        ol = build_ordered_list([1, 2, 3], True)
        ol.delete(99)
        self.assertEqual(to_array(ol), [1, 2, 3])
        self.assertEqual(ol.head.value, 1)
        self.assertEqual(ol.tail.value, 3)
        assert_order(self, ol, [1, 2, 3])


class TestDeleteDesc(unittest.TestCase):

    def test_1(self):
        ol = build_ordered_list([], False)
        ol.delete(42)
        self.assertIsNone(ol.head)
        self.assertIsNone(ol.tail)
        self.assertEqual(to_array(ol), [])

    def test_2(self):
        ol = build_ordered_list([42], False)
        ol.delete(42)
        self.assertIsNone(ol.head)
        self.assertIsNone(ol.tail)
        self.assertEqual(to_array(ol), [])
        assert_order(self, ol, [])

    def test_3(self):
        ol = build_ordered_list([42, 43], False)
        ol.delete(42)
        self.assertEqual(ol.head.value, 43)
        self.assertEqual(ol.tail.value, 43)
        self.assertEqual(to_array(ol), [43])
        assert_order(self, ol, [43])

    def test_4(self):
        ol = build_ordered_list([42, 43], False)
        ol.delete(43)
        self.assertEqual(ol.head.value, 42)
        self.assertEqual(ol.tail.value, 42)
        self.assertEqual(to_array(ol), [42])
        assert_order(self, ol, [42])

    def test_5(self):
        ol = build_ordered_list([42, 42, 43], False)
        ol.delete(42)
        self.assertEqual(to_array(ol), [43, 42])
        self.assertEqual(ol.head.value, 43)
        self.assertEqual(ol.tail.value, 42)
        assert_order(self, ol, [43, 42])

    def test_6(self):
        ol = build_ordered_list([42, 43, 43], False)
        ol.delete(43)
        self.assertEqual(to_array(ol), [43, 42])
        self.assertEqual(ol.head.value, 43)
        self.assertEqual(ol.tail.value, 42)
        assert_order(self, ol, [43, 42])

    def test_7(self):
        ol = build_ordered_list([1, 2, 3, 2], False)
        ol.delete(2)
        self.assertEqual(to_array(ol), [3, 2, 1])
        self.assertEqual(ol.head.value, 3)
        self.assertEqual(ol.tail.value, 1)
        assert_order(self, ol, [3, 2, 1])

    def test_8(self):
        ol = build_ordered_list([2, 2, 3, 4], False)
        ol.delete(2)
        self.assertEqual(to_array(ol), [4, 3, 2])
        self.assertEqual(ol.head.value, 4)
        self.assertEqual(ol.tail.value, 2)
        assert_order(self, ol, [4, 3, 2])

    def test_9(self):
        ol = build_ordered_list([10, 20, 30], False)
        ol.delete(10)
        self.assertEqual(to_array(ol), [30, 20])
        self.assertEqual(ol.head.value, 30)
        self.assertEqual(ol.tail.value, 20)
        assert_order(self, ol, [30, 20])

    def test_10(self):
        ol = build_ordered_list([10, 20, 30], False)
        ol.delete(30)
        self.assertEqual(to_array(ol), [20, 10])
        self.assertEqual(ol.head.value, 20)
        self.assertEqual(ol.tail.value, 10)
        assert_order(self, ol, [20, 10])

    def test_11(self):
        ol = build_ordered_list([1, 2, 3], False)
        ol.delete(99)
        self.assertEqual(to_array(ol), [3, 2, 1])
        self.assertEqual(ol.head.value, 3)
        self.assertEqual(ol.tail.value, 1)
        assert_order(self, ol, [3, 2, 1])


class TestCleanAsc(unittest.TestCase):

    def test_0(self):
        ol = build_ordered_list([1, 2, 3], True)
        ol.clean(False)
        self.assertIsNone(ol.head)
        self.assertIsNone(ol.tail)
        self.assertEqual(ol.len(), 0)
        ol.add(7)
        ol.add(9)
        ol.add(8)
        assert_order(self, ol, [9, 8, 7])

    def test_1(self):
        ol = build_ordered_list([1, 2, 3], True)
        ol.clean(True)
        self.assertIsNone(ol.head)
        self.assertIsNone(ol.tail)
        self.assertEqual(ol.len(), 0)
        assert_order(self, ol, [])

    def test_2(self):
        ol = build_ordered_list([1], True)
        ol.clean(True)
        self.assertIsNone(ol.head)
        self.assertIsNone(ol.tail)
        self.assertEqual(ol.len(), 0)
        assert_order(self, ol, [])

    def test_3(self):
        ol = build_ordered_list([1, 2], True)
        ol.clean(True)
        self.assertIsNone(ol.head)
        self.assertIsNone(ol.tail)
        self.assertEqual(ol.len(), 0)
        assert_order(self, ol, [])

    def test_4(self):
        ol = OrderedList(True)
        ol.clean(True)
        self.assertIsNone(ol.head)
        self.assertIsNone(ol.tail)
        self.assertEqual(ol.len(), 0)
        assert_order(self, ol, [])


class TestCleanDesc(unittest.TestCase):

    def test_0(self):
        ol = build_ordered_list([1, 2, 3], False)
        assert_order(self, ol, [3, 2, 1])
        ol.clean(True)
        self.assertIsNone(ol.head)
        self.assertIsNone(ol.tail)
        self.assertEqual(ol.len(), 0)
        ol.add(7)
        ol.add(9)
        ol.add(8)
        assert_order(self, ol, [7, 8, 9])

    def test_1(self):
        ol = build_ordered_list([1, 2, 3], False)
        ol.clean(False)
        self.assertIsNone(ol.head)
        self.assertIsNone(ol.tail)
        self.assertEqual(ol.len(), 0)
        assert_order(self, ol, [])

    def test_2(self):
        ol = build_ordered_list([1], False)
        ol.clean(False)
        self.assertIsNone(ol.head)
        self.assertIsNone(ol.tail)
        self.assertEqual(ol.len(), 0)
        assert_order(self, ol, [])

    def test_3(self):
        ol = build_ordered_list([1, 2], False)
        ol.clean(False)
        self.assertIsNone(ol.head)
        self.assertIsNone(ol.tail)
        self.assertEqual(ol.len(), 0)
        assert_order(self, ol, [])

    def test_4(self):
        ol = OrderedList(False)
        ol.clean(False)
        self.assertIsNone(ol.head)
        self.assertIsNone(ol.tail)
        self.assertEqual(ol.len(), 0)
        assert_order(self, ol, [])


class TestLenAsc(unittest.TestCase):

    def test_1(self):
        ol = OrderedList(True)
        self.assertEqual(ol.len(), 0)

    def test_2(self):
        ol = build_ordered_list([1, 2, 3], True)
        self.assertEqual(ol.len(), 3)

    def test_3(self):
        ol = build_ordered_list([1, 2, 3], True)
        self.assertEqual(ol.len(), 3)
        ol.delete(2)
        self.assertEqual(ol.len(), 2)
        ol.add(10)
        self.assertEqual(ol.len(), 3)
        ol.clean(True)
        self.assertEqual(ol.len(), 0)


class TestLenDesc(unittest.TestCase):

    def test_1(self):
        ol = OrderedList(False)
        self.assertEqual(ol.len(), 0)

    def test_2(self):
        ol = build_ordered_list([1, 2, 3], False)
        self.assertEqual(ol.len(), 3)

    def test_3(self):
        ol = build_ordered_list([1, 2, 3], False)
        self.assertEqual(ol.len(), 3)
        ol.delete(2)
        self.assertEqual(ol.len(), 2)
        ol.add(10)
        self.assertEqual(ol.len(), 3)
        ol.clean(False)
        self.assertEqual(ol.len(), 0)


class TestDedup(unittest.TestCase):

    def test_1(self):
        ol = OrderedList(False)
        ol.deduplicate()
        assert_order(self, ol, [])

    def test_2(self):
        ol = build_ordered_list([1], False)
        ol.deduplicate()
        assert_order(self, ol, [1])

    def test_3(self):
        ol = build_ordered_list([1, 2], False)
        ol.deduplicate()
        assert_order(self, ol, [2, 1])

    def test_4(self):
        ol = build_ordered_list([1, 2, 3], False)
        ol.deduplicate()
        assert_order(self, ol, [3, 2, 1])

    def test_5(self):
        ol = build_ordered_list([1, 1], False)
        ol.deduplicate()
        assert_order(self, ol, [1])

    def test_6(self):
        ol = build_ordered_list([1, 1, 1], False)
        ol.deduplicate()
        assert_order(self, ol, [1])

    def test_7(self):
        ol = build_ordered_list([1, 1, 1, 2, 3], False)
        ol.deduplicate()
        assert_order(self, ol, [3, 2, 1])

    def test_8(self):
        ol = build_ordered_list([1, 2, 2, 2, 3], False)
        ol.deduplicate()
        assert_order(self, ol, [3, 2, 1])

    def test_9(self):
        ol = build_ordered_list([1, 2, 3, 3, 3], False)
        ol.deduplicate()
        assert_order(self, ol, [3, 2, 1])

    def test_10(self):
        ol = build_ordered_list([1, 1, 1, 2, 2, 2, 3, 3, 3], False)
        ol.deduplicate()
        assert_order(self, ol, [3, 2, 1])


class TestOrderedStringListCompare(unittest.TestCase):

    def test(self):
        ol = OrderedStringList(True)
        self.assertEqual(-1, ol.compare("A", "a"))
        self.assertEqual(-1, ol.compare(" a ", " b "))
        self.assertEqual(0, ol.compare(" a ", "  a "))
        self.assertEqual(1, ol.compare(" b ", " a "))


class TestOrderedStringListAddAsc(unittest.TestCase):

    def test_1(self):
        ol = OrderedStringList(True)
        ol.add("a")
        assert_order(self, ol, ["a"])

    def test_2(self):
        ol = OrderedStringList(True)
        ol.add("a")
        ol.add("b")
        assert_order(self, ol, ["a", "b"])

    def test_3(self):
        ol = OrderedStringList(True)
        ol.add("b")
        ol.add("a")
        assert_order(self, ol, ["a", "b"])

    def test_4(self):
        ol = OrderedStringList(True)
        ol.add("e")
        ol.add("f")
        ol.add("d")
        ol.add("g")
        ol.add("c")
        ol.add("h")
        assert_order(self, ol, ["c", "d", "e", "f", "g", "h"])

    def test_5(self):
        ol = OrderedStringList(True)
        ol.add("b")
        ol.add("a")
        ol.add("a")
        ol.add("b")
        assert_order(self, ol, ["a", "a", "b", "b"])

    def test_6(self):
        ol = OrderedStringList(True)
        ol.add("c")
        ol.add("b")
        ol.add("a")
        ol.add("A")
        assert_order(self, ol, ["A", "a", "b", "c"])


class TestOrderedStringListAddDesc(unittest.TestCase):

    def test_1(self):
        ol = OrderedList(False)
        ol.add("a")
        assert_order(self, ol, ["a"])

    def test_2(self):
        ol = OrderedList(False)
        ol.add("a")
        ol.add("b")
        assert_order(self, ol, ["b", "a"])

    def test_3(self):
        ol = OrderedList(False)
        ol.add("b")
        ol.add("a")
        assert_order(self, ol, ["b", "a"])

    def test_4(self):
        ol = OrderedList(False)
        ol.add("e")
        ol.add("f")
        ol.add("d")
        ol.add("g")
        ol.add("c")
        ol.add("h")
        assert_order(self, ol, ["h", "g", "f", "e", "d", "c"])

    def test_5(self):
        ol = OrderedList(False)
        ol.add("b")
        ol.add("a")
        ol.add("a")
        ol.add("b")
        assert_order(self, ol, ["b", "b", "a", "a"])

    def test_6(self):
        ol = OrderedList(False)
        ol.add("c")
        ol.add("b")
        ol.add("a")
        ol.add("A")
        assert_order(self, ol, ["c", "b", "a", "A"])

    def test_7(self):
        ol = build_ordered_list(["c", "b", "a", "A"], False)
        assert_order(self, ol, ["c", "b", "a", "A"])
        ol = build_ordered_list(["A", "a", "b", "c"], False)
        assert_order(self, ol, ["c", "b", "a", "A"])
        ol = build_ordered_list(["A", "b", "a", "c"], False)
        assert_order(self, ol, ["c", "b", "a", "A"])
        ol = build_ordered_list(["A", "a", "b", "c"], False)
        assert_order(self, ol, ["c", "b", "a", "A"])


class TestMerge(unittest.TestCase):

    def test_1(self):
        ol1 = None
        ol2 = None
        result = merge(ol1, ol2)
        self.assertIsNone(result)

    def test_2(self):
        ol1 = OrderedStringList(True)
        ol2 = None
        result = merge(ol1, ol2)
        self.assertEqual(result, ol1)

    def test_3(self):
        ol2 = OrderedStringList(True)
        ol1 = None
        result = merge(ol1, ol2)
        self.assertEqual(result, ol2)

    def test_4(self):
        ol1 = OrderedStringList(False)
        ol2 = OrderedStringList(True)
        result = merge(ol1, ol2)
        self.assertIsNone(result)

    def test_5(self):
        ol1 = OrderedStringList(True)
        ol2 = OrderedStringList(False)
        result = merge(ol1, ol2)
        self.assertIsNone(result)

    def test_6(self):
        ol1 = build_ordered_list([0], False)
        ol2 = build_ordered_list([1], False)
        result = merge(ol1, ol2)
        assert_order(self, result, [1, 0])

    def test_7(self):
        ol1 = build_ordered_list([1], False)
        ol2 = build_ordered_list([0], False)
        result = merge(ol1, ol2)
        assert_order(self, result, [1, 0])

    def test_8(self):
        ol1 = build_ordered_list([1, 2], False)
        ol2 = build_ordered_list([0], False)
        result = merge(ol1, ol2)
        assert_order(self, result, [2, 1, 0])

    def test_9(self):
        ol1 = build_ordered_list([1], False)
        ol2 = build_ordered_list([-1, 0], False)
        result = merge(ol1, ol2)
        assert_order(self, result, [1, 0, -1])

    def test_10(self):
        ol1 = build_ordered_list([1, 3, 5, 7], False)
        ol2 = build_ordered_list([2, 4, 6], False)
        result = merge(ol1, ol2)
        assert_order(self, result, [7, 6, 5, 4, 3, 2, 1])

    def test_11(self):
        ol1 = build_ordered_list([0], True)
        ol2 = build_ordered_list([1], True)
        result = merge(ol1, ol2)
        assert_order(self, result, [0, 1])

    def test_12(self):
        ol1 = build_ordered_list([1], True)
        ol2 = build_ordered_list([0], True)
        result = merge(ol1, ol2)
        assert_order(self, result, [0, 1])

    def test_113(self):
        ol1 = build_ordered_list([1, 2], True)
        ol2 = build_ordered_list([0], True)
        result = merge(ol1, ol2)
        assert_order(self, result, [0, 1, 2])

    def test_14(self):
        ol1 = build_ordered_list([1], True)
        ol2 = build_ordered_list([-1, 0], True)
        result = merge(ol1, ol2)
        assert_order(self, result, [-1, 0, 1])

    def test_15(self):
        ol1 = build_ordered_list([1, 3, 5, 7], True)
        ol2 = build_ordered_list([2, 4, 6], True)
        result = merge(ol1, ol2)
        assert_order(self, result, [1, 2, 3, 4, 5, 6, 7])


class TestMaxDuplicates(unittest.TestCase):

    def test_1(self):
        ol = None
        self.assertIsNone(max_duplicates(ol))

    def test_2(self):
        ol = OrderedList(True)
        self.assertIsNone(max_duplicates(ol))

    def test_3(self):
        ol = build_ordered_list([1, 3, 5, 7], True)
        self.assertEqual(1, max_duplicates(ol))

    def test_4(self):
        ol = build_ordered_list([1, 1, 5, 7], True)
        self.assertEqual(2, max_duplicates(ol))

    def test_5(self):
        ol = build_ordered_list([1, 1, 5, 5, 5, 7], True)
        self.assertEqual(3, max_duplicates(ol))

    def test_6(self):
        ol = build_ordered_list([1, 1, 5, 5, 7, 7], True)
        self.assertEqual(2, max_duplicates(ol))

    def test_7(self):
        ol = build_ordered_list([1, 1, 1, 5, 5, 7, 7, 7], True)
        self.assertEqual(3, max_duplicates(ol))


class TestSublist(unittest.TestCase):

    def test_1(self):
        ol = None
        sublist = build_ordered_list([1], True)
        self.assertFalse(contains_sublist(ol, sublist))

    def test_2(self):
        ol = build_ordered_list([1], True)
        sublist = None
        self.assertFalse(contains_sublist(ol, sublist))

    def test_3(self):
        ol = OrderedList(True)
        sublist = build_ordered_list([1], True)
        self.assertFalse(contains_sublist(ol, sublist))

    def test_4(self):
        ol = build_ordered_list([1], True)
        sublist = OrderedList(True)
        self.assertFalse(contains_sublist(ol, sublist))

    def test_5(self):
        ol = build_ordered_list([1], True)
        sublist = build_ordered_list([1, 1], True)
        self.assertFalse(contains_sublist(ol, sublist))

    def test_6(self):
        ol = build_ordered_list([1], True)
        sublist = build_ordered_list([1], False)
        self.assertFalse(contains_sublist(ol, sublist))

    def test_7(self):
        ol = build_ordered_list([1], True)
        sublist = build_ordered_list([1], True)
        self.assertTrue(contains_sublist(ol, sublist))

    def test_8(self):
        ol = build_ordered_list([1, 2], True)
        sublist = build_ordered_list([1, 2], True)
        self.assertTrue(contains_sublist(ol, sublist))

    def test_9(self):
        ol = build_ordered_list([1, 2, 3], True)
        sublist = build_ordered_list([1, 2], True)
        self.assertTrue(contains_sublist(ol, sublist))

    def test_10(self):
        ol = build_ordered_list([1, 2, 3], True)
        sublist = build_ordered_list([2, 3], True)
        self.assertTrue(contains_sublist(ol, sublist))

    def test_11(self):
        ol = build_ordered_list([1, 2, 3], True)
        sublist = build_ordered_list([3], True)
        self.assertTrue(contains_sublist(ol, sublist))

    def test_12(self):
        ol = build_ordered_list([1, 2, 2, 3], True)
        sublist = build_ordered_list([2, 3], True)
        self.assertTrue(contains_sublist(ol, sublist))

    def test_13(self):
        ol = build_ordered_list([1, 2, 2, 3], True)
        sublist = build_ordered_list([1, 3], True)
        self.assertFalse(contains_sublist(ol, sublist))

    def test_14(self):
        ol = build_ordered_list([1, 2, 2, 3], True)
        sublist = build_ordered_list([3, 4], True)
        self.assertFalse(contains_sublist(ol, sublist))

    def test_15(self):
        ol = build_ordered_list([1, 2, 2, 3], True)
        sublist = build_ordered_list([0, 1], True)
        self.assertFalse(contains_sublist(ol, sublist))

def build_ordered_list(values, order):
    ol = OrderedList(order)
    for v in values:
        ol.add(v)
    return ol


def to_array(ol: OrderedList):
    result = []
    node = ol.head
    while node is not None:
        result.append(node.value)
        node = node.next
    return result

def assert_order(testcase: unittest.TestCase, ol: OrderedList, arr):
    if ol.head is None:
        testcase.assertIsNone(ol.tail)
        return

    testcase.assertIsNone(ol.head.prev)
    testcase.assertIsNone(ol.tail.next)

    natural_order = []
    node = ol.head
    prev = None
    while node is not None:
        natural_order.append(node.value)
        testcase.assertIs(node.prev, prev)
        if node.next is not None:
            testcase.assertIs(node.next.prev, node)
        prev = node
        node = node.next

    if ol.is_ascending():
        for i in range(len(natural_order) - 1):
            testcase.assertLessEqual(natural_order[i], natural_order[i + 1])
    else:
        for i in range(len(natural_order) - 1):
            testcase.assertGreaterEqual(natural_order[i], natural_order[i + 1])

    for i in range(len(natural_order)):
        testcase.assertEqual(natural_order[i], arr[i])

    reversed_order = []
    node = ol.tail
    nxt = None
    while node is not None:
        reversed_order.append(node.value)
        testcase.assertIs(node.next, nxt)
        if node.prev is not None:
            testcase.assertIs(node.prev.next, node)
        nxt = node
        node = node.prev

    testcase.assertEqual(reversed_order, list(reversed(natural_order)))
