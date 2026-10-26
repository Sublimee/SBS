import unittest

from task3 import BST, BSTNode
from task3_2 import BSTWithInvert, BSTWithMaxSumLevel, BSTWithRestore


class TestWideAllNodes(unittest.TestCase):

    def setUp(self):
        self.node8 = BSTNode(8, "8", None)
        self.tree = BST(self.node8)

        self.node4 = BSTNode(4, "4", self.node8)
        self.node8.LeftChild = self.node4

        self.node12 = BSTNode(12, "12", self.node8)
        self.node8.RightChild = self.node12

        self.node2 = BSTNode(2, "2", self.node4)
        self.node4.LeftChild = self.node2

        self.node6 = BSTNode(6, "6", self.node4)
        self.node4.RightChild = self.node6

        self.node10 = BSTNode(10, "10", self.node12)
        self.node12.LeftChild = self.node10

        self.node14 = BSTNode(14, "14", self.node12)
        self.node12.RightChild = self.node14

    def assert_nodes(self, result, nodes):
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), len(nodes))
        for i in range(len(nodes)):
            self.assertIs(result[i], nodes[i])

    def test_1(self):
        result = BST(None).WideAllNodes()

        self.assert_nodes(result, [])

    def test_2(self):
        root = BSTNode(0, "0", None)

        result = BST(root).WideAllNodes()

        self.assert_nodes(result, [root])

    def test_3(self):
        result = self.tree.WideAllNodes()

        self.assert_nodes(result, [
            self.node8,
            self.node4, self.node12,
            self.node2, self.node6, self.node10, self.node14,
        ])

    def test_4(self):
        tree = BST(None)
        tree.AddKeyValue(1, "1")
        tree.AddKeyValue(2, "2")
        tree.AddKeyValue(3, "3")

        result = tree.WideAllNodes()

        keys = [node.NodeKey for node in result]
        self.assertEqual(keys, [1, 2, 3])

    def test_5(self):
        tree = BST(None)
        tree.AddKeyValue(3, "3")
        tree.AddKeyValue(2, "2")
        tree.AddKeyValue(1, "1")

        result = tree.WideAllNodes()

        keys = [node.NodeKey for node in result]
        self.assertEqual(keys, [3, 2, 1])

    def test_6(self):
        tree = BST(None)
        tree.AddKeyValue(8, "8")
        tree.AddKeyValue(4, "4")
        tree.AddKeyValue(12, "12")
        tree.AddKeyValue(6, "6")
        tree.AddKeyValue(10, "10")
        tree.AddKeyValue(5, "5")
        tree.AddKeyValue(11, "11")

        result = tree.WideAllNodes()

        keys = [node.NodeKey for node in result]
        self.assertEqual(keys, [8, 4, 12, 6, 10, 5, 11])

    def test_7(self):
        self.tree.DeleteNodeByKey(8)

        result = self.tree.WideAllNodes()

        keys = [node.NodeKey for node in result]
        self.assertEqual(keys, [10, 4, 12, 2, 6, 14])


