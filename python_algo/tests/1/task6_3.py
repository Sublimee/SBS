import unittest

from task6 import Deque
from task6_2 import DequeMin, Deque2
from task6_2 import build_deque, isPalindrome


class TestAddFront(unittest.TestCase):

    def test_1(self):
        d = Deque()
        item = 10
        d.addFront(item)
        self.assertIs(d.head.value, item)
        self.assertIs(d.tail.value, item)
        self.assertEqual(to_array(d), [10])
        assert_order(self, d)

    def test_2(self):
        d = build_deque([1, 2, 3])
        item = 99
        d.addFront(item)
        self.assertEqual(to_array(d), [99, 1, 2, 3])
        self.assertIs(d.head.value, item)
        self.assertEqual(d.tail.value, 3)
        assert_order(self, d)

    def test_3(self):
        d = build_deque([1, 2, 3])
        item = 99
        another_item = 98
        d.addFront(item)
        d.addFront(another_item)
        self.assertEqual(to_array(d), [98, 99, 1, 2, 3])
        self.assertIs(d.head.value, another_item)
        self.assertEqual(d.tail.value, 3)
        assert_order(self, d)


class TestAddTail(unittest.TestCase):

    def test_1(self):
        d = Deque()
        item = 10
        d.addTail(item)
        self.assertIs(d.head.value, item)
        self.assertIs(d.tail.value, item)
        self.assertEqual(to_array(d), [10])
        assert_order(self, d)

    def test_2(self):
        d = build_deque([1, 2, 3])
        item = 99
        d.addTail(item)
        self.assertEqual(to_array(d), [1, 2, 3, 99])
        self.assertIs(d.head.value, 1)
        self.assertEqual(d.tail.value, 99)
        assert_order(self, d)

    def test_3(self):
        d = build_deque([1, 2, 3])
        item = 99
        another_item = 98
        d.addTail(item)
        d.addTail(another_item)
        self.assertEqual(to_array(d), [1, 2, 3, 99, 98])
        self.assertIs(d.head.value, 1)
        self.assertEqual(d.tail.value, another_item)
        assert_order(self, d)


class TestRemoveFront(unittest.TestCase):

    def test_0(self):
        d = Deque()
        d.removeFront()
        self.assertIs(d.head, None)
        self.assertIs(d.tail, None)
        self.assertEqual(d.size(), 0)

    def test_1(self):
        d = build_deque([1])
        d.removeFront()
        self.assertIs(d.head, None)
        self.assertIs(d.tail, None)
        self.assertEqual(d.size(), 0)

    def test_2(self):
        d = build_deque([1, 2])
        d.removeFront()
        self.assertEqual(to_array(d), [2])
        self.assertIs(d.head.value, 2)
        self.assertEqual(d.tail.value, 2)
        assert_order(self, d)

    def test_3(self):
        d = build_deque([1, 2, 3])
        d.removeFront()
        self.assertEqual(to_array(d), [2, 3])
        self.assertIs(d.head.value, 2)
        self.assertEqual(d.tail.value, 3)
        assert_order(self, d)

    def test_4(self):
        d = build_deque([1, 2, 3])
        d.removeFront()
        d.removeFront()
        self.assertEqual(to_array(d), [3])
        self.assertIs(d.head.value, 3)
        self.assertEqual(d.tail.value, 3)
        assert_order(self, d)


class TestRemoveTail(unittest.TestCase):

    def test_0(self):
        d = Deque()
        d.removeTail()
        self.assertIs(d.head, None)
        self.assertIs(d.tail, None)
        self.assertEqual(d.size(), 0)

    def test_1(self):
        d = build_deque([1])
        d.removeTail()
        self.assertIs(d.head, None)
        self.assertIs(d.tail, None)
        self.assertEqual(d.size(), 0)

    def test_2(self):
        d = build_deque([1, 2])
        d.removeTail()
        self.assertEqual(to_array(d), [1])
        self.assertIs(d.head.value, 1)
        self.assertEqual(d.tail.value, 1)
        assert_order(self, d)

    def test_3(self):
        d = build_deque([1, 2, 3])
        d.removeTail()
        self.assertEqual(to_array(d), [1, 2])
        self.assertIs(d.head.value, 1)
        self.assertEqual(d.tail.value, 2)
        assert_order(self, d)

    def test_4(self):
        d = build_deque([1, 2, 3])
        d.removeTail()
        d.removeTail()
        self.assertEqual(to_array(d), [1])
        self.assertIs(d.head.value, 1)
        self.assertEqual(d.tail.value, 1)
        assert_order(self, d)


