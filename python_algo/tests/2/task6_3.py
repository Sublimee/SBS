import unittest

from task6 import BSTNode, BalancedBST
from task6_2 import BalancedBSTWithCorrectnessCheck


class TestGenerateTree(unittest.TestCase):

    def test_1(self) -> None:
        tree = BalancedBST()

        tree.GenerateTree([])

        self.assertIsNone(tree.Root)

    def test_2(self) -> None:
        tree = BalancedBST()

        tree.GenerateTree([5])

        self.assertEqual(tree.Root.NodeKey, 5)
        self.assertEqual(tree.Root.Level, 0)
        self.assertIsNone(tree.Root.Parent)
        self.assertIsNone(tree.Root.LeftChild)
        self.assertIsNone(tree.Root.RightChild)

    def test_3(self) -> None:
        tree = BalancedBST()

        tree.GenerateTree([1, 2, 3])

        self.assertEqual(tree.Root.NodeKey, 2)
        self.assertEqual(tree.Root.LeftChild.NodeKey, 1)
        self.assertEqual(tree.Root.RightChild.NodeKey, 3)
        self.assertEqual(tree.Root.Level, 0)
        self.assertEqual(tree.Root.LeftChild.Level, 1)
        self.assertEqual(tree.Root.RightChild.Level, 1)
        self.assertIsNone(tree.Root.Parent)
        self.assertIs(tree.Root.LeftChild.Parent, tree.Root)
        self.assertIs(tree.Root.RightChild.Parent, tree.Root)
        self.assertIsNone(tree.Root.LeftChild.LeftChild)
        self.assertIsNone(tree.Root.LeftChild.RightChild)
        self.assertIsNone(tree.Root.RightChild.LeftChild)
        self.assertIsNone(tree.Root.RightChild.RightChild)

    def test_4(self) -> None:
        tree = BalancedBST()

        tree.GenerateTree([3, 1, 2])

        self.assertEqual(tree.Root.NodeKey, 2)
        self.assertEqual(tree.Root.LeftChild.NodeKey, 1)
        self.assertEqual(tree.Root.RightChild.NodeKey, 3)

    def test_5(self) -> None:
        tree = BalancedBST()

        tree.GenerateTree([2, 1])

        self.assertEqual(tree.Root.NodeKey, 2)
        self.assertEqual(tree.Root.LeftChild.NodeKey, 1)
        self.assertEqual(tree.Root.LeftChild.Level, 1)
        self.assertIs(tree.Root.LeftChild.Parent, tree.Root)
        self.assertIsNone(tree.Root.RightChild)
        self.assertIsNone(tree.Root.LeftChild.LeftChild)
        self.assertIsNone(tree.Root.LeftChild.RightChild)

    def test_6(self) -> None:
        tree = BalancedBST()

        tree.GenerateTree([4, 1, 3, 2])

        self.assertEqual(tree.Root.NodeKey, 3)
        self.assertEqual(tree.Root.LeftChild.NodeKey, 2)
        self.assertEqual(tree.Root.RightChild.NodeKey, 4)
        self.assertEqual(tree.Root.LeftChild.LeftChild.NodeKey, 1)
        self.assertEqual(tree.Root.LeftChild.LeftChild.Level, 2)
        self.assertIs(tree.Root.LeftChild.LeftChild.Parent, tree.Root.LeftChild)
        self.assertIsNone(tree.Root.LeftChild.RightChild)
        self.assertIsNone(tree.Root.RightChild.LeftChild)
        self.assertIsNone(tree.Root.RightChild.RightChild)

    def test_7(self) -> None:
        tree = BalancedBST()

        tree.GenerateTree([5, 1, 7, 3, 6, 2, 4])

        root = tree.Root
        nodes = [root, root.LeftChild, root.RightChild,
                 root.LeftChild.LeftChild, root.LeftChild.RightChild,
                 root.RightChild.LeftChild, root.RightChild.RightChild]
        self.assertEqual([node.NodeKey for node in nodes], [4, 2, 6, 1, 3, 5, 7])
        self.assertEqual([node.Level for node in nodes], [0, 1, 1, 2, 2, 2, 2])
        self.assertIsNone(root.Parent)
        self.assertIs(root.LeftChild.Parent, root)
        self.assertIs(root.RightChild.Parent, root)
        self.assertIs(root.LeftChild.LeftChild.Parent, root.LeftChild)
        self.assertIs(root.LeftChild.RightChild.Parent, root.LeftChild)
        self.assertIs(root.RightChild.LeftChild.Parent, root.RightChild)
        self.assertIs(root.RightChild.RightChild.Parent, root.RightChild)
        for node in nodes[3:]:
            self.assertIsNone(node.LeftChild)
            self.assertIsNone(node.RightChild)

    def test_8(self) -> None:
        tree = BalancedBST()

        tree.GenerateTree([2, -3, 0, 3, -1, 1, -2])

        root = tree.Root
        self.assertEqual(root.NodeKey, 0)
        self.assertEqual(root.LeftChild.NodeKey, -2)
        self.assertEqual(root.RightChild.NodeKey, 2)
        self.assertEqual(root.LeftChild.LeftChild.NodeKey, -3)
        self.assertEqual(root.LeftChild.RightChild.NodeKey, -1)
        self.assertEqual(root.RightChild.LeftChild.NodeKey, 1)
        self.assertEqual(root.RightChild.RightChild.NodeKey, 3)

    def test_9(self) -> None:
        tree = BalancedBST()
        values = [3, 1, 2]

        tree.GenerateTree(values)

        self.assertEqual(values, [3, 1, 2])
        self.assertEqual(tree.Root.NodeKey, 2)
        self.assertEqual(tree.Root.LeftChild.NodeKey, 1)
        self.assertEqual(tree.Root.RightChild.NodeKey, 3)


