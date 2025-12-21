import unittest

from task3 import DynArray
from task3_2 import DynArrayBank, MultiDynArray, DynArray2

def make_arr(n: int):
    a = DynArray()
    for i in range(n):
        a.append(i)
    return a

def make_arr_bank(n: int):
    a = DynArrayBank()
    for i in range(n):
        a.append(i)
    return a


class TestDynArrayInsert(unittest.TestCase):

    def assert_content_equals(self, arr: DynArray, expected):
        self.assertEqual(len(arr), len(expected))
        self.assertEqual(len(arr), arr.count)
        for i in range(arr.count):
            self.assertEqual(arr[i], expected[i])

    def test_1(self):
        a = DynArray()
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        a.insert(0, 1)
        self.assert_content_equals(a, [1])
        self.assertEqual(len(a), old_len + 1)
        self.assertEqual(a.count, old_count + 1)
        self.assertEqual(a.capacity, old_capacity)

    def test_2(self):
        a = DynArray()
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        a.insert(len(a), 1)
        self.assert_content_equals(a, [1])
        self.assertEqual(len(a), old_len + 1)
        self.assertEqual(a.count, old_count + 1)
        self.assertEqual(a.capacity, old_capacity)

    def test_3(self):
        a = make_arr(5)
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        a.insert(0, 999)
        self.assert_content_equals(a, [999, 0, 1, 2, 3, 4])
        self.assertEqual(len(a), old_len + 1)
        self.assertEqual(a.count, old_count + 1)
        self.assertEqual(a.capacity, old_capacity)

    def test_4(self):
        a = make_arr(5)
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        a.insert(1, 999)
        self.assert_content_equals(a, [0, 999, 1, 2, 3, 4])
        self.assertEqual(len(a), old_len + 1)
        self.assertEqual(a.count, old_count + 1)
        self.assertEqual(a.capacity, old_capacity)

    def test_5(self):
        a = make_arr(4)
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        a.insert(2, 999)
        self.assert_content_equals(a, [0, 1, 999, 2, 3])
        self.assertEqual(len(a), old_len + 1)
        self.assertEqual(a.count, old_count + 1)
        self.assertEqual(a.capacity, old_capacity)

    def test_6(self):
        a = make_arr(5)
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        a.insert(4, 999)
        self.assert_content_equals(a, [0, 1, 2, 3, 999, 4])
        self.assertEqual(len(a), old_len + 1)
        self.assertEqual(a.count, old_count + 1)
        self.assertEqual(a.capacity, old_capacity)

    def test_7(self):
        a = make_arr(5)
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        a.insert(len(a), 999)
        self.assert_content_equals(a, [0, 1, 2, 3, 4, 999])
        self.assertEqual(len(a), old_len + 1)
        self.assertEqual(a.count, old_count + 1)
        self.assertEqual(a.capacity, old_capacity)

    def test_8(self):
        a = make_arr(5)
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        with self.assertRaises(IndexError):
            a.insert(-1, 100)
        self.assert_content_equals(a, [0, 1, 2, 3, 4])
        self.assertEqual(len(a), old_len)
        self.assertEqual(a.count, old_count)
        self.assertEqual(a.capacity, old_capacity)

    def test_9(self):
        a = make_arr(5)
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        with self.assertRaises(IndexError):
            a.insert(6, 100)
        self.assert_content_equals(a, [0, 1, 2, 3, 4])
        self.assertEqual(len(a), old_len)
        self.assertEqual(a.count, old_count)
        self.assertEqual(a.capacity, 16)
        self.assertEqual(a.capacity, old_capacity)

    def test_10(self):
        a = make_arr(7)
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        a.insert(3, "x")
        self.assertEqual(len(a), old_len + 1)
        self.assertEqual(a.count, old_count + 1)
        self.assertEqual(a.capacity, old_capacity)

    def test_11(self):
        a = make_arr(16)
        a.insert(8, 999)

        self.assertEqual(a.capacity, 32)
        self.assertEqual(len(a), 17)
        self.assertEqual(a.count, 17)

        expected = list(range(16))
        expected.insert(8, 999)
        self.assert_content_equals(a, expected)

    def test_12(self):
        a = DynArray()
        a.insert(0, 0)
        a.insert(1, 2)
        a.insert(1, 1)
        a.insert(len(a), 3)
        self.assert_content_equals(a, [0, 1, 2, 3])


        a = make_arr(5)
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        with self.assertRaises(IndexError):
            a.insert(-1, 100)
        self.assert_content_equals(a, [0, 1, 2, 3, 4])
        self.assertEqual(len(a), old_len)
        self.assertEqual(a.count, old_count)
        self.assertEqual(a.capacity, old_capacity)