class TestDeepAllNodes(unittest.TestCase):

    def setUp(self):
        self.node8 = BSTNode(8, "8", None)
        self.tree = BST(self.node8)

        self.node4 = BSTNode(4, "4", self.node8)
        self.node8.LeftChild = self.node4

        self.node12 = BSTNode(12, "12", self.node8)
        self.node8.RightChild = self.node12

        self.node2 = BSTNode(2, "2", self.node4)
        self.node4.LeftChild = self.node2

        self.node6 = BSTNode(6, "6", self.node4)
        self.node4.RightChild = self.node6

        self.node10 = BSTNode(10, "10", self.node12)
        self.node12.LeftChild = self.node10

        self.node14 = BSTNode(14, "14", self.node12)
        self.node12.RightChild = self.node14

    def assert_nodes(self, result, nodes):
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), len(nodes))
        for i in range(len(nodes)):
            self.assertIs(result[i], nodes[i])

    def test_1(self):
        tree = BST(None)

        self.assert_nodes(tree.DeepAllNodes(0), [])
        self.assert_nodes(tree.DeepAllNodes(1), [])
        self.assert_nodes(tree.DeepAllNodes(2), [])

    def test_2(self):
        root = BSTNode(0, "0", None)
        tree = BST(root)

        self.assert_nodes(tree.DeepAllNodes(0), [root])
        self.assert_nodes(tree.DeepAllNodes(1), [root])
        self.assert_nodes(tree.DeepAllNodes(2), [root])

    def test_3(self):
        result = self.tree.DeepAllNodes(0)

        self.assert_nodes(result, [
            self.node2, self.node4, self.node6,
            self.node8,
            self.node10, self.node12, self.node14,
        ])

    def test_4(self):
        result = self.tree.DeepAllNodes(1)

        self.assert_nodes(result, [
            self.node2, self.node6, self.node4,
            self.node10, self.node14, self.node12,
            self.node8,
        ])

    def test_5(self):
        result = self.tree.DeepAllNodes(2)

        self.assert_nodes(result, [
            self.node8,
            self.node4, self.node2, self.node6,
            self.node12, self.node10, self.node14,
        ])

    def test_6(self):
        tree = BST(None)
        tree.AddKeyValue(8, "8")
        tree.AddKeyValue(4, "4")
        tree.AddKeyValue(12, "12")
        tree.AddKeyValue(6, "6")
        tree.AddKeyValue(10, "10")
        tree.AddKeyValue(5, "5")
        tree.AddKeyValue(11, "11")

        keys = [node.NodeKey for node in tree.DeepAllNodes(0)]
        self.assertEqual(keys, [4, 5, 6, 8, 10, 11, 12])

        keys = [node.NodeKey for node in tree.DeepAllNodes(1)]
        self.assertEqual(keys, [5, 6, 4, 11, 10, 12, 8])

        keys = [node.NodeKey for node in tree.DeepAllNodes(2)]
        self.assertEqual(keys, [8, 4, 6, 5, 12, 10, 11])

    def test_7(self):
        tree = BST(None)
        tree.AddKeyValue(1, "1")
        tree.AddKeyValue(2, "2")
        tree.AddKeyValue(3, "3")

        keys = [node.NodeKey for node in tree.DeepAllNodes(0)]
        self.assertEqual(keys, [1, 2, 3])

        keys = [node.NodeKey for node in tree.DeepAllNodes(1)]
        self.assertEqual(keys, [3, 2, 1])

        keys = [node.NodeKey for node in tree.DeepAllNodes(2)]
        self.assertEqual(keys, [1, 2, 3])

    def test_8(self):
        self.tree.DeleteNodeByKey(8)

        keys = [node.NodeKey for node in self.tree.DeepAllNodes(0)]
        self.assertEqual(keys, [2, 4, 6, 10, 12, 14])

        keys = [node.NodeKey for node in self.tree.DeepAllNodes(1)]
        self.assertEqual(keys, [2, 6, 4, 14, 12, 10])

        keys = [node.NodeKey for node in self.tree.DeepAllNodes(2)]
        self.assertEqual(keys, [10, 4, 2, 6, 12, 14])


