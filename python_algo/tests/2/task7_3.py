import unittest

from task7 import Heap
from task7_2 import HeapWithFindMaxInRange, HeapWithFindLessThan, HeapWithMerge


class TestMakeHeap(unittest.TestCase):

    def test_1(self) -> None:
        heap = Heap()

        heap.MakeHeap([], 0)

        self.assertEqual(heap.HeapArray, [None])
        self.assertEqual(heap.Size, 0)

    def test_2(self) -> None:
        heap = Heap()

        heap.MakeHeap([], 2)

        self.assertEqual(heap.HeapArray, [None, None, None, None, None, None, None])
        self.assertEqual(heap.Size, 0)

    def test_3(self) -> None:
        heap = Heap()

        heap.MakeHeap([5], 0)

        self.assertEqual(heap.HeapArray, [5])
        self.assertEqual(heap.Size, 1)

    def test_4(self) -> None:
        heap = Heap()

        heap.MakeHeap([0], 1)

        self.assertEqual(heap.HeapArray, [0, None, None])
        self.assertEqual(heap.Size, 1)

    def test_5(self) -> None:
        heap = Heap()

        heap.MakeHeap([1, 2], 1)

        self.assertEqual(heap.HeapArray, [2, 1, None])
        self.assertEqual(heap.Size, 2)

    def test_6(self) -> None:
        heap = Heap()

        heap.MakeHeap([2, 7, 5], 1)

        self.assertEqual(heap.HeapArray, [7, 2, 5])
        self.assertEqual(heap.Size, 3)

    def test_7(self) -> None:
        heap = Heap()

        heap.MakeHeap([2, 5, 7], 1)

        self.assertEqual(heap.HeapArray, [7, 5, 2])
        self.assertEqual(heap.Size, 3)

    def test_8(self) -> None:
        heap = Heap()

        heap.MakeHeap([7, 6, 5, 4, 3, 2, 1], 2)

        self.assertEqual(heap.HeapArray, [7, 6, 5, 4, 3, 2, 1])
        self.assertEqual(heap.Size, 7)

    def test_9(self) -> None:
        heap = Heap()

        heap.MakeHeap([1, 2, 3, 4, 5, 6, 7], 2)

        self.assertEqual(heap.HeapArray, [7, 5, 6, 4, 2, 1, 3])
        self.assertEqual(heap.Size, 7)

    def test_10(self) -> None:
        heap = Heap()

        heap.MakeHeap([3, 1, 6, 5, 2, 4], 3)

        self.assertEqual(heap.HeapArray, [6, 5, 4, 1, 2, 3, None, None, None, None, None, None, None, None, None])
        self.assertEqual(heap.Size, 6)

    def test_11(self) -> None:
        heap = Heap()

        heap.MakeHeap([0, 5, 5, 0, 2, 5, 0], 2)

        self.assertEqual(heap.HeapArray, [5, 2, 5, 0, 0, 5, 0])
        self.assertEqual(heap.Size, 7)

    def test_12(self) -> None:
        heap = Heap()
        heap.MakeHeap([1, 2, 3, 4, 5, 6, 7], 2)

        heap.MakeHeap([2, 9], 1)

        self.assertEqual(heap.HeapArray, [9, 2, None])
        self.assertEqual(heap.Size, 2)

    def test_13(self) -> None:
        heap = Heap()
        heap.MakeHeap([1, 2, 3], 1)

        heap.MakeHeap([], 0)

        self.assertEqual(heap.HeapArray, [None])
        self.assertEqual(heap.Size, 0)