class TestDynArrayDelete(unittest.TestCase):

    def assert_content_equals(self, arr: DynArray, expected):
        self.assertEqual(len(arr), len(expected))
        self.assertEqual(len(arr), arr.count)
        for i in range(arr.count):
            self.assertEqual(arr[i], expected[i])

    def test_1(self):
        a = make_arr(3)
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        with self.assertRaises(IndexError):
            a.delete(-1)
        self.assertEqual(len(a), old_len)
        self.assertEqual(a.count, old_count)
        self.assertEqual(a.capacity, old_capacity)

    def test_2(self):
        a = make_arr(3)
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        with self.assertRaises(IndexError):
            a.delete(3)
        self.assertEqual(len(a), old_len)
        self.assertEqual(a.count, old_count)
        self.assertEqual(a.capacity, old_capacity)

    def test_3(self):
        a = make_arr(5)
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        a.delete(0)
        self.assert_content_equals(a, [1, 2, 3, 4])
        self.assertEqual(len(a), old_len - 1)
        self.assertEqual(a.count, old_count - 1)
        self.assertEqual(a.capacity, old_capacity)

    def test_4(self):
        a = make_arr(5)
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        a.delete(1)
        self.assert_content_equals(a, [0, 2, 3, 4])
        self.assertEqual(len(a), old_len - 1)
        self.assertEqual(a.count, old_count - 1)
        self.assertEqual(a.capacity, old_capacity)

    def test_5(self):
        a = make_arr(5)
        old_len = len(a)
        old_count = a.count
        old_capacity = a.capacity
        a.delete(4)
        self.assert_content_equals(a, [0, 1, 2, 3])
        self.assertEqual(len(a), old_len - 1)
        self.assertEqual(a.count, old_count - 1)
        self.assertEqual(a.capacity, old_capacity)

    def test_6(self):
        a = make_arr(3)
        old_capacity = a.capacity
        a.delete(0)
        a.delete(0)
        a.delete(0)
        self.assertEqual(len(a), 0)
        with self.assertRaises(IndexError):
            a.delete(0)
        self.assertEqual(len(a), 0)
        self.assertEqual(a.count, 0)
        self.assertEqual(a.capacity, old_capacity)

    def test_7(self):
        a = make_arr(9)
        self.assertEqual(a.capacity, 16)

        a.delete(0)
        self.assertEqual(len(a), 8)
        self.assertEqual(a.count, 8)
        self.assertEqual(a.capacity, 16)

    def test_8(self):
        a = make_arr(9)
        self.assertEqual(a.capacity, 16)

        a.delete(0)
        a.delete(0)
        self.assertEqual(len(a), 7)
        self.assertEqual(a.count, 7)
        self.assertEqual(a.capacity, 16)

    def test_9(self):
        a = make_arr(17)
        self.assertEqual(a.capacity, 32)
        self.assertEqual(len(a), 17)

        a.delete(0)
        self.assertEqual(len(a), 16)
        self.assertEqual(a.capacity, 32)

        a.delete(0)
        self.assertEqual(len(a), 15)
        self.assertEqual(a.capacity, 21)

        self.assert_content_equals(a, list(range(2, 17)))

    def test_10(self):
        a = DynArray()
        a.resize(24)
        for i in range(13):
            a.append(i)

        self.assertEqual(a.capacity, 24)
        self.assertEqual(len(a), 13)

        a.delete(0)
        self.assertEqual(a.capacity, 24)
        self.assertEqual(len(a), 12)

        a.delete(0)
        self.assertEqual(a.capacity, 16)
        self.assertEqual(len(a), 11)

        self.assert_content_equals(a, list(range(2, 13)))

    def test_11(self):
        a = DynArray()
        a.resize(17)
        for i in range(3):
            a.append(i)

        self.assertEqual(a.capacity, 17)
        self.assertEqual(len(a), 3)

        a.delete(0)
        self.assertEqual(a.capacity, 16)
        self.assertEqual(len(a), 2)

        a.delete(0)
        self.assertEqual(a.capacity, 16)
        self.assertEqual(len(a), 1)

        a.delete(0)
        self.assertEqual(a.capacity, 16)
        self.assertEqual(len(a), 0)