class TestIsCorrect(unittest.TestCase):

    def setUp(self) -> None:
        self.tree = BalancedBSTWithCorrectnessCheck()
        self.tree.GenerateTree([5, 1, 7, 3, 6, 2, 4])

    def test_1(self) -> None:
        tree = BalancedBSTWithCorrectnessCheck()

        self.assertTrue(tree.IsCorrect())

    def test_2(self) -> None:
        tree = BalancedBSTWithCorrectnessCheck()
        tree.GenerateTree([5])

        self.assertTrue(tree.IsCorrect())

    def test_3(self) -> None:
        self.assertTrue(self.tree.IsCorrect())

    def test_4(self) -> None:
        self.tree.Root.LeftChild.NodeKey = 5

        self.assertFalse(self.tree.IsCorrect())

    def test_5(self) -> None:
        self.tree.Root.LeftChild.NodeKey = 4

        self.assertFalse(self.tree.IsCorrect())

    def test_6(self) -> None:
        self.tree.Root.RightChild.NodeKey = 3

        self.assertFalse(self.tree.IsCorrect())

    def test_7(self) -> None:
        tree = BalancedBSTWithCorrectnessCheck()
        tree.Root = BSTNode(5, None)
        tree.Root.RightChild = BSTNode(5, tree.Root)

        self.assertTrue(tree.IsCorrect())

    def test_8(self) -> None:
        self.tree.Root.LeftChild.LeftChild.NodeKey = 2

        self.assertFalse(self.tree.IsCorrect())

    def test_9(self) -> None:
        self.tree.Root.RightChild.RightChild.NodeKey = 5

        self.assertFalse(self.tree.IsCorrect())

    def test_10(self) -> None:
        tree = BalancedBSTWithCorrectnessCheck()
        tree.GenerateTree([2, -3, 0, 3, -1, 1, -2])

        self.assertTrue(tree.IsCorrect())

    def test_11(self) -> None:
        tree = BalancedBSTWithCorrectnessCheck()
        tree.Root = BSTNode(3, None)
        tree.Root.LeftChild = BSTNode(2, tree.Root)
        tree.Root.LeftChild.LeftChild = BSTNode(1, tree.Root.LeftChild)

        self.assertTrue(tree.IsCorrect())

        tree.Root.LeftChild.LeftChild.NodeKey = 3

        self.assertFalse(tree.IsCorrect())

    def test_12(self) -> None:
        tree = BalancedBSTWithCorrectnessCheck()
        tree.Root = BSTNode(1, None)
        tree.Root.RightChild = BSTNode(2, tree.Root)
        tree.Root.RightChild.RightChild = BSTNode(3, tree.Root.RightChild)

        self.assertTrue(tree.IsCorrect())

        tree.Root.RightChild.RightChild.NodeKey = 1

        self.assertFalse(tree.IsCorrect())