class TestInvert(unittest.TestCase):

    def setUp(self):
        self.node8 = BSTNode(8, "8", None)
        self.tree = BSTWithInvert(self.node8)

        self.node4 = BSTNode(4, "4", self.node8)
        self.node8.LeftChild = self.node4

        self.node12 = BSTNode(12, "12", self.node8)
        self.node8.RightChild = self.node12

        self.node2 = BSTNode(2, "2", self.node4)
        self.node4.LeftChild = self.node2

        self.node6 = BSTNode(6, "6", self.node4)
        self.node4.RightChild = self.node6

        self.node10 = BSTNode(10, "10", self.node12)
        self.node12.LeftChild = self.node10

        self.node14 = BSTNode(14, "14", self.node12)
        self.node12.RightChild = self.node14

    def assert_children(self, node, left, right):
        self.assertIs(node.LeftChild, left)
        self.assertIs(node.RightChild, right)

    def test_1(self):
        tree = BSTWithInvert(None)

        tree.Invert()

        self.assertIsNone(tree.Root)

    def test_2(self):
        root = BSTNode(0, "0", None)
        tree = BSTWithInvert(root)

        tree.Invert()

        self.assertIs(tree.Root, root)
        self.assert_children(root, None, None)

    def test_3(self):
        self.tree.Invert()

        self.assertIs(self.tree.Root, self.node8)
        self.assert_children(self.node8, self.node12, self.node4)
        self.assert_children(self.node12, self.node14, self.node10)
        self.assert_children(self.node4, self.node6, self.node2)
        self.assert_children(self.node14, None, None)
        self.assert_children(self.node10, None, None)
        self.assert_children(self.node6, None, None)
        self.assert_children(self.node2, None, None)

    def test_4(self):
        self.tree.Invert()

        self.assertIsNone(self.node8.Parent)
        self.assertIs(self.node4.Parent, self.node8)
        self.assertIs(self.node12.Parent, self.node8)
        self.assertIs(self.node2.Parent, self.node4)
        self.assertIs(self.node6.Parent, self.node4)
        self.assertIs(self.node10.Parent, self.node12)
        self.assertIs(self.node14.Parent, self.node12)

    def test_5(self):
        self.tree.Invert()

        keys = [node.NodeKey for node in self.tree.WideAllNodes()]
        self.assertEqual(keys, [8, 12, 4, 14, 10, 6, 2])

        keys = [node.NodeKey for node in self.tree.DeepAllNodes(0)]
        self.assertEqual(keys, [14, 12, 10, 8, 6, 4, 2])

    def test_6(self):
        tree = BSTWithInvert(None)
        tree.AddKeyValue(1, "1")
        tree.AddKeyValue(2, "2")
        tree.AddKeyValue(3, "3")

        tree.Invert()

        root = tree.Root
        self.assertEqual(root.NodeKey, 1)
        self.assertIsNone(root.RightChild)
        self.assertEqual(root.LeftChild.NodeKey, 2)
        self.assertIsNone(root.LeftChild.RightChild)
        self.assertEqual(root.LeftChild.LeftChild.NodeKey, 3)

    def test_7(self):
        self.tree.Invert()
        self.tree.Invert()

        self.assertIs(self.tree.Root, self.node8)
        self.assert_children(self.node8, self.node4, self.node12)
        self.assert_children(self.node4, self.node2, self.node6)
        self.assert_children(self.node12, self.node10, self.node14)


class TestGetMaxSumLevel(unittest.TestCase):

    def setUp(self):
        self.node8 = BSTNode(8, 5, None)
        self.tree = BSTWithMaxSumLevel(self.node8)

        self.node4 = BSTNode(4, 3, self.node8)
        self.node8.LeftChild = self.node4

        self.node12 = BSTNode(12, 1, self.node8)
        self.node8.RightChild = self.node12

        self.node2 = BSTNode(2, 4, self.node4)
        self.node4.LeftChild = self.node2

        self.node6 = BSTNode(6, 2, self.node4)
        self.node4.RightChild = self.node6

        self.node10 = BSTNode(10, 6, self.node12)
        self.node12.LeftChild = self.node10

        self.node14 = BSTNode(14, 1, self.node12)
        self.node12.RightChild = self.node14

    def test_1(self):
        tree = BSTWithMaxSumLevel(None)

        self.assertEqual(tree.GetMaxSumLevel(), -1)

    def test_2(self):
        root = BSTNode(0, -3, None)
        tree = BSTWithMaxSumLevel(root)

        self.assertEqual(tree.GetMaxSumLevel(), 0)

    def test_3(self):
        self.assertEqual(self.tree.GetMaxSumLevel(), 2)

    def test_4(self):
        self.node8.NodeValue = 20

        self.assertEqual(self.tree.GetMaxSumLevel(), 0)

    def test_5(self):
        self.node4.NodeValue = 10
        self.node12.NodeValue = 10

        self.assertEqual(self.tree.GetMaxSumLevel(), 1)

    def test_6(self):
        self.node4.NodeValue = 6
        self.node12.NodeValue = 7

        self.assertEqual(self.tree.GetMaxSumLevel(), 1)

    def test_7(self):
        self.node2.NodeValue = -4
        self.node6.NodeValue = -2
        self.node10.NodeValue = -6
        self.node14.NodeValue = -1

        self.assertEqual(self.tree.GetMaxSumLevel(), 0)

    def test_8(self):
        self.node8.NodeValue = -5
        self.node4.NodeValue = -3
        self.node12.NodeValue = -1
        self.node2.NodeValue = -4
        self.node6.NodeValue = -2
        self.node10.NodeValue = -6
        self.node14.NodeValue = -1

        self.assertEqual(self.tree.GetMaxSumLevel(), 1)

    def test_9(self):
        tree = BSTWithMaxSumLevel(None)
        tree.AddKeyValue(1, 1)
        tree.AddKeyValue(2, 2)
        tree.AddKeyValue(3, 3)
        tree.AddKeyValue(4, 1)

        self.assertEqual(tree.GetMaxSumLevel(), 2)

    def test_10(self):
        root = BSTNode(0, 0, None)
        tree = BSTWithMaxSumLevel(root)
        node = root
        for key in range(1, 100000):
            child = BSTNode(key, key, node)
            node.RightChild = child
            node = child

        self.assertEqual(tree.GetMaxSumLevel(), 99999)


