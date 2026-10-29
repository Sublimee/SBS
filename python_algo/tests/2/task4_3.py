import unittest

from task4 import BSTBasedOnArray
from task4_2 import BSTBasedOnArrayWithLCA, BSTBasedOnArrayWithWideAllNodes


class TestInit(unittest.TestCase):

    def test_1(self):
        tree = BSTBasedOnArray(0)

        self.assertEqual(tree.Tree, [None])

    def test_2(self):
        tree = BSTBasedOnArray(1)

        self.assertEqual(tree.Tree, [None] * 3)

    def test_3(self):
        tree = BSTBasedOnArray(3)

        self.assertEqual(tree.Tree, [None] * 15)


class TestFindKeyIndex(unittest.TestCase):

    def setUp(self):
        self.tree = BSTBasedOnArray(3)
        self.tree.Tree = [5, 2, 8, 1, 3, 7, None, None, None, None, None, None, None, None, None]

    def test_1(self):
        tree = BSTBasedOnArray(2)

        result = tree.FindKeyIndex(1)

        self.assertEqual(result, 0)
        self.assertIsNone(tree.Tree[0])

    def test_2(self):
        self.assertEqual(self.tree.FindKeyIndex(5), 0)
        self.assertEqual(self.tree.FindKeyIndex(2), 1)
        self.assertEqual(self.tree.FindKeyIndex(8), 2)
        self.assertEqual(self.tree.FindKeyIndex(1), 3)
        self.assertEqual(self.tree.FindKeyIndex(3), 4)
        self.assertEqual(self.tree.FindKeyIndex(7), 5)

    def test_3(self):
        self.assertEqual(self.tree.FindKeyIndex(9), -6)

    def test_4(self):
        self.assertEqual(self.tree.FindKeyIndex(0), -7)

    def test_5(self):
        self.assertEqual(self.tree.FindKeyIndex(4), -10)

    def test_6(self):
        self.assertEqual(self.tree.FindKeyIndex(6), -11)

    def test_7(self):
        tree = BSTBasedOnArray(1)
        tree.Tree = [5, 2, 8]

        self.assertIsNone(tree.FindKeyIndex(1))
        self.assertIsNone(tree.FindKeyIndex(3))
        self.assertIsNone(tree.FindKeyIndex(6))
        self.assertIsNone(tree.FindKeyIndex(9))

    def test_8(self):
        tree = BSTBasedOnArray(0)
        tree.Tree = [5]

        self.assertEqual(tree.FindKeyIndex(5), 0)
        self.assertIsNone(tree.FindKeyIndex(1))

    def test_9(self):
        tree = BSTBasedOnArray(2)
        tree.Tree = [5, 2, 8, 1, 3, 7, 9]

        self.assertEqual(tree.FindKeyIndex(5), 0)
        self.assertEqual(tree.FindKeyIndex(2), 1)
        self.assertEqual(tree.FindKeyIndex(8), 2)
        self.assertEqual(tree.FindKeyIndex(1), 3)
        self.assertEqual(tree.FindKeyIndex(3), 4)
        self.assertEqual(tree.FindKeyIndex(7), 5)
        self.assertEqual(tree.FindKeyIndex(9), 6)

    def test_10(self):
        tree = BSTBasedOnArray(2)
        tree.Tree = [5, 2, 8, 1, 3, 7, 9]

        self.assertIsNone(tree.FindKeyIndex(0))
        self.assertIsNone(tree.FindKeyIndex(4))
        self.assertIsNone(tree.FindKeyIndex(6))
        self.assertIsNone(tree.FindKeyIndex(10))