class TestIsBalanced(unittest.TestCase):

    def test_1(self) -> None:
        tree = BalancedBST()

        self.assertTrue(tree.IsBalanced(tree.Root))

    def test_2(self) -> None:
        tree = BalancedBST()
        tree.GenerateTree([5])

        self.assertTrue(tree.IsBalanced(tree.Root))

    def test_3(self) -> None:
        tree = BalancedBST()
        tree.GenerateTree([5, 1, 7, 3, 6, 2, 4])

        self.assertTrue(tree.IsBalanced(tree.Root))

    def test_4(self) -> None:
        tree = BalancedBST()
        tree.GenerateTree([4, 1, 3, 2])

        self.assertTrue(tree.IsBalanced(tree.Root))

    def test_5(self) -> None:
        tree = BalancedBST()
        tree.Root = BSTNode(3, None)
        tree.Root.LeftChild = BSTNode(2, tree.Root)

        self.assertTrue(tree.IsBalanced(tree.Root))

        tree.Root.LeftChild.LeftChild = BSTNode(1, tree.Root.LeftChild)

        self.assertFalse(tree.IsBalanced(tree.Root))

    def test_6(self) -> None:
        tree = BalancedBST()
        tree.Root = BSTNode(1, None)
        tree.Root.RightChild = BSTNode(2, tree.Root)

        self.assertTrue(tree.IsBalanced(tree.Root))

        tree.Root.RightChild.RightChild = BSTNode(3, tree.Root.RightChild)

        self.assertFalse(tree.IsBalanced(tree.Root))

    def test_7(self) -> None:
        tree = BalancedBST()
        tree.GenerateTree([1, 2, 3, 4, 5, 6, 7])
        left = tree.Root.LeftChild
        left.RightChild = None
        left.LeftChild.LeftChild = BSTNode(0, left.LeftChild)

        self.assertFalse(tree.IsBalanced(tree.Root))

    def test_8(self) -> None:
        tree = BalancedBST()
        tree.GenerateTree([1, 2, 3, 4, 5, 6, 7])
        right = tree.Root.RightChild
        right.LeftChild = None
        right.RightChild.RightChild = BSTNode(8, right.RightChild)

        self.assertFalse(tree.IsBalanced(tree.Root))

    def test_9(self) -> None:
        tree = BalancedBST()
        tree.GenerateTree([1, 2, 3, 4, 5, 6, 7])
        tree.Root.LeftChild.LeftChild = None
        tree.Root.LeftChild.RightChild = None

        self.assertTrue(tree.IsBalanced(tree.Root))

    def test_10(self) -> None:
        tree = BalancedBST()
        tree.GenerateTree([1, 2, 3, 4, 5, 6, 7])
        tree.Root.LeftChild.LeftChild.LeftChild = BSTNode(0, tree.Root.LeftChild.LeftChild)
        tree.Root.LeftChild.LeftChild.LeftChild.LeftChild = BSTNode(-1, tree.Root.LeftChild.LeftChild.LeftChild)

        self.assertFalse(tree.IsBalanced(tree.Root))
        self.assertFalse(tree.IsBalanced(tree.Root.LeftChild))
        self.assertTrue(tree.IsBalanced(tree.Root.RightChild))