class TestRestore(unittest.TestCase):

    def assert_node(self, node, key, parent):
        self.assertEqual(node.NodeKey, key)
        self.assertEqual(node.NodeValue, key)
        self.assertIs(node.Parent, parent)

    def test_1(self):
        tree = BSTWithRestore(None)

        tree.Restore([], [])

        self.assertIsNone(tree.Root)

    def test_2(self):
        tree = BSTWithRestore(None)

        tree.Restore([1], [1])

        self.assert_node(tree.Root, 1, None)
        self.assertIsNone(tree.Root.LeftChild)
        self.assertIsNone(tree.Root.RightChild)

    def test_3(self):
        tree = BSTWithRestore(None)

        tree.Restore([1, 2, 4, 5, 3, 6, 7], [4, 2, 5, 1, 6, 3, 7])

        root = tree.Root
        self.assert_node(root, 1, None)
        self.assert_node(root.LeftChild, 2, root)
        self.assert_node(root.RightChild, 3, root)
        self.assert_node(root.LeftChild.LeftChild, 4, root.LeftChild)
        self.assert_node(root.LeftChild.RightChild, 5, root.LeftChild)
        self.assert_node(root.RightChild.LeftChild, 6, root.RightChild)
        self.assert_node(root.RightChild.RightChild, 7, root.RightChild)

    def test_4(self):
        tree = BSTWithRestore(None)

        tree.Restore([1, 2, 3], [3, 2, 1])

        root = tree.Root
        self.assert_node(root, 1, None)
        self.assertIsNone(root.RightChild)
        self.assert_node(root.LeftChild, 2, root)
        self.assertIsNone(root.LeftChild.RightChild)
        self.assert_node(root.LeftChild.LeftChild, 3, root.LeftChild)

    def test_5(self):
        tree = BSTWithRestore(None)

        tree.Restore([1, 2, 3], [1, 2, 3])

        root = tree.Root
        self.assert_node(root, 1, None)
        self.assertIsNone(root.LeftChild)
        self.assert_node(root.RightChild, 2, root)
        self.assertIsNone(root.RightChild.LeftChild)
        self.assert_node(root.RightChild.RightChild, 3, root.RightChild)

    def test_6(self):
        left = BSTWithRestore(None)
        left.Restore([1, 2], [2, 1])

        right = BSTWithRestore(None)
        right.Restore([1, 2], [1, 2])

        self.assert_node(left.Root.LeftChild, 2, left.Root)
        self.assertIsNone(left.Root.RightChild)
        self.assertIsNone(right.Root.LeftChild)
        self.assert_node(right.Root.RightChild, 2, right.Root)

    def test_7(self):
        prefix = [5, 3, 4, 8, 9, 7]
        infix = [3, 4, 5, 8, 7, 9]
        tree = BSTWithRestore(None)

        tree.Restore(prefix, infix)

        keys = [node.NodeKey for node in tree.DeepAllNodes(2)]
        self.assertEqual(keys, prefix)
        keys = [node.NodeKey for node in tree.DeepAllNodes(0)]
        self.assertEqual(keys, infix)