class TestAddKey(unittest.TestCase):

    def test_1(self):
        tree = BSTBasedOnArray(2)

        result = tree.AddKey(5)

        self.assertEqual(result, 0)
        self.assertEqual(tree.Tree[0], 5)

    def test_2(self):
        tree = BSTBasedOnArray(2)
        tree.AddKey(5)

        self.assertEqual(tree.AddKey(2), 1)
        self.assertEqual(tree.AddKey(8), 2)
        self.assertEqual(tree.AddKey(1), 3)
        self.assertEqual(tree.AddKey(3), 4)
        self.assertEqual(tree.AddKey(7), 5)
        self.assertEqual(tree.AddKey(9), 6)

        self.assertEqual(tree.Tree, [5, 2, 8, 1, 3, 7, 9])

    def test_3(self):
        tree = BSTBasedOnArray(2)
        tree.AddKey(5)
        tree.AddKey(2)

        result = tree.AddKey(2)

        self.assertEqual(result, 1)
        self.assertEqual(tree.Tree, [5, 2, None, None, None, None, None])

    def test_4(self):
        tree = BSTBasedOnArray(2)
        tree.AddKey(5)

        result = tree.AddKey(5)

        self.assertEqual(result, 0)
        self.assertEqual(tree.Tree, [5, None, None, None, None, None, None])

    def test_5(self):
        tree = BSTBasedOnArray(1)
        tree.AddKey(5)
        tree.AddKey(2)
        tree.AddKey(8)

        result = tree.AddKey(1)

        self.assertEqual(result, -1)
        self.assertEqual(tree.Tree, [5, 2, 8])

    def test_6(self):
        tree = BSTBasedOnArray(2)
        tree.AddKey(1)
        tree.AddKey(2)
        tree.AddKey(3)

        self.assertEqual(tree.Tree, [1, None, 2, None, None, None, 3])
        self.assertEqual(tree.AddKey(4), -1)

    def test_7(self):
        tree = BSTBasedOnArray(0)

        self.assertEqual(tree.AddKey(5), 0)
        self.assertEqual(tree.AddKey(1), -1)
        self.assertEqual(tree.Tree, [5])

    def test_8(self):
        tree = BSTBasedOnArray(3)
        tree.AddKey(5)
        tree.AddKey(2)
        tree.AddKey(8)

        self.assertEqual(tree.AddKey(3), 4)
        self.assertEqual(tree.FindKeyIndex(3), 4)
        self.assertEqual(tree.FindKeyIndex(4), -10)

    def test_9(self):
        tree = BSTBasedOnArray(2)
        tree.AddKey(5)
        tree.AddKey(2)
        tree.AddKey(8)
        tree.AddKey(1)
        tree.AddKey(3)
        tree.AddKey(7)
        tree.AddKey(9)

        self.assertEqual(tree.AddKey(0), -1)
        self.assertEqual(tree.AddKey(4), -1)
        self.assertEqual(tree.AddKey(6), -1)
        self.assertEqual(tree.AddKey(10), -1)

        self.assertEqual(tree.Tree, [5, 2, 8, 1, 3, 7, 9])

    def test_10(self):
        tree = BSTBasedOnArray(2)
        tree.AddKey(5)
        tree.AddKey(2)
        tree.AddKey(8)
        tree.AddKey(1)
        tree.AddKey(3)
        tree.AddKey(7)
        tree.AddKey(9)

        self.assertEqual(tree.AddKey(5), 0)
        self.assertEqual(tree.AddKey(3), 4)
        self.assertEqual(tree.AddKey(9), 6)

        self.assertEqual(tree.Tree, [5, 2, 8, 1, 3, 7, 9])

    def test_11(self):
        tree = BSTBasedOnArray(2)
        tree.AddKey(5)
        tree.AddKey(8)
        tree.AddKey(9)
        tree.AddKey(7)
        tree.AddKey(2)
        tree.AddKey(3)
        tree.AddKey(1)

        self.assertEqual(tree.Tree, [5, 2, 8, 1, 3, 7, 9])