class TestSize(unittest.TestCase):

    def test_1(self):
        d = Deque()
        self.assertEqual(d.size(), 0)

    def test_2(self):
        d = build_deque([1, 2, 3])
        self.assertEqual(d.size(), 3)

    def test_3(self):
        d = build_deque([1, 2, 3])
        self.assertEqual(d.size(), 3)
        d.addFront(10)
        self.assertEqual(d.size(), 4)
        d.addTail(10)
        self.assertEqual(d.size(), 5)
        d.removeTail()
        self.assertEqual(d.size(), 4)
        d.removeFront()
        self.assertEqual(d.size(), 3)
        d.removeFront()
        self.assertEqual(d.size(), 2)
        d.removeFront()
        self.assertEqual(d.size(), 1)
        d.removeFront()
        self.assertEqual(d.size(), 0)
        d.removeFront()
        self.assertEqual(d.size(), 0)


class TestIsPalindrome(unittest.TestCase):

    def test_0(self):
        self.assertFalse(isPalindrome(None))

    def test_1(self):
        self.assertFalse(isPalindrome(""))

    def test_2(self):
        self.assertTrue(isPalindrome("a"))

    def test_3(self):
        self.assertTrue(isPalindrome("aa"))

    def test_4(self):
        self.assertTrue(isPalindrome("aaa"))

    def test_5(self):
        self.assertTrue(isPalindrome("aba"))

    def test_6(self):
        self.assertTrue(isPalindrome("заказ"))

    def test_7(self):
        self.assertTrue(isPalindrome("а роза упала на лапу Азора!"))

    def test_8(self):
        self.assertFalse(isPalindrome("abbc"))


class TestMinDequeAddFront(unittest.TestCase):

    def test_1(self):
        d = DequeMin()
        self.assertEqual(min_deque_to_array(d), [])
        self.assertIsNone(d.min())

    def test_2(self):
        d = DequeMin()
        d.addFront(5)
        self.assertEqual(min_deque_to_array(d), [5])
        self.assertEqual(d.min(), 5)

    def test_3(self):
        d = DequeMin()
        d.addFront(3)
        self.assertEqual(min_deque_to_array(d), [3])
        d.addFront(2)
        self.assertEqual(min_deque_to_array(d), [2, 3])
        d.addFront(1)
        self.assertEqual(min_deque_to_array(d), [1, 2, 3])
        self.assertEqual(d.min(), 1)

    def test_4(self):
        d = DequeMin()
        d.addFront(2)
        self.assertEqual(min_deque_to_array(d), [2])
        self.assertEqual(d.min(), 2)
        d.addFront(2)
        self.assertEqual(min_deque_to_array(d), [2, 2])
        self.assertEqual(d.min(), 2)
        d.addFront(1)
        self.assertEqual(min_deque_to_array(d), [1, 2, 2])
        self.assertEqual(d.min(), 1)

    def test_5(self):
        d = DequeMin()
        d.addFront(4)
        d.addFront(3)
        d.addFront(2)
        d.addFront(1)
        self.assertEqual(min_deque_to_array(d), [1, 2, 3, 4])
        self.assertEqual(d.min(), 1)
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [2, 3, 4])
        self.assertEqual(d.min(), 2)
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [3, 4])
        self.assertEqual(d.min(), 3)

    def test_6(self):
        d = DequeMin()
        d.addFront(4)
        d.addFront(3)
        d.addFront(2)
        d.addFront(1)
        self.assertEqual(min_deque_to_array(d), [1, 2, 3, 4])
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [1, 2, 3])
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [1, 2])
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [1])
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [])
        self.assertIsNone(d.min())

    def test_7(self):
        d = DequeMin()
        d.addFront(-1)
        self.assertEqual(min_deque_to_array(d), [-1])
        self.assertEqual(d.min(), -1)
        d.addFront(-2)
        self.assertEqual(min_deque_to_array(d), [-2, -1])
        self.assertEqual(d.min(), -2)
        d.addFront(0)
        self.assertEqual(min_deque_to_array(d), [0, -2, -1])
        self.assertEqual(d.min(), -2)

    def test_8(self):
        d = DequeMin()
        d.addFront(10)
        d.addFront(9)
        self.assertEqual(min_deque_to_array(d), [9, 10])
        self.assertEqual(d.min(), 9)
        d.removeFront()
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [])
        self.assertIsNone(d.min())
        d.addFront(7)
        self.assertEqual(min_deque_to_array(d), [7])
        self.assertEqual(d.min(), 7)