class TestBankDynArray(unittest.TestCase):

    def test_1(self):
        a = make_arr_bank(8)
        self.assertEqual(a.capacity, a.MIN_CAPACITY)

        self.assertGreaterEqual(a.get_credits(), 0)

        a.delete(0)

        self.assertEqual(a.capacity, a.MIN_CAPACITY)
        self.assertEqual(len(a), 7)
        self.assertGreaterEqual(a.get_credits(), 0)

    def test_2(self):
        a = make_arr_bank(9)
        self.assertEqual(a.capacity, 16)

        self.assertGreaterEqual(a.get_credits(), 0)

        a.delete(0)

        self.assertEqual(a.capacity, 16)
        self.assertEqual(len(a), 8)
        self.assertGreaterEqual(a.get_credits(), 0)

    def test_3(self):
        a = make_arr_bank(17)
        self.assertEqual(a.capacity, 32)
        self.assertEqual(len(a), 17)
        self.assertGreaterEqual(a.get_credits(), 0)

        a.delete(0)
        self.assertEqual(a.capacity, 32)
        self.assertEqual(len(a), 16)
        self.assertGreaterEqual(a.get_credits(), 0)

        credits_before_resize = a.get_credits()
        a.delete(0)

        self.assertEqual(a.capacity, 21)
        self.assertEqual(len(a), 15)

        self.assertGreaterEqual(a.get_credits(), 0)
        self.assertLessEqual(a.get_credits(), credits_before_resize)

    def test_4(self):
        a = make_arr_bank(17)
        self.assertEqual(a.capacity, 32)

        a.delete(0)
        self.assertEqual(len(a), 16)
        self.assertEqual(a.capacity, 32)
        self.assertGreaterEqual(a.get_credits(), 0)

        credits_before = a.get_credits()
        a.delete(0)

        self.assertGreaterEqual(a.get_credits(), 0)
        self.assertLessEqual(a.get_credits(), credits_before)


class TestMultiDynArrayInit(unittest.TestCase):
    
    def test_1(self):
        with self.assertRaises(Exception):
            MultiDynArray([])

    def test_2(self):
        with self.assertRaises(Exception):
            MultiDynArray([0])

    def test_3(self):
        with self.assertRaises(Exception):
            MultiDynArray([3, 0, 5])

    def test_4(self):
        with self.assertRaises(Exception):
            MultiDynArray([-1, 2])
    
    
    def test_5(self):
        a = MultiDynArray([4])
    
        assert a.dimensions == 1
        assert len(a._root) == 0
        assert a._root.capacity == 4
        assert a._root.count == 0
    
    def test_6(self):
        a = MultiDynArray([2, 5])
    
        assert a.dimensions == 2
        assert len(a._root) == 2
        assert a._root.capacity == 2
        assert a._root.count == 2

        level1_0 = a._root[0]
        level1_1 = a._root[1]
    
        assert isinstance(level1_0, DynArray2)
        assert isinstance(level1_1, DynArray2)
    
        assert level1_0.capacity == 5
        assert level1_1.capacity == 5
    
        assert len(level1_0) == 0
        assert level1_0.count == 0
        assert len(level1_1) == 0
        assert level1_1.count == 0
    
    def test_7(self):
        a = MultiDynArray([2, 3, 5])
    
        assert a.dimensions == 3
        assert len(a._root) == 2
        assert a._root.capacity == 2
        assert a._root.count == 2

        level1_0 = a._root[0]
        level1_1 = a._root[1]
    
        assert isinstance(level1_0, DynArray2)
        assert isinstance(level1_1, DynArray2)
    
        assert len(level1_0) == 3
        assert level1_0.count == 3
        assert len(level1_1) == 3
        assert level1_1.count == 3
        assert level1_0.capacity == 3
        assert level1_1.capacity == 3
    
        level_1_0_2_0 = level1_0[0]
        level_1_0_2_2 = level1_0[2]

        assert isinstance(level_1_0_2_0, DynArray2)
        assert level_1_0_2_0.capacity == 5
        assert len(level_1_0_2_0) == 0

        assert isinstance(level_1_0_2_2, DynArray2)
        assert level_1_0_2_2.capacity == 5
        assert len(level_1_0_2_2) == 0
    
    
    def test_8(self):
        a = MultiDynArray([2, 3, 5])

        assert a._root[0] is not a._root[1]
        assert a._root[0][0] is not a._root[0][1]
        assert a._root[0][0] is not a._root[1][0]