class TestGetMax(unittest.TestCase):

    def test_1(self) -> None:
        heap = Heap()

        self.assertEqual(heap.GetMax(), -1)
        self.assertEqual(heap.HeapArray, [])
        self.assertEqual(heap.Size, 0)

    def test_2(self) -> None:
        heap = Heap()
        heap.MakeHeap([], 1)

        self.assertEqual(heap.GetMax(), -1)
        self.assertEqual(heap.HeapArray, [None, None, None])
        self.assertEqual(heap.Size, 0)

    def test_3(self) -> None:
        heap = Heap()
        heap.MakeHeap([0], 0)

        self.assertEqual(heap.GetMax(), 0)
        self.assertEqual(heap.HeapArray, [None])
        self.assertEqual(heap.Size, 0)
        self.assertEqual(heap.GetMax(), -1)

    def test_4(self) -> None:
        heap = Heap()
        heap.MakeHeap([7, 5], 1)

        self.assertEqual(heap.GetMax(), 7)
        self.assertEqual(heap.HeapArray, [5, None, None])
        self.assertEqual(heap.Size, 1)

    def test_5(self) -> None:
        heap = Heap()
        heap.MakeHeap([9, 7, 8, 1], 2)

        self.assertEqual(heap.GetMax(), 9)
        self.assertEqual(heap.HeapArray, [8, 7, 1, None, None, None, None])
        self.assertEqual(heap.Size, 3)

    def test_6(self) -> None:
        heap = Heap()
        heap.MakeHeap([9, 8, 7, 6, 5, 4, 3], 2)

        self.assertEqual(heap.GetMax(), 9)
        self.assertEqual(heap.HeapArray, [8, 6, 7, 3, 5, 4, None])
        self.assertEqual(heap.Size, 6)

    def test_7(self) -> None:
        heap = Heap()
        heap.MakeHeap([5, 5, 0], 1)

        self.assertEqual(heap.GetMax(), 5)
        self.assertEqual(heap.GetMax(), 5)
        self.assertEqual(heap.GetMax(), 0)
        self.assertEqual(heap.GetMax(), -1)
        self.assertEqual(heap.HeapArray, [None, None, None])
        self.assertEqual(heap.Size, 0)

    def test_8(self) -> None:
        heap = Heap()
        heap.MakeHeap([2, 7, 1, 5, 3], 2)

        self.assertEqual(heap.GetMax(), 7)
        self.assertEqual(heap.GetMax(), 5)
        self.assertEqual(heap.GetMax(), 3)
        self.assertEqual(heap.GetMax(), 2)
        self.assertEqual(heap.GetMax(), 1)
        self.assertEqual(heap.GetMax(), -1)
        self.assertEqual(heap.HeapArray, [None, None, None, None, None, None, None])
        self.assertEqual(heap.Size, 0)


class TestAdd(unittest.TestCase):

    def test_1(self) -> None:
        heap = Heap()

        self.assertFalse(heap.Add(5))
        self.assertEqual(heap.HeapArray, [])
        self.assertEqual(heap.Size, 0)

    def test_2(self) -> None:
        heap = Heap()
        heap.MakeHeap([], 0)

        self.assertTrue(heap.Add(0))
        self.assertEqual(heap.HeapArray, [0])
        self.assertEqual(heap.Size, 1)

    def test_3(self) -> None:
        heap = Heap()
        heap.MakeHeap([5], 0)

        self.assertFalse(heap.Add(9))
        self.assertEqual(heap.HeapArray, [5])
        self.assertEqual(heap.Size, 1)

    def test_4(self) -> None:
        heap = Heap()
        heap.MakeHeap([9, 7, 8], 2)

        self.assertTrue(heap.Add(1))
        self.assertEqual(heap.HeapArray, [9, 7, 8, 1, None, None, None])
        self.assertEqual(heap.Size, 4)

    def test_5(self) -> None:
        heap = Heap()
        heap.MakeHeap([10, 8, 9], 2)

        self.assertTrue(heap.Add(20))
        self.assertEqual(heap.HeapArray, [20, 10, 9, 8, None, None, None])
        self.assertEqual(heap.Size, 4)

    def test_6(self) -> None:
        heap = Heap()
        heap.MakeHeap([10, 8, 9], 2)

        self.assertTrue(heap.Add(9))
        self.assertEqual(heap.HeapArray, [10, 9, 9, 8, None, None, None])
        self.assertEqual(heap.Size, 4)

    def test_7(self) -> None:
        heap = Heap()
        heap.MakeHeap([5], 1)

        self.assertTrue(heap.Add(5))
        self.assertEqual(heap.HeapArray, [5, 5, None])
        self.assertEqual(heap.Size, 2)

    def test_8(self) -> None:
        heap = Heap()
        heap.MakeHeap([], 1)

        self.assertTrue(heap.Add(1))
        self.assertTrue(heap.Add(2))
        self.assertTrue(heap.Add(3))
        self.assertFalse(heap.Add(4))
        self.assertEqual(heap.HeapArray, [3, 1, 2])
        self.assertEqual(heap.Size, 3)

    def test_9(self) -> None:
        heap = Heap()
        heap.MakeHeap([7, 5, 6], 1)

        self.assertEqual(heap.GetMax(), 7)
        self.assertTrue(heap.Add(9))
        self.assertEqual(heap.HeapArray, [9, 5, 6])
        self.assertEqual(heap.Size, 3)
        self.assertEqual(heap.GetMax(), 9)
        self.assertEqual(heap.GetMax(), 6)
        self.assertEqual(heap.GetMax(), 5)
        self.assertEqual(heap.GetMax(), -1)

    def test_10(self) -> None:
        heap = Heap()
        heap.MakeHeap([5], 0)

        self.assertEqual(heap.GetMax(), 5)
        self.assertTrue(heap.Add(3))
        self.assertEqual(heap.HeapArray, [3])
        self.assertEqual(heap.Size, 1)
        self.assertEqual(heap.GetMax(), 3)
        self.assertEqual(heap.Size, 0)