class TestMinDequeAddTail(unittest.TestCase):

    def test_1(self):
        d = DequeMin()
        self.assertEqual(min_deque_to_array(d), [])
        self.assertIsNone(d.min())

    def test_2(self):
        d = DequeMin()
        d.addTail(5)
        self.assertEqual(min_deque_to_array(d), [5])
        self.assertEqual(d.min(), 5)

    def test_3(self):
        d = DequeMin()
        d.addTail(1)
        self.assertEqual(min_deque_to_array(d), [1])
        d.addTail(2)
        self.assertEqual(min_deque_to_array(d), [1, 2])
        d.addTail(3)
        self.assertEqual(min_deque_to_array(d), [1, 2, 3])
        self.assertEqual(d.min(), 1)

    def test_4(self):
        d = DequeMin()
        d.addTail(2)
        self.assertEqual(min_deque_to_array(d), [2])
        self.assertEqual(d.min(), 2)
        d.addTail(2)
        self.assertEqual(min_deque_to_array(d), [2, 2])
        self.assertEqual(d.min(), 2)
        d.addTail(1)
        self.assertEqual(min_deque_to_array(d), [2, 2, 1])
        self.assertEqual(d.min(), 1)

    def test_5(self):
        d = DequeMin()
        d.addTail(1)
        d.addTail(2)
        d.addTail(3)
        d.addTail(4)
        self.assertEqual(min_deque_to_array(d), [1, 2, 3, 4])
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [1, 2, 3])
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [1, 2])
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [1])
        self.assertEqual(d.min(), 1)

    def test_6(self):
        d = DequeMin()
        d.addTail(1)
        d.addTail(2)
        d.addTail(3)
        d.addTail(4)
        self.assertEqual(min_deque_to_array(d), [1, 2, 3, 4])
        self.assertEqual(d.min(), 1)
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [2, 3, 4])
        self.assertEqual(d.min(), 2)
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [3, 4])
        self.assertEqual(d.min(), 3)

    def test_7(self):
        d = DequeMin()
        d.addTail(-1)
        self.assertEqual(min_deque_to_array(d), [-1])
        self.assertEqual(d.min(), -1)
        d.addTail(-2)
        self.assertEqual(min_deque_to_array(d), [-1, -2])
        self.assertEqual(d.min(), -2)
        d.addTail(0)
        self.assertEqual(min_deque_to_array(d), [-1, -2, 0])
        self.assertEqual(d.min(), -2)

    def test_8(self):
        d = DequeMin()
        d.addTail(9)
        d.addTail(10)
        self.assertEqual(min_deque_to_array(d), [9, 10])
        self.assertEqual(d.min(), 9)
        d.removeTail()
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [])
        self.assertIsNone(d.min())
        d.addTail(7)
        self.assertEqual(min_deque_to_array(d), [7])
        self.assertEqual(d.min(), 7)