class TestMultiDynArrayAppend(unittest.TestCase):

    def test_1(self):
        a = MultiDynArray([2, 5])

        a.append((1,), 10)
        a.append((1,), 20)

        assert a[1, 0] == 10
        assert a[1, 1] == 20

    def test_2(self):
        a = MultiDynArray([2, 3, 5])

        a.append((1, 2), 1)
        a.append((1, 2), 2)

        assert a[1, 2, 0] == 1
        assert a[1, 2, 1] == 2

    def test_3(self):
        a = MultiDynArray([2, 3, 5])

        a.append((0, 0), 1)
        a.append((0, 1), 2)

        assert a[0, 0, 0] == 1
        assert a[0, 1, 0] == 2

        with self.assertRaises(Exception):
            _ = a[0, 0, 1]

    def test_4(self):
        a = MultiDynArray([2, 3, 5])
        a.append((1, 2), 1)

        assert a[1, 2, 0] == 1
        with self.assertRaises(Exception):
            _ = a[1, 2, 1]

    def test_5(self):
        a = MultiDynArray([2, 3, 5])

        with self.assertRaises(Exception):
            a.append((0,), 123)

    def test_6(self):
        a = MultiDynArray([2, 3, 5])

        child = DynArray2(3)
        a.append((), child)
        assert a._root.count == 3

    def test_7(self):
        a = MultiDynArray([2, 3, 5])

        child = DynArray2(3)
        a.append(0, child)
        assert a._root[0].count == 4

class TestMultiDynArrayInsert(unittest.TestCase):

    def test_1(self):
        a = MultiDynArray([2, 3, 5])

        a.append((1, 2), 10)
        a.append((1, 2), 30)

        a.insert((1, 2, 1), 20)

        assert a[1, 2, 0] == 10
        assert a[1, 2, 1] == 20
        assert a[1, 2, 2] == 30


    def test_2(self):
        a = MultiDynArray([2, 3, 5])

        a.insert((0, 0, 0), 1)

        assert a[0, 0, 0] == 1


    def test_3(self):
        a = MultiDynArray([2, 3, 5])

        with self.assertRaises(Exception):
            a.insert((0, 0, 1), 1)


    def test_4(self):
        a = MultiDynArray([2, 3, 5])

        with self.assertRaises(Exception):
            a.insert((10, 7, 0), 1)


    def test_5(self):
        a = MultiDynArray([2, 3, 5])

        a.insert((0, 0, 0), 1)
        a.insert((0, 1, 0), 2)

        assert a[0, 0, 0] == 1
        assert a[0, 1, 0] == 2

        with self.assertRaises(Exception):
            _ = a[0, 0, 1]


    def test_6(self):
        a = MultiDynArray([2, 3, 5])

        a.append((1, 1), 1)
        a.append((1, 1), 2)
        a.append((1, 1), 4)

        a.insert((1, 1, 2), 3)

        assert a[1, 1, 0] == 1
        assert a[1, 1, 1] == 2
        assert a[1, 1, 2] == 3
        assert a[1, 1, 3] == 4

    def test_7(self):
        a = MultiDynArray([2, 3, 5])

        child = DynArray2(3)
        a.insert(2, child)
        assert a._root.count == 3

class TestMultiDynArrayDelete(unittest.TestCase):

    def test_1(self):
        a = MultiDynArray([2, 3, 5])

        a.append((1, 2), 10)
        a.append((1, 2), 20)
        a.append((1, 2), 30)

        a.delete((1, 2, 1))

        assert a[1, 2, 0] == 10
        assert a[1, 2, 1] == 30
        with self.assertRaises(Exception):
            _ = a[1, 2, 2]


    def test_2(self):
        a = MultiDynArray([2, 3, 5])

        a.append((0, 0), "a")
        a.append((0, 0), "b")
        a.append((0, 0), "c")

        a.delete((0, 0, 0))

        assert a[0, 0, 0] == "b"
        assert a[0, 0, 1] == "c"
        with self.assertRaises(Exception):
            _ = a[0, 0, 2]


    def test_3(self):
        a = MultiDynArray([2, 3, 5])

        a.append((0, 1), 1)
        a.append((0, 1), 2)

        a.delete((0, 1, 1))

        assert a[0, 1, 0] == 1
        with self.assertRaises(Exception):
            _ = a[0, 1, 1]


    def test_4(self):
        a = MultiDynArray([2, 3, 5])

        a.append((1, 1), 42)

        with self.assertRaises(Exception):
            a.delete((1, 1, 1))


    def test_5(self):
        a = MultiDynArray([2, 3, 5])

        with self.assertRaises(Exception):
            a.delete((0, 0, 0))


    def test_6(self):
        a = MultiDynArray([2, 3, 5])

        a.append((0, 0), "x")
        a.append((0, 1), "y")

        a.delete((0, 0, 0))

        with self.assertRaises(Exception):
            _ = a[0, 0, 0]

        assert a[0, 1, 0] == "y"


    def test_7(self):
        a = MultiDynArray([2, 3, 5])

        with self.assertRaises(Exception):
            a.delete((10, 7, 0))