class TestIsHeap(unittest.TestCase):

    def test_1(self) -> None:
        heap = Heap()

        self.assertTrue(heap.IsHeap())

    def test_2(self) -> None:
        heap = Heap()
        heap.MakeHeap([], 2)

        self.assertTrue(heap.IsHeap())

    def test_3(self) -> None:
        heap = Heap()
        heap.MakeHeap([0], 0)

        self.assertTrue(heap.IsHeap())

    def test_4(self) -> None:
        heap = Heap()
        heap.HeapArray = [9, 7, 8, 3, 5, 0, 6]
        heap.Size = 7

        self.assertTrue(heap.IsHeap())

    def test_5(self) -> None:
        heap = Heap()
        heap.HeapArray = [5, 5, 0, None, None, None, None]
        heap.Size = 3

        self.assertTrue(heap.IsHeap())

    def test_6(self) -> None:
        heap = Heap()
        heap.HeapArray = [5, 6, 1]
        heap.Size = 3

        self.assertFalse(heap.IsHeap())

    def test_7(self) -> None:
        heap = Heap()
        heap.HeapArray = [5, 1, 6]
        heap.Size = 3

        self.assertFalse(heap.IsHeap())

    def test_8(self) -> None:
        heap = Heap()
        heap.HeapArray = [9, 7, 8, 3, 10, 0, 6]
        heap.Size = 7

        self.assertFalse(heap.IsHeap())

    def test_9(self) -> None:
        heap = Heap()
        heap.HeapArray = [9, 7, 8, 3, 5, 0, 10]
        heap.Size = 7

        self.assertFalse(heap.IsHeap())

    def test_10(self) -> None:
        heap = Heap()
        heap.HeapArray = [5, None, 1]
        heap.Size = 3

        self.assertFalse(heap.IsHeap())

    def test_11(self) -> None:
        heap = Heap()
        heap.HeapArray = [None, 1, None]
        heap.Size = 2

        self.assertFalse(heap.IsHeap())

    def test_12(self) -> None:
        heap = Heap()
        heap.HeapArray = [5, None, 0]
        heap.Size = 1

        self.assertFalse(heap.IsHeap())

    def test_13(self) -> None:
        heap = Heap()
        heap.HeapArray = [5]
        heap.Size = 0

        self.assertFalse(heap.IsHeap())

    def test_14(self) -> None:
        heap = Heap()
        heap.HeapArray = [5]
        heap.Size = -1

        self.assertFalse(heap.IsHeap())

    def test_15(self) -> None:
        heap = Heap()
        heap.HeapArray = [5]
        heap.Size = 2

        self.assertFalse(heap.IsHeap())

    def test_16(self) -> None:
        heap = Heap()
        heap.MakeHeap([1, 5, 3], 2)

        self.assertTrue(heap.IsHeap())
        self.assertTrue(heap.Add(7))
        self.assertTrue(heap.IsHeap())
        self.assertEqual(heap.GetMax(), 7)
        self.assertTrue(heap.IsHeap())

    def test_17(self) -> None:
        heap = Heap()
        heap.MakeHeap([5], 0)

        self.assertEqual(heap.GetMax(), 5)
        self.assertTrue(heap.IsHeap())