class TestMinDequeRemoveFront(unittest.TestCase):

    def test_1(self):
        d = DequeMin()
        d.addFront(5)
        self.assertEqual(min_deque_to_array(d), [5])
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [])
        self.assertIsNone(d.min())

    def test_2(self):
        d = DequeMin()
        d.addFront(3)
        d.addFront(2)
        d.addFront(1)
        self.assertEqual(min_deque_to_array(d), [1, 2, 3])
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [2, 3])
        self.assertEqual(d.min(), 2)
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [3])
        self.assertEqual(d.min(), 3)

    def test_3(self):
        d = DequeMin()
        d.addTail(1)
        d.addTail(2)
        d.addTail(3)
        self.assertEqual(min_deque_to_array(d), [1, 2, 3])
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [2, 3])
        self.assertEqual(d.min(), 2)

    def test_4(self):
        d = DequeMin()
        d.addFront(2)
        d.addFront(2)
        d.addFront(1)
        d.addFront(1)
        self.assertEqual(min_deque_to_array(d), [1, 1, 2, 2])
        self.assertEqual(d.min(), 1)
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [1, 2, 2])
        self.assertEqual(d.min(), 1)
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [2, 2])
        self.assertEqual(d.min(), 2)

    def test_5(self):
        d = DequeMin()
        d.addFront(3)
        d.addFront(2)
        d.addFront(1)
        self.assertEqual(min_deque_to_array(d), [1, 2, 3])
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [2, 3])
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [3])
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [])
        self.assertIsNone(d.min())

    def test_6(self):
        d = DequeMin()
        d.addTail(3)
        d.addFront(2)
        d.addTail(4)
        d.addFront(1)
        self.assertEqual(min_deque_to_array(d), [1, 2, 3, 4])
        self.assertEqual(d.min(), 1)
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [2, 3, 4])
        self.assertEqual(d.min(), 2)

    def test_7(self):
        d = DequeMin()
        d.addFront(-1)
        d.addFront(-2)
        d.addFront(0)
        self.assertEqual(min_deque_to_array(d), [0, -2, -1])
        self.assertEqual(d.min(), -2)
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [-2, -1])
        self.assertEqual(d.min(), -2)

    def test_8(self):
        d = DequeMin()
        d.addTail(1)
        d.addTail(2)
        self.assertEqual(min_deque_to_array(d), [1, 2])
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [2])
        d.removeFront()
        self.assertEqual(min_deque_to_array(d), [])
        self.assertIsNone(d.min())
        d.addFront(5)
        self.assertEqual(min_deque_to_array(d), [5])
        self.assertEqual(d.min(), 5)


class TestMinDequeRemoveTail(unittest.TestCase):

    def test_1(self):
        d = DequeMin()
        d.addTail(5)
        self.assertEqual(min_deque_to_array(d), [5])
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [])
        self.assertIsNone(d.min())

    def test_2(self):
        d = DequeMin()
        d.addTail(1)
        d.addTail(2)
        d.addTail(3)
        self.assertEqual(min_deque_to_array(d), [1, 2, 3])
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [1, 2])
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [1])
        self.assertEqual(d.min(), 1)

    def test_3(self):
        d = DequeMin()
        d.addFront(3)
        d.addFront(2)
        d.addFront(1)
        self.assertEqual(min_deque_to_array(d), [1, 2, 3])
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [1, 2])
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [1])
        self.assertEqual(d.min(), 1)

    def test_4(self):
        d = DequeMin()
        d.addFront(3)
        d.addFront(2)
        d.addFront(1)
        self.assertEqual(min_deque_to_array(d), [1, 2, 3])
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [1, 2])
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [1])
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [])
        self.assertIsNone(d.min())

    def test_5(self):
        d = DequeMin()
        d.addTail(2)
        d.addTail(2)
        d.addTail(1)
        d.addTail(1)
        self.assertEqual(min_deque_to_array(d), [2, 2, 1, 1])
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [2, 2, 1])
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [2, 2])
        self.assertEqual(d.min(), 2)

    def test_6(self):
        d = DequeMin()
        d.addFront(2)
        d.addTail(3)
        d.addFront(1)
        d.addTail(4)
        self.assertEqual(min_deque_to_array(d), [1, 2, 3, 4])
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [1, 2, 3])
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [1, 2])
        self.assertEqual(d.min(), 1)

    def test_7(self):
        d = DequeMin()
        d.addTail(-1)
        d.addTail(-2)
        d.addTail(0)
        self.assertEqual(min_deque_to_array(d), [-1, -2, 0])
        self.assertEqual(d.min(), -2)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [-1, -2])
        self.assertEqual(d.min(), -2)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [-1])
        self.assertEqual(d.min(), -1)

    def test_8(self):
        d = DequeMin()
        d.addFront(1)
        d.addFront(2)
        self.assertEqual(min_deque_to_array(d), [2, 1])
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [2])
        self.assertEqual(d.min(), 2)

    def test_9(self):
        d = DequeMin()
        d.addFront(1)
        d.addFront(2)
        self.assertEqual(min_deque_to_array(d), [2, 1])
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [2])
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [])
        self.assertIsNone(d.min())
        d.addTail(7)
        self.assertEqual(min_deque_to_array(d), [7])
        self.assertEqual(d.min(), 7)

    def test_10(self):
        d = DequeMin()
        d.addTail(3)
        d.addTail(2)
        d.addTail(1)
        self.assertEqual(min_deque_to_array(d), [3, 2, 1])
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [3, 2])
        self.assertEqual(d.min(), 2)
        d.removeTail()
        self.assertEqual(min_deque_to_array(d), [3])
        self.assertEqual(d.min(), 3)