class TestFindLCA(unittest.TestCase):

    def setUp(self):
        self.tree = BSTBasedOnArrayWithLCA(2)
        self.tree.Tree = [5, 2, 8, 1, 3, 7, 9]

    def test_1(self):
        tree = BSTBasedOnArrayWithLCA(2)

        self.assertIsNone(tree.FindLCA(1, 2))

    def test_2(self):
        tree = BSTBasedOnArrayWithLCA(2)
        tree.AddKey(5)

        self.assertEqual(tree.FindLCA(5, 5), 0)

    def test_3(self):
        self.assertEqual(self.tree.FindLCA(1, 3), 1)
        self.assertEqual(self.tree.FindLCA(7, 9), 2)

    def test_4(self):
        self.assertEqual(self.tree.FindLCA(1, 9), 0)
        self.assertEqual(self.tree.FindLCA(3, 7), 0)

    def test_5(self):
        self.assertEqual(self.tree.FindLCA(2, 7), 0)
        self.assertEqual(self.tree.FindLCA(9, 2), 0)

    def test_6(self):
        self.assertEqual(self.tree.FindLCA(2, 3), 1)
        self.assertEqual(self.tree.FindLCA(9, 8), 2)
        self.assertEqual(self.tree.FindLCA(5, 1), 0)

    def test_7(self):
        self.assertEqual(self.tree.FindLCA(3, 3), 4)
        self.assertEqual(self.tree.FindLCA(5, 5), 0)

    def test_8(self):
        self.assertEqual(self.tree.FindLCA(1, 3), self.tree.FindLCA(3, 1))
        self.assertEqual(self.tree.FindLCA(2, 9), self.tree.FindLCA(9, 2))

    def test_9(self):
        self.assertIsNone(self.tree.FindLCA(1, 4))
        self.assertIsNone(self.tree.FindLCA(6, 9))
        self.assertIsNone(self.tree.FindLCA(0, 10))

    def test_10(self):
        tree = BSTBasedOnArrayWithLCA(2)
        tree.AddKey(5)
        tree.AddKey(8)
        tree.AddKey(7)

        self.assertEqual(tree.FindLCA(7, 8), 2)
        self.assertEqual(tree.FindLCA(7, 5), 0)
        self.assertIsNone(tree.FindLCA(7, 2))


class TestWideAllNodes(unittest.TestCase):

    def test_1(self):
        tree = BSTBasedOnArrayWithWideAllNodes(2)

        self.assertEqual(tree.WideAllNodes(), ())

    def test_2(self):
        tree = BSTBasedOnArrayWithWideAllNodes(2)
        tree.AddKey(5)

        self.assertEqual(tree.WideAllNodes(), (5,))

    def test_3(self):
        tree = BSTBasedOnArrayWithWideAllNodes(2)
        tree.AddKey(5)
        tree.AddKey(2)
        tree.AddKey(8)
        tree.AddKey(1)
        tree.AddKey(3)
        tree.AddKey(7)
        tree.AddKey(9)

        self.assertEqual(tree.WideAllNodes(), (5, 2, 8, 1, 3, 7, 9))

    def test_4(self):
        tree = BSTBasedOnArrayWithWideAllNodes(2)
        tree.AddKey(5)
        tree.AddKey(8)
        tree.AddKey(9)
        tree.AddKey(7)
        tree.AddKey(2)
        tree.AddKey(3)
        tree.AddKey(1)

        self.assertEqual(tree.WideAllNodes(), (5, 2, 8, 1, 3, 7, 9))

    def test_5(self):
        tree = BSTBasedOnArrayWithWideAllNodes(3)
        tree.AddKey(5)
        tree.AddKey(2)
        tree.AddKey(8)
        tree.AddKey(3)
        tree.AddKey(9)
        tree.AddKey(4)

        self.assertEqual(tree.WideAllNodes(), (5, 2, 8, 3, 9, 4))

    def test_6(self):
        tree = BSTBasedOnArrayWithWideAllNodes(2)
        tree.AddKey(1)
        tree.AddKey(2)
        tree.AddKey(3)

        self.assertEqual(tree.WideAllNodes(), (1, 2, 3))

    def test_7(self):
        tree = BSTBasedOnArrayWithWideAllNodes(1)
        tree.AddKey(5)
        tree.AddKey(2)
        tree.AddKey(8)
        tree.AddKey(1)

        self.assertEqual(tree.WideAllNodes(), (5, 2, 8))