class TestFindMaxInRange(unittest.TestCase):

    def test_1(self) -> None:
        heap = HeapWithFindMaxInRange()

        self.assertEqual(heap.FindMaxInRange(0, 10), -1)

    def test_2(self) -> None:
        heap = HeapWithFindMaxInRange()
        heap.MakeHeap([], 2)

        self.assertEqual(heap.FindMaxInRange(0, 10), -1)

    def test_3(self) -> None:
        heap = HeapWithFindMaxInRange()
        heap.MakeHeap([5], 0)

        self.assertEqual(heap.FindMaxInRange(5, 5), 5)

    def test_4(self) -> None:
        heap = HeapWithFindMaxInRange()
        heap.MakeHeap([9, 7, 8, 3, 5, 0, 6], 2)

        self.assertEqual(heap.FindMaxInRange(0, 10), 9)

    def test_5(self) -> None:
        heap = HeapWithFindMaxInRange()
        heap.MakeHeap([9, 7, 8, 3, 5, 0, 6], 2)

        self.assertEqual(heap.FindMaxInRange(5, 8), 8)

    def test_6(self) -> None:
        heap = HeapWithFindMaxInRange()
        heap.MakeHeap([9, 8, 7, 3, 5, 0, 6], 2)

        self.assertEqual(heap.FindMaxInRange(5, 8), 8)

    def test_7(self) -> None:
        heap = HeapWithFindMaxInRange()
        heap.MakeHeap([9, 7, 8, 3, 5, 0, 6], 2)

        self.assertEqual(heap.FindMaxInRange(5, 6), 6)

    def test_8(self) -> None:
        heap = HeapWithFindMaxInRange()
        heap.MakeHeap([9, 7, 8, 3, 5, 0, 6], 2)

        self.assertEqual(heap.FindMaxInRange(10, 20), -1)

    def test_9(self) -> None:
        heap = HeapWithFindMaxInRange()
        heap.MakeHeap([9, 7, 8, 3, 5, 0, 6], 2)

        self.assertEqual(heap.FindMaxInRange(4, 4), -1)

    def test_10(self) -> None:
        heap = HeapWithFindMaxInRange()
        heap.MakeHeap([0], 0)

        self.assertEqual(heap.FindMaxInRange(0, 0), 0)

    def test_11(self) -> None:
        heap = HeapWithFindMaxInRange()
        heap.MakeHeap([5, 5, 0], 1)

        self.assertEqual(heap.FindMaxInRange(5, 5), 5)

    def test_12(self) -> None:
        heap = HeapWithFindMaxInRange()
        heap.MakeHeap([9, 7], 2)

        self.assertEqual(heap.FindMaxInRange(0, 7), 7)

    def test_13(self) -> None:
        heap = HeapWithFindMaxInRange()
        heap.MakeHeap([5], 0)

        self.assertEqual(heap.FindMaxInRange(0, 4), -1)

    def test_14(self) -> None:
        heap = HeapWithFindMaxInRange()
        heap.MakeHeap([9, 7, 8], 1)

        self.assertEqual(heap.FindMaxInRange(8, 5), -1)