class TestMinDequeSize(unittest.TestCase):

    def test_1(self):
        d = DequeMin()
        self.assertEqual(d.size(), 0)

    def test_2(self):
        d = DequeMin()
        d.addFront(1)
        self.assertEqual(d.size(), 1)
        d.addTail(2)
        self.assertEqual(d.size(), 2)

    def test_3(self):
        d = DequeMin()
        d.addFront(3)
        d.addFront(2)
        d.addFront(1)
        self.assertEqual(d.size(), 3)
        self.assertEqual(len(min_deque_to_array(d)), 3)

    def test_4(self):
        d = DequeMin()
        d.addTail(1)
        d.addTail(2)
        d.addTail(3)
        self.assertEqual(d.size(), 3)
        d.removeFront()
        self.assertEqual(d.size(), 2)
        d.removeTail()
        self.assertEqual(d.size(), 1)

    def test_5(self):
        d = DequeMin()
        d.addFront(1)
        d.addFront(2)
        d.addFront(3)
        self.assertEqual(d.size(), 3)
        d.removeFront()
        d.removeFront()
        d.removeFront()
        self.assertEqual(d.size(), 0)

    def test_6(self):
        d = DequeMin()
        d.addTail(1)
        d.addTail(2)
        self.assertEqual(d.size(), 2)
        d.removeTail()
        self.assertEqual(d.size(), 1)
        d.removeTail()
        self.assertEqual(d.size(), 0)

    def test_7(self):
        d = DequeMin()
        d.addFront(1)
        d.addTail(2)
        d.addFront(3)
        d.addTail(4)
        self.assertEqual(d.size(), 4)
        self.assertEqual(len(min_deque_to_array(d)), 4)

    def test_8(self):
        d = DequeMin()
        d.addFront(1)
        d.removeFront()
        self.assertEqual(d.size(), 0)
        d.addTail(2)
        self.assertEqual(d.size(), 1)

    def test_9(self):
        d = DequeMin()
        d.addTail(1)
        d.addTail(2)
        d.addTail(3)
        d.removeFront()
        self.assertEqual(d.size(), 2)
        d.removeFront()
        self.assertEqual(d.size(), 1)

    def test_10(self):
        d = DequeMin()
        d.addFront(5)
        d.addFront(4)
        d.addFront(3)
        d.addFront(2)
        d.addFront(1)
        self.assertEqual(d.size(), 5)
        d.removeTail()
        d.removeTail()
        self.assertEqual(d.size(), 3)


class TestMinDequeMin(unittest.TestCase):

    def test_0(self):
        d = DequeMin()
        d.addFront(3)
        d.addFront(2)
        d.addFront(1)
        d.addTail(4)
        d.addTail(5)
        d.addTail(6)
        self.assertEqual(d.min(), 1)
        d.removeFront()
        self.assertEqual(d.min(), 2)
        d.removeTail()
        d.removeTail()
        d.removeTail()
        self.assertEqual(d.min(), 2)
        d.removeTail()
        self.assertEqual(d.min(), 2)

    def test_1(self):
        d = DequeMin()
        d.addFront(3)
        d.addFront(2)
        d.addFront(1)
        d.addTail(4)
        d.addTail(5)
        self.assertEqual(d.min(), 1)
        d.removeFront()
        self.assertEqual(d.min(), 2)
        d.removeTail()
        self.assertEqual(d.min(), 2)

    def test_2(self):
        d = DequeMin()
        d.addFront(5)
        d.addFront(4)
        d.addFront(3)
        d.addFront(2)
        d.addFront(1)
        self.assertEqual(d.min(), 1)
        d.removeFront()
        self.assertEqual(d.min(), 2)
        d.removeFront()
        self.assertEqual(d.min(), 3)
        d.removeFront()
        d.removeFront()
        self.assertEqual(d.min(), 5)

    def test_3(self):
        d = DequeMin()
        d.addTail(1)
        d.addTail(2)
        d.addTail(3)
        d.addTail(4)
        d.addTail(5)
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(d.min(), 1)
        d.removeFront()
        self.assertEqual(d.min(), 2)

    def test_4(self):
        d = DequeMin()
        d.addFront(2)
        d.addFront(2)
        d.addTail(2)
        d.addTail(2)
        self.assertEqual(d.min(), 2)
        d.removeFront()
        self.assertEqual(d.min(), 2)
        d.removeTail()
        self.assertEqual(d.min(), 2)
        d.removeFront()
        d.removeTail()
        self.assertIsNone(d.min())

    def test_5(self):
        d = DequeMin()
        d.addFront(5)
        d.addFront(4)
        d.addFront(3)
        d.addFront(2)
        d.addFront(1)
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(d.min(), 1)
        d.removeFront()
        self.assertEqual(d.min(), 2)

    def test_6(self):
        d = DequeMin()
        d.addTail(5)
        d.addTail(4)
        d.addTail(3)
        d.addTail(2)
        d.addTail(1)
        self.assertEqual(d.min(), 1)
        self.assertEqual(d.removeFront(), 5)
        self.assertEqual(d.min(), 1)
        self.assertEqual(d.removeFront(), 4)
        self.assertEqual(d.min(), 1)

    def test_7(self):
        d = DequeMin()
        d.addFront(3)
        self.assertEqual(d.min(), 3)
        d.addTail(1)
        self.assertEqual(d.min(), 1)
        d.addFront(2)
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(d.min(), 2)
        d.removeFront()
        self.assertEqual(d.min(), 3)

    def test_8(self):
        d = DequeMin()
        d.addFront(10)
        self.assertEqual(d.min(), 10)
        d.removeTail()
        self.assertIsNone(d.min())
        d.addTail(7)
        self.assertEqual(d.min(), 7)

    def test_9(self):
        d = DequeMin()
        d.addTail(5)
        d.addTail(4)
        d.addTail(3)
        d.addTail(2)
        d.addTail(1)
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(d.min(), 2)
        d.removeTail()
        self.assertEqual(d.min(), 3)

    def test_10(self):
        d = DequeMin()
        d.addFront(1)
        d.addFront(2)
        d.addFront(3)
        d.addFront(4)
        self.assertEqual(d.min(), 1)
        d.removeFront()
        self.assertEqual(d.min(), 1)
        d.removeTail()
        self.assertEqual(d.min(), 2)