class TestFindLessThan(unittest.TestCase):

    def test_1(self) -> None:
        heap = HeapWithFindLessThan()

        self.assertEqual(heap.FindLessThan(10), -1)

    def test_2(self) -> None:
        heap = HeapWithFindLessThan()
        heap.MakeHeap([], 2)

        self.assertEqual(heap.FindLessThan(10), -1)

    def test_3(self) -> None:
        heap = HeapWithFindLessThan()
        heap.MakeHeap([5], 0)

        self.assertEqual(heap.FindLessThan(6), 5)

    def test_4(self) -> None:
        heap = HeapWithFindLessThan()
        heap.MakeHeap([5], 0)

        self.assertEqual(heap.FindLessThan(5), -1)

    def test_5(self) -> None:
        heap = HeapWithFindLessThan()
        heap.MakeHeap([5], 0)

        self.assertEqual(heap.FindLessThan(4), -1)

    def test_6(self) -> None:
        heap = HeapWithFindLessThan()
        heap.MakeHeap([0], 1)

        self.assertEqual(heap.FindLessThan(1), 0)
        self.assertEqual(heap.FindLessThan(0), -1)
        self.assertEqual(heap.FindLessThan(-1), -1)

    def test_7(self) -> None:
        heap = HeapWithFindLessThan()
        heap.MakeHeap([9, 3], 1)

        self.assertEqual(heap.FindLessThan(4), 3)

    def test_8(self) -> None:
        heap = HeapWithFindLessThan()
        heap.MakeHeap([9, 8, 7, 1], 2)

        self.assertEqual(heap.FindLessThan(5), 1)

    def test_9(self) -> None:
        heap = HeapWithFindLessThan()
        heap.MakeHeap([9, 8, 7, 6, 5, 4, 0], 2)

        self.assertEqual(heap.FindLessThan(1), 0)

    def test_10(self) -> None:
        heap = HeapWithFindLessThan()
        heap.MakeHeap([9, 8, 7, 6, 5, 4, 3], 2)

        self.assertEqual(heap.FindLessThan(3), -1)

    def test_11(self) -> None:
        heap = HeapWithFindLessThan()
        heap.MakeHeap([5, 5, 5], 1)

        self.assertEqual(heap.FindLessThan(6), 5)
        self.assertEqual(heap.FindLessThan(5), -1)

    def test_12(self) -> None:
        heap = HeapWithFindLessThan()
        heap.MakeHeap([9, 8, 7, 3, 5], 3)

        self.assertIn(heap.FindLessThan(6), [3, 5])