class TestDeque2(unittest.TestCase):

    def test_0(self):
        d = Deque2()

        self.assertEqual(d.INIT_CAPACITY, 4)
        self.assertEqual(d.capacity, 4)
        self.assertEqual(d.head_index, None)
        self.assertEqual(d.tail_index, None)
        self.assertEqual(d.size(), 0)

    def test_1(self):
        d = Deque2()

        self.assertEqual(d.removeTail(), None)

        self.assertEqual(d.INIT_CAPACITY, 4)
        self.assertEqual(d.capacity, 4)
        self.assertEqual(d.head_index, None)
        self.assertEqual(d.tail_index, None)
        self.assertEqual(d.size(), 0)

    def test_2(self):
        d = Deque2()

        self.assertEqual(d.removeFront(), None)

        self.assertEqual(d.INIT_CAPACITY, 4)
        self.assertEqual(d.capacity, 4)
        self.assertEqual(d.head_index, None)
        self.assertEqual(d.tail_index, None)
        self.assertEqual(d.size(), 0)

    def test_3(self):
        d = Deque2()

        d.addFront(1)
        d.addFront(2)
        d.addFront(3)
        d.addFront(4)
        d.addFront(5)
        d.addFront(6)
        d.addFront(7)
        d.addFront(8)
        d.addFront(9)
        d.addFront(10)

        self.assertEqual(d.INIT_CAPACITY, 4)
        self.assertEqual(d.capacity, 16)
        self.assertEqual(d.size(), 10)
        self.assertEqual(d.head_index, 14)
        self.assertEqual(d.tail_index, 7)

    def test_4(self):
        d = Deque2()

        d.addTail(1)
        d.addTail(2)
        d.addTail(3)
        d.addTail(4)
        d.addTail(5)
        d.addTail(6)
        d.addTail(7)
        d.addTail(8)
        d.addTail(9)
        d.addTail(10)

        self.assertEqual(d.INIT_CAPACITY, 4)
        self.assertEqual(d.capacity, 16)
        self.assertEqual(d.size(), 10)
        self.assertEqual(d.head_index, 0)
        self.assertEqual(d.tail_index, 9)

    def test_5(self):
        d = Deque2()

        d.addTail(1)
        d.addTail(2)
        d.addTail(3)

        self.assertEqual(d.size(), 3)
        self.assertEqual(d.removeFront(), 1)
        self.assertEqual(d.removeFront(), 2)
        self.assertEqual(d.removeFront(), 3)
        self.assertEqual(d.size(), 0)
        self.assertIsNone(d.head_index)
        self.assertIsNone(d.tail_index)

    def test_6(self):
        d = Deque2()

        d.addFront(1)
        d.addFront(2)
        d.addFront(3)

        self.assertEqual(d.size(), 3)
        self.assertEqual(d.removeFront(), 3)
        self.assertEqual(d.removeFront(), 2)
        self.assertEqual(d.removeFront(), 1)
        self.assertEqual(d.size(), 0)
        self.assertIsNone(d.head_index)
        self.assertIsNone(d.tail_index)

    def test_7(self):
        d = Deque2()

        d.addFront(1)
        d.addFront(2)
        d.addFront(3)

        self.assertEqual(d.size(), 3)
        self.assertEqual(d.removeTail(), 1)
        self.assertEqual(d.removeTail(), 2)
        self.assertEqual(d.removeTail(), 3)
        self.assertEqual(d.size(), 0)
        self.assertIsNone(d.head_index)
        self.assertIsNone(d.tail_index)

    def test_8(self):
        d = Deque2()

        d.addTail(1)
        d.addTail(2)
        d.addTail(3)

        self.assertEqual(d.size(), 3)
        self.assertEqual(d.removeTail(), 3)
        self.assertEqual(d.removeTail(), 2)
        self.assertEqual(d.removeTail(), 1)
        self.assertEqual(d.size(), 0)
        self.assertIsNone(d.head_index)
        self.assertIsNone(d.tail_index)

    def test_9(self):
        d = Deque2()

        d.addTail(1)
        d.addTail(2)
        d.addTail(3)
        d.addTail(4)

        self.assertEqual(d.removeFront(), 1)
        self.assertEqual(d.removeFront(), 2)

        d.addTail(5)
        d.addTail(6)

        self.assertEqual(d.size(), 4)
        self.assertEqual(d.removeFront(), 3)
        self.assertEqual(d.removeFront(), 4)
        self.assertEqual(d.removeFront(), 5)
        self.assertEqual(d.removeFront(), 6)
        self.assertEqual(d.size(), 0)
        self.assertIsNone(d.head_index)
        self.assertIsNone(d.tail_index)

    def test_10(self):
        d = Deque2()

        d.addFront(1)
        d.addFront(2)
        d.addFront(3)
        d.addFront(4)

        self.assertEqual(d.size(), 4)
        self.assertEqual(d.removeFront(), 4)
        self.assertEqual(d.removeFront(), 3)
        self.assertEqual(d.removeFront(), 2)
        self.assertEqual(d.removeFront(), 1)
        self.assertEqual(d.size(), 0)
        self.assertIsNone(d.head_index)
        self.assertIsNone(d.tail_index)

    def test_11(self):
        d = Deque2()

        d.addTail(1)
        d.addTail(2)
        d.addTail(3)
        d.addTail(4)
        d.addTail(5)
        d.addTail(6)

        self.assertEqual(d.capacity, 8)
        self.assertEqual(d.size(), 6)
        self.assertEqual(d.removeFront(), 1)
        self.assertEqual(d.removeFront(), 2)
        self.assertEqual(d.removeFront(), 3)
        self.assertEqual(d.removeFront(), 4)
        self.assertEqual(d.removeFront(), 5)
        self.assertEqual(d.removeFront(), 6)
        self.assertEqual(d.size(), 0)
        self.assertIsNone(d.head_index)
        self.assertIsNone(d.tail_index)

    def test_12(self):
        d = Deque2()

        d.addTail(1)
        d.addTail(2)
        d.addTail(3)
        d.addTail(4)

        self.assertEqual(d.removeFront(), 1)
        self.assertEqual(d.removeFront(), 2)

        d.addTail(5)
        d.addTail(6)
        d.addTail(7)

        self.assertEqual(d.capacity, 8)
        self.assertEqual(d.size(), 5)

        self.assertEqual(d.removeFront(), 3)
        self.assertEqual(d.removeFront(), 4)
        self.assertEqual(d.removeFront(), 5)
        self.assertEqual(d.removeFront(), 6)
        self.assertEqual(d.removeFront(), 7)

        self.assertEqual(d.size(), 0)
        self.assertIsNone(d.head_index)
        self.assertIsNone(d.tail_index)

    def test_13(self):
        d = Deque2()

        d.addTail(10)

        self.assertEqual(d.size(), 1)
        self.assertEqual(d.head_index, 0)
        self.assertEqual(d.tail_index, 0)
        self.assertEqual(d.head_index, d.tail_index)
        self.assertEqual(d.removeFront(), 10)
        self.assertEqual(d.size(), 0)
        self.assertIsNone(d.head_index)
        self.assertIsNone(d.tail_index)


def to_array(d):
    result = []
    node = d.head
    while node is not None:
        result.append(node.value)
        node = node.next
    return result


def min_deque_to_array(d):
    return list(reversed(d.front.stack)) + list(d.tail.stack)


def assert_order(testcase: unittest.TestCase, d):
    if d.head is None:
        testcase.assertIsNone(d.tail)
        return

    testcase.assertIsNone(d.head.prev)
    testcase.assertIsNone(d.tail.next)

    natural_order = []
    node = d.head
    prev = None
    while node is not None:
        natural_order.append(node.value)
        testcase.assertIs(node.prev, prev)
        if node.next is not None:
            testcase.assertIs(node.next.prev, node)
        prev = node
        node = node.next

    reversed_order = []
    node = d.tail
    nxt = None
    while node is not None:
        reversed_order.append(node.value)
        testcase.assertIs(node.next, nxt)
        if node.prev is not None:
            testcase.assertIs(node.prev.next, node)
        nxt = node
        node = node.prev

    testcase.assertEqual(reversed_order, list(reversed(natural_order)))