class TestMerge(unittest.TestCase):

    def test_1(self) -> None:
        heap = HeapWithMerge()
        other = Heap()

        heap.Merge(other)

        self.assertEqual(heap.Size, 0)
        self.assertEqual(other.Size, 0)
        self.assertTrue(heap.IsHeap())
        self.assertTrue(other.IsHeap())
        self.assertEqual(heap.GetMax(), -1)

    def test_2(self) -> None:
        heap = HeapWithMerge()
        heap.MakeHeap([], 1)
        other = Heap()
        other.MakeHeap([], 2)

        heap.Merge(other)

        self.assertEqual(heap.HeapArray, [None, None, None])
        self.assertEqual(heap.Size, 0)
        self.assertEqual(other.Size, 0)
        self.assertTrue(heap.IsHeap())
        self.assertTrue(other.IsHeap())

    def test_3(self) -> None:
        heap = HeapWithMerge()
        other = Heap()
        other.MakeHeap([5], 0)

        heap.Merge(other)

        self.assertEqual(heap.HeapArray, [5])
        self.assertEqual(heap.Size, 1)
        self.assertEqual(other.Size, 0)
        self.assertTrue(heap.IsHeap())
        self.assertTrue(other.IsHeap())
        self.assertEqual(heap.GetMax(), 5)
        self.assertEqual(heap.GetMax(), -1)
        self.assertEqual(other.GetMax(), -1)

    def test_4(self) -> None:
        heap = HeapWithMerge()
        heap.MakeHeap([7, 3, 5], 1)
        other = Heap()

        heap.Merge(other)

        self.assertEqual(heap.HeapArray, [7, 3, 5])
        self.assertEqual(heap.Size, 3)
        self.assertTrue(heap.IsHeap())
        self.assertTrue(other.IsHeap())

    def test_5(self) -> None:
        heap = HeapWithMerge()
        heap.MakeHeap([5], 0)
        other = Heap()
        other.MakeHeap([9], 0)

        heap.Merge(other)

        self.assertEqual(heap.HeapArray, [9, 5, None])
        self.assertEqual(heap.Size, 2)
        self.assertEqual(other.Size, 0)
        self.assertTrue(heap.IsHeap())
        self.assertTrue(other.IsHeap())
        self.assertEqual(heap.GetMax(), 9)
        self.assertEqual(heap.GetMax(), 5)
        self.assertEqual(heap.GetMax(), -1)

    def test_6(self) -> None:
        heap = HeapWithMerge()
        heap.MakeHeap([7, 3], 2)
        other = Heap()
        other.MakeHeap([8, 5], 1)

        heap.Merge(other)

        self.assertEqual(len(heap.HeapArray), 7)
        self.assertEqual(heap.Size, 4)
        self.assertEqual(other.Size, 0)
        self.assertTrue(heap.IsHeap())
        self.assertTrue(other.IsHeap())
        self.assertEqual(heap.GetMax(), 8)
        self.assertEqual(heap.GetMax(), 7)
        self.assertEqual(heap.GetMax(), 5)
        self.assertEqual(heap.GetMax(), 3)
        self.assertEqual(heap.GetMax(), -1)

    def test_7(self) -> None:
        heap = HeapWithMerge()
        heap.MakeHeap([5, 5, 0], 1)
        other = Heap()
        other.MakeHeap([5, 0, 0], 1)

        heap.Merge(other)

        self.assertEqual(heap.Size, 6)
        self.assertEqual(other.Size, 0)
        self.assertTrue(heap.IsHeap())
        self.assertTrue(other.IsHeap())
        self.assertEqual(heap.GetMax(), 5)
        self.assertEqual(heap.GetMax(), 5)
        self.assertEqual(heap.GetMax(), 5)
        self.assertEqual(heap.GetMax(), 0)
        self.assertEqual(heap.GetMax(), 0)
        self.assertEqual(heap.GetMax(), 0)
        self.assertEqual(heap.GetMax(), -1)

    def test_8(self) -> None:
        heap = HeapWithMerge()
        heap.MakeHeap([0], 0)
        other = Heap()
        other.MakeHeap([7, 6, 5, 4, 3, 2, 1], 2)

        heap.Merge(other)

        self.assertEqual(len(heap.HeapArray), 15)
        self.assertEqual(heap.Size, 8)
        self.assertEqual(other.Size, 0)
        self.assertTrue(heap.IsHeap())
        self.assertTrue(other.IsHeap())
        self.assertEqual(heap.GetMax(), 7)
        self.assertEqual(heap.GetMax(), 6)
        self.assertEqual(heap.GetMax(), 5)
        self.assertEqual(heap.GetMax(), 4)
        self.assertEqual(heap.GetMax(), 3)
        self.assertEqual(heap.GetMax(), 2)
        self.assertEqual(heap.GetMax(), 1)
        self.assertEqual(heap.GetMax(), 0)
        self.assertEqual(heap.GetMax(), -1)

    def test_9(self) -> None:
        heap = HeapWithMerge()
        heap.MakeHeap([2], 0)
        other = Heap()
        other.MakeHeap([5], 0)
        third = Heap()
        third.MakeHeap([3], 0)

        heap.Merge(other)
        heap.Merge(other)
        heap.Merge(third)

        self.assertEqual(heap.Size, 3)
        self.assertEqual(other.Size, 0)
        self.assertEqual(third.Size, 0)
        self.assertTrue(heap.IsHeap())
        self.assertTrue(other.IsHeap())
        self.assertTrue(third.IsHeap())
        self.assertEqual(heap.GetMax(), 5)
        self.assertEqual(heap.GetMax(), 3)
        self.assertEqual(heap.GetMax(), 2)
        self.assertEqual(heap.GetMax(), -1)