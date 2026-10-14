import unittest

from task2 import BST, BSTFind, BSTNode
from task2_2 import BSTComparable, BSTWithMaxSumPaths, BSTWithPathsOfLength, BSTWithSymmetricCheck


class TestFindNodeByKey(unittest.TestCase):

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

    def assert_find_node_by_key_result(self, result, node, hasKey, toLeft=None):
        self.assertIsInstance(result, BSTFind)
        self.assertIs(result.Node, node)
        self.assertIs(result.NodeHasKey, hasKey)
        if toLeft is not None:
            self.assertIs(result.ToLeft, toLeft)

    def test_1(self):
        result = BST(None).FindNodeByKey(8)

        self.assert_find_node_by_key_result(result, None, False, False)

    def test_2(self):
        root = BSTNode(0, "0", None)

        result = BST(root).FindNodeByKey(0)

        self.assert_find_node_by_key_result(result, root, True)

    def test_3(self):
        root = BSTNode(0, "root", None)
        tree = BST(root)

        result = tree.FindNodeByKey(-1)
        self.assert_find_node_by_key_result(result, root, False, True)

        result = tree.FindNodeByKey(1)
        self.assert_find_node_by_key_result(result, root, False, False)

    def test_4(self):
        result = self.tree.FindNodeByKey(8)
        self.assert_find_node_by_key_result(result, self.node8, True)
        self.assertEqual(result.Node.NodeValue, "8")

        result = self.tree.FindNodeByKey(4)
        self.assert_find_node_by_key_result(result, self.node4, True)
        self.assertEqual(result.Node.NodeValue, "4")

        result = self.tree.FindNodeByKey(12)
        self.assert_find_node_by_key_result(result, self.node12, True)
        self.assertEqual(result.Node.NodeValue, "12")

        result = self.tree.FindNodeByKey(2)
        self.assert_find_node_by_key_result(result, self.node2, True)
        self.assertEqual(result.Node.NodeValue, "2")

        result = self.tree.FindNodeByKey(6)
        self.assert_find_node_by_key_result(result, self.node6, True)
        self.assertEqual(result.Node.NodeValue, "6")

        result = self.tree.FindNodeByKey(10)
        self.assert_find_node_by_key_result(result, self.node10, True)
        self.assertEqual(result.Node.NodeValue, "10")

        result = self.tree.FindNodeByKey(14)
        self.assert_find_node_by_key_result(result, self.node14, True)
        self.assertEqual(result.Node.NodeValue, "14")

    def test_5(self):
        result = self.tree.FindNodeByKey(-1)
        self.assert_find_node_by_key_result(result, self.node2, False, True)

        result = self.tree.FindNodeByKey(5)
        self.assert_find_node_by_key_result(result, self.node6, False, True)

        result = self.tree.FindNodeByKey(9)
        self.assert_find_node_by_key_result(result, self.node10, False, True)

        result = self.tree.FindNodeByKey(13)
        self.assert_find_node_by_key_result(result, self.node14, False, True)

    def test_6(self):
        result = self.tree.FindNodeByKey(3)
        self.assert_find_node_by_key_result(result, self.node2, False, False)

        result = self.tree.FindNodeByKey(7)
        self.assert_find_node_by_key_result(result, self.node6, False, False)

        result = self.tree.FindNodeByKey(11)
        self.assert_find_node_by_key_result(result, self.node10, False, False)

        result = self.tree.FindNodeByKey(15)
        self.assert_find_node_by_key_result(result, self.node14, False, False)

    def test_7(self):
        root = BSTNode(8, "8", None)
        child = BSTNode(12, "12", root)
        root.RightChild = child
        tree = BST(root)

        result = tree.FindNodeByKey(6)
        self.assert_find_node_by_key_result(result, root, False, True)

        root = BSTNode(8, "8", None)
        child = BSTNode(4, "4", root)
        root.LeftChild = child
        tree = BST(root)

        result = tree.FindNodeByKey(10)
        self.assert_find_node_by_key_result(result, root, False, False)

    def test_8(self):
        root = BSTNode(0, "0", None)
        child = BSTNode(-1, "-1", root)
        root.LeftChild = child
        last = BSTNode(-2, "-2", child)
        child.LeftChild = last
        tree = BST(root)

        result = tree.FindNodeByKey(-2)
        self.assert_find_node_by_key_result(result, last, True)

        result = tree.FindNodeByKey(-3)
        self.assert_find_node_by_key_result(result, last, False, True)

        root = BSTNode(0, "0", None)
        child = BSTNode(1, "1", root)
        root.RightChild = child
        last = BSTNode(2, "2", child)
        child.RightChild = last
        tree = BST(root)

        result = tree.FindNodeByKey(2)
        self.assert_find_node_by_key_result(result, last, True)

        result = tree.FindNodeByKey(3)
        self.assert_find_node_by_key_result(result, last, False, False)


class TestAddKeyValue(unittest.TestCase):

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

    def assert_node_state(self, node, key, value, parent, left=None, right=None):
        self.assertIsInstance(node, BSTNode)
        self.assertEqual(node.NodeKey, key)
        self.assertEqual(node.NodeValue, value)
        self.assertIs(node.Parent, parent)
        self.assertIs(node.LeftChild, left)
        self.assertIs(node.RightChild, right)

    def assert_initial_tree(self):
        self.assertIs(self.tree.Root, self.node8)
        self.assert_node_state(self.node8, 8, "8", None, self.node4, self.node12)
        self.assert_node_state(self.node4, 4, "4", self.node8, self.node2, self.node6)
        self.assert_node_state(self.node12, 12, "12", self.node8, self.node10, self.node14)
        self.assert_node_state(self.node2, 2, "2", self.node4)
        self.assert_node_state(self.node6, 6, "6", self.node4)
        self.assert_node_state(self.node10, 10, "10", self.node12)
        self.assert_node_state(self.node14, 14, "14", self.node12)

    def test_1(self):
        tree = BST(None)
        self.assertIsNone(tree.FindNodeByKey(8).Node)

        self.assertIs(tree.AddKeyValue(8, "8"), True)

        self.assert_node_state(tree.Root, 8, "8", None)
        result = tree.FindNodeByKey(8)
        self.assertIs(result.NodeHasKey, True)
        self.assertIs(result.Node, tree.Root)

    def test_2(self):
        root = BSTNode(8, "8", None)
        node12 = BSTNode(12, "12", root)
        root.RightChild = node12
        tree = BST(root)
        self.assertIs(tree.FindNodeByKey(4).NodeHasKey, False)

        self.assertIs(tree.AddKeyValue(4, "4"), True)

        node4 = root.LeftChild
        self.assert_node_state(node4, 4, "4", root)
        self.assertIs(tree.Root, root)
        self.assert_node_state(root, 8, "8", None, node4, node12)
        self.assert_node_state(node12, 12, "12", root)
        result = tree.FindNodeByKey(4)
        self.assertIs(result.NodeHasKey, True)
        self.assertIs(result.Node, node4)

    def test_3(self):
        root = BSTNode(8, "8", None)
        node4 = BSTNode(4, "4", root)
        root.LeftChild = node4
        tree = BST(root)
        self.assertIs(tree.FindNodeByKey(12).NodeHasKey, False)

        self.assertIs(tree.AddKeyValue(12, "12"), True)

        node12 = root.RightChild
        self.assert_node_state(node12, 12, "12", root)
        self.assertIs(tree.Root, root)
        self.assert_node_state(root, 8, "8", None, node4, node12)
        self.assert_node_state(node4, 4, "4", root)
        result = tree.FindNodeByKey(12)
        self.assertIs(result.NodeHasKey, True)
        self.assertIs(result.Node, node12)

    def test_4(self):
        self.assertIs(self.tree.FindNodeByKey(5).NodeHasKey, False)

        self.assertIs(self.tree.AddKeyValue(5, "5"), True)

        node5 = self.node6.LeftChild
        self.assert_node_state(node5, 5, "5", self.node6)
        self.assert_node_state(self.node6, 6, "6", self.node4, node5)
        self.assertIs(self.tree.Root, self.node8)
        self.assertIs(self.node8.LeftChild, self.node4)
        self.assertIs(self.node4.RightChild, self.node6)
        result = self.tree.FindNodeByKey(5)
        self.assertIs(result.NodeHasKey, True)
        self.assertIs(result.Node, node5)

    def test_5(self):
        self.assertIs(self.tree.FindNodeByKey(11).NodeHasKey, False)

        self.assertIs(self.tree.AddKeyValue(11, "11"), True)

        node11 = self.node10.RightChild
        self.assert_node_state(node11, 11, "11", self.node10)
        self.assert_node_state(self.node10, 10, "10", self.node12, None, node11)
        self.assertIs(self.tree.Root, self.node8)
        self.assertIs(self.node8.RightChild, self.node12)
        self.assertIs(self.node12.LeftChild, self.node10)
        result = self.tree.FindNodeByKey(11)
        self.assertIs(result.NodeHasKey, True)
        self.assertIs(result.Node, node11)

    def test_6(self):
        self.assertIs(self.tree.AddKeyValue(8, "other"), False)

        self.assert_initial_tree()

    def test_7(self):
        self.assertIs(self.tree.AddKeyValue(4, "other"), False)
        self.assert_initial_tree()

        self.assertIs(self.tree.AddKeyValue(10, "other"), False)
        self.assert_initial_tree()

    def test_8(self):
        tree = BST(None)
        self.assertIs(tree.AddKeyValue(0, "0"), True)
        root = tree.Root

        self.assertIs(tree.AddKeyValue(-1, "-1"), True)
        node_minus1 = root.LeftChild

        self.assertIs(tree.AddKeyValue(-2, "-2"), True)
        self.assertIsInstance(node_minus1, BSTNode)
        node_minus2 = node_minus1.LeftChild

        self.assertIs(tree.AddKeyValue(1, "1"), True)
        node1 = root.RightChild

        self.assertIs(tree.AddKeyValue(2, "2"), True)
        self.assertIsInstance(node1, BSTNode)
        node2 = node1.RightChild

        self.assertIs(tree.AddKeyValue(-2, "other"), False)

        self.assertIs(tree.Root, root)
        self.assert_node_state(root, 0, "0", None, node_minus1, node1)
        self.assert_node_state(node_minus1, -1, "-1", root, node_minus2)
        self.assert_node_state(node_minus2, -2, "-2", node_minus1)
        self.assert_node_state(node1, 1, "1", root, None, node2)
        self.assert_node_state(node2, 2, "2", node1)
        self.assertIs(tree.FindNodeByKey(-2).NodeHasKey, True)
        self.assertIs(tree.FindNodeByKey(-2).Node, node_minus2)
        self.assertIs(tree.FindNodeByKey(2).NodeHasKey, True)
        self.assertIs(tree.FindNodeByKey(2).Node, node2)


class TestFinMinMax(unittest.TestCase):

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

    def test_1(self):
        tree = BST(None)

        self.assertIsNone(tree.FinMinMax(tree.Root, False))
        self.assertIsNone(tree.FinMinMax(tree.Root, True))
        self.assertIsNone(self.tree.FinMinMax(None, False))
        self.assertIsNone(self.tree.FinMinMax(None, True))

    def test_2(self):
        root = BSTNode(0, "0", None)
        tree = BST(root)

        self.assertIs(tree.FinMinMax(root, False), root)
        self.assertIs(tree.FinMinMax(root, True), root)

    def test_3(self):
        result = self.tree.FinMinMax(self.tree.Root, False)

        self.assertIs(result, self.node2)

    def test_4(self):
        result = self.tree.FinMinMax(self.tree.Root, True)

        self.assertIs(result, self.node14)

    def test_5(self):
        result = self.tree.FinMinMax(self.node4, False)
        self.assertIs(result, self.node2)

        result = self.tree.FinMinMax(self.node12, False)
        self.assertIs(result, self.node10)

    def test_6(self):
        result = self.tree.FinMinMax(self.node4, True)
        self.assertIs(result, self.node6)

        result = self.tree.FinMinMax(self.node12, True)
        self.assertIs(result, self.node14)

    def test_7(self):
        self.assertIs(self.tree.FinMinMax(self.node6, False), self.node6)
        self.assertIs(self.tree.FinMinMax(self.node6, True), self.node6)

    def test_8(self):
        root = BSTNode(8, "8", None)
        node12 = BSTNode(12, "12", root)
        root.RightChild = node12
        node10 = BSTNode(10, "10", node12)
        node12.LeftChild = node10
        tree = BST(root)

        self.assertIs(tree.FinMinMax(root, False), root)
        self.assertIs(tree.FinMinMax(root, True), node12)

        root = BSTNode(8, "8", None)
        node4 = BSTNode(4, "4", root)
        root.LeftChild = node4
        node6 = BSTNode(6, "6", node4)
        node4.RightChild = node6
        tree = BST(root)

        self.assertIs(tree.FinMinMax(root, False), node4)
        self.assertIs(tree.FinMinMax(root, True), root)

    def test_9(self):
        root = BSTNode(0, "0", None)
        node_minus1 = BSTNode(-1, "-1", root)
        root.LeftChild = node_minus1
        node_minus2 = BSTNode(-2, "-2", node_minus1)
        node_minus1.LeftChild = node_minus2
        node1 = BSTNode(1, "1", root)
        root.RightChild = node1
        node2 = BSTNode(2, "2", node1)
        node1.RightChild = node2
        tree = BST(root)

        self.assertIs(tree.FinMinMax(root, False), node_minus2)
        self.assertIs(tree.FinMinMax(root, True), node2)
        self.assertIs(tree.FinMinMax(node_minus1, False), node_minus2)
        self.assertIs(tree.FinMinMax(node_minus1, True), node_minus1)
        self.assertIs(tree.FinMinMax(node1, False), node1)
        self.assertIs(tree.FinMinMax(node1, True), node2)


class TestDeleteRoot(unittest.TestCase):

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

    def assert_node_state(self, node, key, parent, left=None, right=None):
        self.assertEqual(node.NodeKey, key)
        self.assertEqual(node.NodeValue, str(key))
        self.assertIs(node.Parent, parent)
        self.assertIs(node.LeftChild, left)
        self.assertIs(node.RightChild, right)

    def test_1(self):
        root = BSTNode(8, "8", None)
        node4 = BSTNode(4, "4", root)
        root.LeftChild = node4
        node12 = BSTNode(12, "12", root)
        root.RightChild = node12
        tree = BST(root)

        self.assertIs(tree.DeleteNodeByKey(8), True)

        self.assertIs(tree.Root, node12)
        self.assert_node_state(node12, 12, None, node4)
        self.assert_node_state(node4, 4, node12)
        self.assertIs(tree.FindNodeByKey(8).NodeHasKey, False)

    def test_2(self):
        root = BSTNode(8, "8", None)
        node4 = BSTNode(4, "4", root)
        root.LeftChild = node4
        node12 = BSTNode(12, "12", root)
        root.RightChild = node12
        node14 = BSTNode(14, "14", node12)
        node12.RightChild = node14
        tree = BST(root)

        self.assertIs(tree.DeleteNodeByKey(8), True)

        self.assertIs(tree.Root, node12)
        self.assert_node_state(node12, 12, None, node4, node14)
        self.assert_node_state(node4, 4, node12)
        self.assert_node_state(node14, 14, node12)
        self.assertIs(tree.FindNodeByKey(8).NodeHasKey, False)

    def test_3(self):
        self.assertIs(self.tree.DeleteNodeByKey(8), True)

        self.assertIs(self.tree.Root, self.node10)
        self.assert_node_state(self.node10, 10, None, self.node4, self.node12)
        self.assert_node_state(self.node4, 4, self.node10, self.node2, self.node6)
        self.assert_node_state(self.node12, 12, self.node10, None, self.node14)
        self.assert_node_state(self.node2, 2, self.node4)
        self.assert_node_state(self.node6, 6, self.node4)
        self.assert_node_state(self.node14, 14, self.node12)
        self.assertIs(self.tree.FindNodeByKey(8).NodeHasKey, False)

    def test_4(self):
        node11 = BSTNode(11, "11", self.node10)
        self.node10.RightChild = node11

        self.assertIs(self.tree.DeleteNodeByKey(8), True)

        self.assertIs(self.tree.Root, self.node10)
        self.assert_node_state(self.node10, 10, None, self.node4, self.node12)
        self.assert_node_state(self.node4, 4, self.node10, self.node2, self.node6)
        self.assert_node_state(self.node12, 12, self.node10, node11, self.node14)
        self.assert_node_state(node11, 11, self.node12)
        self.assert_node_state(self.node2, 2, self.node4)
        self.assert_node_state(self.node6, 6, self.node4)
        self.assert_node_state(self.node14, 14, self.node12)
        self.assertIs(self.tree.FindNodeByKey(8).NodeHasKey, False)
        self.assertIs(self.tree.FindNodeByKey(11).Node, node11)


class TestDeleteNodeByKey(unittest.TestCase):

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

    def assert_node_state(self, node, key, parent, left=None, right=None):
        self.assertEqual(node.NodeKey, key)
        self.assertEqual(node.NodeValue, str(key))
        self.assertIs(node.Parent, parent)
        self.assertIs(node.LeftChild, left)
        self.assertIs(node.RightChild, right)

    def test_1(self):
        tree = BST(None)

        self.assertIs(tree.DeleteNodeByKey(8), False)
        self.assertIsNone(tree.Root)

    def test_2(self):
        self.assertIs(self.tree.DeleteNodeByKey(99), False)

        self.assertIs(self.tree.Root, self.node8)
        self.assert_node_state(self.node8, 8, None, self.node4, self.node12)
        self.assert_node_state(self.node4, 4, self.node8, self.node2, self.node6)
        self.assert_node_state(self.node12, 12, self.node8, self.node10, self.node14)
        self.assert_node_state(self.node2, 2, self.node4)
        self.assert_node_state(self.node6, 6, self.node4)
        self.assert_node_state(self.node10, 10, self.node12)
        self.assert_node_state(self.node14, 14, self.node12)

    def test_3(self):
        root = BSTNode(8, "8", None)
        tree = BST(root)

        self.assertIs(tree.DeleteNodeByKey(8), True)
        self.assertIsNone(tree.Root)
        self.assertIs(tree.DeleteNodeByKey(8), False)

    def test_4(self):
        self.assertIs(self.tree.DeleteNodeByKey(2), True)
        self.assertIs(self.tree.DeleteNodeByKey(14), True)

        self.assertIs(self.tree.Root, self.node8)
        self.assert_node_state(self.node8, 8, None, self.node4, self.node12)
        self.assert_node_state(self.node4, 4, self.node8, None, self.node6)
        self.assert_node_state(self.node12, 12, self.node8, self.node10)
        self.assert_node_state(self.node6, 6, self.node4)
        self.assert_node_state(self.node10, 10, self.node12)
        self.assertIs(self.tree.FindNodeByKey(2).NodeHasKey, False)
        self.assertIs(self.tree.FindNodeByKey(14).NodeHasKey, False)

    def test_5(self):
        root = BSTNode(8, "8", None)
        node4 = BSTNode(4, "4", root)
        root.LeftChild = node4
        tree = BST(root)

        self.assertIs(tree.DeleteNodeByKey(8), True)
        self.assertIs(tree.Root, node4)
        self.assert_node_state(node4, 4, None)

        root = BSTNode(8, "8", None)
        node12 = BSTNode(12, "12", root)
        root.RightChild = node12
        tree = BST(root)

        self.assertIs(tree.DeleteNodeByKey(8), True)
        self.assertIs(tree.Root, node12)
        self.assert_node_state(node12, 12, None)

    def test_6(self):
        root = BSTNode(8, "8", None)
        node4 = BSTNode(4, "4", root)
        root.LeftChild = node4
        node2 = BSTNode(2, "2", node4)
        node4.LeftChild = node2
        node12 = BSTNode(12, "12", root)
        root.RightChild = node12
        node14 = BSTNode(14, "14", node12)
        node12.RightChild = node14
        tree = BST(root)

        self.assertIs(tree.DeleteNodeByKey(4), True)
        self.assertIs(tree.DeleteNodeByKey(12), True)

        self.assertIs(tree.Root, root)
        self.assert_node_state(root, 8, None, node2, node14)
        self.assert_node_state(node2, 2, root)
        self.assert_node_state(node14, 14, root)

    def test_7(self):
        root = BSTNode(8, "8", None)
        node4 = BSTNode(4, "4", root)
        root.LeftChild = node4
        node6 = BSTNode(6, "6", node4)
        node4.RightChild = node6
        node12 = BSTNode(12, "12", root)
        root.RightChild = node12
        node10 = BSTNode(10, "10", node12)
        node12.LeftChild = node10
        tree = BST(root)

        self.assertIs(tree.DeleteNodeByKey(4), True)
        self.assertIs(tree.DeleteNodeByKey(12), True)

        self.assertIs(tree.Root, root)
        self.assert_node_state(root, 8, None, node6, node10)
        self.assert_node_state(node6, 6, root)
        self.assert_node_state(node10, 10, root)

    def test_8(self):
        self.assertIs(self.tree.DeleteNodeByKey(4), True)

        self.assertIs(self.tree.Root, self.node8)
        self.assert_node_state(self.node8, 8, None, self.node6, self.node12)
        self.assert_node_state(self.node6, 6, self.node8, self.node2)
        self.assert_node_state(self.node2, 2, self.node6)
        self.assert_node_state(self.node12, 12, self.node8, self.node10, self.node14)
        self.assert_node_state(self.node10, 10, self.node12)
        self.assert_node_state(self.node14, 14, self.node12)
        self.assertIs(self.tree.FindNodeByKey(4).NodeHasKey, False)

    def test_9(self):
        self.assertIs(self.tree.DeleteNodeByKey(12), True)

        self.assertIs(self.tree.Root, self.node8)
        self.assert_node_state(self.node8, 8, None, self.node4, self.node14)
        self.assert_node_state(self.node14, 14, self.node8, self.node10)
        self.assert_node_state(self.node10, 10, self.node14)
        self.assert_node_state(self.node4, 4, self.node8, self.node2, self.node6)
        self.assert_node_state(self.node2, 2, self.node4)
        self.assert_node_state(self.node6, 6, self.node4)
        self.assertIs(self.tree.FindNodeByKey(12).NodeHasKey, False)

    def test_10(self):
        node5 = BSTNode(5, "5", self.node6)
        self.node6.LeftChild = node5

        self.assertIs(self.tree.DeleteNodeByKey(4), True)

        self.assertIs(self.tree.Root, self.node8)
        self.assert_node_state(self.node8, 8, None, node5, self.node12)
        self.assert_node_state(node5, 5, self.node8, self.node2, self.node6)
        self.assert_node_state(self.node2, 2, node5)
        self.assert_node_state(self.node6, 6, node5)
        self.assert_node_state(self.node12, 12, self.node8, self.node10, self.node14)
        self.assert_node_state(self.node10, 10, self.node12)
        self.assert_node_state(self.node14, 14, self.node12)
        self.assertIs(self.tree.FindNodeByKey(4).NodeHasKey, False)

    def test_11(self):
        node13 = BSTNode(13, "13", self.node14)
        self.node14.LeftChild = node13

        self.assertIs(self.tree.DeleteNodeByKey(12), True)

        self.assertIs(self.tree.Root, self.node8)
        self.assert_node_state(self.node8, 8, None, self.node4, node13)
        self.assert_node_state(node13, 13, self.node8, self.node10, self.node14)
        self.assert_node_state(self.node10, 10, node13)
        self.assert_node_state(self.node14, 14, node13)
        self.assert_node_state(self.node4, 4, self.node8, self.node2, self.node6)
        self.assert_node_state(self.node2, 2, self.node4)
        self.assert_node_state(self.node6, 6, self.node4)
        self.assertIs(self.tree.FindNodeByKey(12).NodeHasKey, False)

    def test_12(self):
        root = BSTNode(20, "20", None)
        node8 = BSTNode(8, "8", root)
        root.LeftChild = node8
        node30 = BSTNode(30, "30", root)
        root.RightChild = node30
        node4 = BSTNode(4, "4", node8)
        node8.LeftChild = node4
        node16 = BSTNode(16, "16", node8)
        node8.RightChild = node16
        node12 = BSTNode(12, "12", node16)
        node16.LeftChild = node12
        node10 = BSTNode(10, "10", node12)
        node12.LeftChild = node10
        node11 = BSTNode(11, "11", node10)
        node10.RightChild = node11
        tree = BST(root)

        self.assertIs(tree.DeleteNodeByKey(8), True)

        self.assertIs(tree.Root, root)
        self.assert_node_state(root, 20, None, node10, node30)
        self.assert_node_state(node10, 10, root, node4, node16)
        self.assert_node_state(node4, 4, node10)
        self.assert_node_state(node16, 16, node10, node12)
        self.assert_node_state(node12, 12, node16, node11)
        self.assert_node_state(node11, 11, node12)
        self.assert_node_state(node30, 30, root)
        self.assertIs(tree.FindNodeByKey(8).NodeHasKey, False)

    def test_13(self):
        root = BSTNode(0, "0", None)
        node8 = BSTNode(8, "8", root)
        root.RightChild = node8
        node4 = BSTNode(4, "4", node8)
        node8.LeftChild = node4
        node16 = BSTNode(16, "16", node8)
        node8.RightChild = node16
        node12 = BSTNode(12, "12", node16)
        node16.LeftChild = node12
        node13 = BSTNode(13, "13", node12)
        node12.RightChild = node13
        tree = BST(root)

        self.assertIs(tree.DeleteNodeByKey(8), True)

        self.assertIs(tree.Root, root)
        self.assert_node_state(root, 0, None, None, node12)
        self.assert_node_state(node12, 12, root, node4, node16)
        self.assert_node_state(node4, 4, node12)
        self.assert_node_state(node16, 16, node12, node13)
        self.assert_node_state(node13, 13, node16)
        self.assertIs(tree.FindNodeByKey(8).NodeHasKey, False)


class TestCount(unittest.TestCase):

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

    def test_1(self):
        tree = BST(None)

        self.assertEqual(tree.Count(), 0)

    def test_2(self):
        root = BSTNode(0, "0", None)
        tree = BST(root)

        self.assertEqual(tree.Count(), 1)

    def test_3(self):
        self.assertEqual(self.tree.Count(), 7)

    def test_4(self):
        root = BSTNode(0, "0", None)
        node_minus1 = BSTNode(-1, "-1", root)
        root.LeftChild = node_minus1
        node_minus2 = BSTNode(-2, "-2", node_minus1)
        node_minus1.LeftChild = node_minus2
        tree = BST(root)

        self.assertEqual(tree.Count(), 3)

    def test_5(self):
        root = BSTNode(0, "0", None)
        node1 = BSTNode(1, "1", root)
        root.RightChild = node1
        node2 = BSTNode(2, "2", node1)
        node1.RightChild = node2
        tree = BST(root)

        self.assertEqual(tree.Count(), 3)

    def test_6(self):
        tree = BST(None)
        self.assertEqual(tree.Count(), 0)

        self.assertIs(tree.AddKeyValue(8, "8"), True)
        self.assertEqual(tree.Count(), 1)

        self.assertIs(tree.AddKeyValue(4, "4"), True)
        self.assertEqual(tree.Count(), 2)

        self.assertIs(tree.AddKeyValue(12, "12"), True)
        self.assertEqual(tree.Count(), 3)

        self.assertIs(tree.AddKeyValue(4, "other"), False)
        self.assertEqual(tree.Count(), 3)

    def test_7(self):
        self.assertEqual(self.tree.Count(), 7)

        self.assertIs(self.tree.DeleteNodeByKey(99), False)
        self.assertEqual(self.tree.Count(), 7)

        self.assertIs(self.tree.DeleteNodeByKey(2), True)
        self.assertEqual(self.tree.Count(), 6)

        self.assertIs(self.tree.DeleteNodeByKey(4), True)
        self.assertEqual(self.tree.Count(), 5)

        self.assertIs(self.tree.DeleteNodeByKey(12), True)
        self.assertEqual(self.tree.Count(), 4)

        self.assertIs(self.tree.DeleteNodeByKey(8), True)
        self.assertEqual(self.tree.Count(), 3)

        self.assertIs(self.tree.DeleteNodeByKey(6), True)
        self.assertEqual(self.tree.Count(), 2)

        self.assertIs(self.tree.DeleteNodeByKey(14), True)
        self.assertEqual(self.tree.Count(), 1)

        self.assertIs(self.tree.DeleteNodeByKey(10), True)
        self.assertEqual(self.tree.Count(), 0)
        self.assertIsNone(self.tree.Root)

    def assert_node_state(self, node, key, parent, left=None, right=None):
        self.assertEqual(node.NodeKey, key)
        self.assertEqual(node.NodeValue, str(key))
        self.assertIs(node.Parent, parent)
        self.assertIs(node.LeftChild, left)
        self.assertIs(node.RightChild, right)

    def test_8(self):
        self.assertEqual(self.tree.Count(), 7)
        self.assertEqual(self.tree.Count(), 7)

        self.assertIs(self.tree.Root, self.node8)
        self.assert_node_state(self.node8, 8, None, self.node4, self.node12)
        self.assert_node_state(self.node4, 4, self.node8, self.node2, self.node6)
        self.assert_node_state(self.node12, 12, self.node8, self.node10, self.node14)
        self.assert_node_state(self.node2, 2, self.node4)
        self.assert_node_state(self.node6, 6, self.node4)
        self.assert_node_state(self.node10, 10, self.node12)
        self.assert_node_state(self.node14, 14, self.node12)


class TestCompare(unittest.TestCase):

    def test_1(self) -> None:
        self.assertTrue(BSTComparable(None).Compare(BSTComparable(None)))

    def test_2(self) -> None:
        empty = BSTComparable(None)
        tree = BSTComparable(BSTNode(8, "8", None))
        self.assertFalse(empty.Compare(tree))
        self.assertFalse(tree.Compare(empty))

    def test_3(self) -> None:
        root = BSTNode(8, "8", None)
        root.LeftChild = BSTNode(4, "4", root)
        root.RightChild = BSTNode(12, "12", root)
        tree = BSTComparable(root)
        self.assertTrue(tree.Compare(tree))

    def test_4(self) -> None:
        firstRoot = BSTNode(8, "8", None)
        firstLeft = BSTNode(4, "4", firstRoot)
        firstRoot.LeftChild = firstLeft
        firstRoot.RightChild = BSTNode(12, "12", firstRoot)
        firstLeft.RightChild = BSTNode(6, "6", firstLeft)
        first = BSTComparable(firstRoot)

        secondRoot = BSTNode(8, "8", None)
        secondLeft = BSTNode(4, "4", secondRoot)
        secondRoot.LeftChild = secondLeft
        secondRoot.RightChild = BSTNode(12, "12", secondRoot)
        secondLeft.RightChild = BSTNode(6, "6", secondLeft)
        second = BSTComparable(secondRoot)
        self.assertIsNot(first.Root, second.Root)
        self.assertTrue(first.Compare(second))
        self.assertTrue(second.Compare(first))

    def test_5(self) -> None:
        firstRoot = BSTNode(8, "8", None)
        firstRoot.LeftChild = BSTNode(4, "4", firstRoot)
        firstRoot.RightChild = BSTNode(12, "12", firstRoot)
        first = BSTComparable(firstRoot)

        secondRoot = BSTNode(8, "8", None)
        secondRoot.LeftChild = BSTNode(4, "4", secondRoot)
        second = BSTComparable(secondRoot)
        self.assertFalse(first.Compare(second))
        self.assertFalse(second.Compare(first))

    def test_6(self) -> None:
        firstRoot = BSTNode(8, "8", None)
        firstRoot.LeftChild = BSTNode(4, "4", firstRoot)
        first = BSTComparable(firstRoot)

        secondRoot = BSTNode(8, "8", None)
        secondRoot.LeftChild = BSTNode(5, "5", secondRoot)
        second = BSTComparable(secondRoot)
        self.assertFalse(first.Compare(second))

    def test_7(self) -> None:
        firstRoot = BSTNode(8, "8", None)
        firstLeft = BSTNode(4, "4", firstRoot)
        firstRoot.LeftChild = firstLeft
        firstRoot.RightChild = BSTNode(12, "12", firstRoot)
        firstLeft.RightChild = BSTNode(6, "6", firstLeft)
        first = BSTComparable(firstRoot)

        secondRoot = BSTNode(8, "8", None)
        secondLeft = BSTNode(4, "4", secondRoot)
        secondRight = BSTNode(12, "12", secondRoot)
        secondGrandchild = BSTNode(6, "6", secondLeft)
        secondRoot.LeftChild = secondLeft
        secondRoot.RightChild = secondRight
        secondLeft.RightChild = secondGrandchild
        second = BSTComparable(secondRoot)

        secondGrandchild.NodeValue = "other"
        self.assertFalse(first.Compare(second))

    def test_8(self) -> None:
        firstRoot = BSTNode(8, "8", None)
        firstLeft = BSTNode(4, "4", firstRoot)
        firstRoot.LeftChild = firstLeft
        firstRoot.RightChild = BSTNode(12, "12", firstRoot)
        firstLeft.LeftChild = BSTNode(2, "2", firstLeft)
        firstLeft.RightChild = BSTNode(6, "6", firstLeft)
        first = BSTComparable(firstRoot)

        secondRoot = BSTNode(8, "8", None)
        node2 = BSTNode(2, "2", secondRoot)
        node4 = BSTNode(4, "4", node2)
        secondRoot.LeftChild = node2
        secondRoot.RightChild = BSTNode(12, "12", secondRoot)
        node2.RightChild = node4
        node4.RightChild = BSTNode(6, "6", node4)
        second = BSTComparable(secondRoot)
        self.assertFalse(first.Compare(second))

    def test_9(self) -> None:
        firstRoot = BSTNode(8, "8", None)
        firstLeft = BSTNode(4, "4", firstRoot)
        firstRight = BSTNode(12, "12", firstRoot)
        firstRoot.LeftChild = firstLeft
        firstRoot.RightChild = firstRight
        firstLeft.LeftChild = BSTNode(2, "2", firstLeft)
        firstLeft.RightChild = BSTNode(6, "6", firstLeft)
        firstRight.LeftChild = BSTNode(10, "10", firstRight)
        firstRight.RightChild = BSTNode(14, "14", firstRight)
        first = BSTComparable(firstRoot)

        secondRoot = BSTNode(8, "8", None)
        secondRight = BSTNode(12, "12", secondRoot)
        secondRight.RightChild = BSTNode(14, "14", secondRight)
        secondRight.LeftChild = BSTNode(10, "10", secondRight)
        secondLeft = BSTNode(4, "4", secondRoot)
        secondLeft.RightChild = BSTNode(6, "6", secondLeft)
        secondLeft.LeftChild = BSTNode(2, "2", secondLeft)
        secondRoot.RightChild = secondRight
        secondRoot.LeftChild = secondLeft
        second = BSTComparable(secondRoot)
        self.assertTrue(first.Compare(second))


class TestIsSymmetric(unittest.TestCase):

    def setUp(self) -> None:
        self.root = BSTNode(8, "8", None)
        self.left = BSTNode(4, "4", self.root)
        self.right = BSTNode(4, "4", self.root)
        self.leftOuter = BSTNode(2, "2", self.left)
        self.leftInner = BSTNode(6, "6", self.left)
        self.rightInner = BSTNode(6, "6", self.right)
        self.rightOuter = BSTNode(2, "2", self.right)
        self.root.LeftChild = self.left
        self.root.RightChild = self.right
        self.left.LeftChild = self.leftOuter
        self.left.RightChild = self.leftInner
        self.right.LeftChild = self.rightInner
        self.right.RightChild = self.rightOuter
        self.tree = BSTWithSymmetricCheck(self.root)

    def test_1(self) -> None:
        self.assertTrue(BSTWithSymmetricCheck(None).IsSymmetric())

    def test_2(self) -> None:
        root = BSTNode(8, "8", None)
        self.assertTrue(BSTWithSymmetricCheck(root).IsSymmetric())

    def test_3(self) -> None:
        root = BSTNode(8, "8", None)
        root.LeftChild = BSTNode(4, "4", root)
        self.assertFalse(BSTWithSymmetricCheck(root).IsSymmetric())

    def test_4(self) -> None:
        root = BSTNode(8, "8", None)
        root.RightChild = BSTNode(4, "4", root)
        self.assertFalse(BSTWithSymmetricCheck(root).IsSymmetric())

    def test_5(self) -> None:
        root = BSTNode(8, "8", None)
        root.LeftChild = BSTNode(4, "4", root)
        root.RightChild = BSTNode(4, "4", root)
        self.assertTrue(BSTWithSymmetricCheck(root).IsSymmetric())

    def test_6(self) -> None:
        self.assertTrue(self.tree.IsSymmetric())

    def test_7(self) -> None:
        self.left.RightChild = None
        self.right.LeftChild = None
        self.leftOuter.LeftChild = BSTNode(1, "1", self.leftOuter)
        self.rightOuter.RightChild = BSTNode(1, "1", self.rightOuter)
        self.assertTrue(self.tree.IsSymmetric())

    def test_8(self) -> None:
        self.left.LeftChild = None
        self.right.RightChild = None
        self.assertTrue(self.tree.IsSymmetric())

    def test_9(self) -> None:
        root = BSTNode(8, "7", None)
        left = BSTNode(4, "4", root)
        right = BSTNode(4, "4", root)
        root.LeftChild = left
        root.RightChild = right
        left.LeftChild = BSTNode(2, "2", left)
        right.LeftChild = BSTNode(2, "2", right)
        self.assertFalse(BSTWithSymmetricCheck(root).IsSymmetric())

    def test_10(self) -> None:
        self.left.LeftChild = None
        self.assertFalse(self.tree.IsSymmetric())

    def test_11(self) -> None:
        self.right.LeftChild = None
        self.rightOuter.LeftChild = self.rightInner
        self.rightInner.Parent = self.rightOuter
        self.assertFalse(self.tree.IsSymmetric())


class TestGetPathsByLength(unittest.TestCase):

    def setUp(self) -> None:
        self.root = BSTNode(8, "root", None)
        self.node4 = BSTNode(4, "4", self.root)
        self.node12 = BSTNode(12, "12", self.root)
        self.node2 = BSTNode(2, "2", self.node4)
        self.node6 = BSTNode(6, "6", self.node4)
        self.node7 = BSTNode(7, "7", self.node6)
        self.node10 = BSTNode(10, "10", self.node12)
        self.node14 = BSTNode(14, "14", self.node12)
        self.node13 = BSTNode(13, "13", self.node14)
        self.root.LeftChild = self.node4
        self.root.RightChild = self.node12
        self.node4.LeftChild = self.node2
        self.node4.RightChild = self.node6
        self.node6.RightChild = self.node7
        self.node12.LeftChild = self.node10
        self.node12.RightChild = self.node14
        self.node14.LeftChild = self.node13
        self.tree = BSTWithPathsOfLength(self.root)

    def test_1(self) -> None:
        tree = BSTWithPathsOfLength(None)
        self.assertEqual(tree.GetPathsByLength(0), [])
        self.assertEqual(tree.GetPathsByLength(2), [])

    def test_2(self) -> None:
        root = BSTNode(8, "root", None)
        tree = BSTWithPathsOfLength(root)
        self.assertEqual(tree.GetPathsByLength(0), [[root]])

    def test_3(self) -> None:
        root = BSTNode(8, "root", None)
        tree = BSTWithPathsOfLength(root)
        self.assertEqual(tree.GetPathsByLength(1), [])

    def test_4(self) -> None:
        self.assertEqual(self.tree.GetPathsByLength(2), [
            [self.root, self.node4, self.node2],
            [self.root, self.node12, self.node10],
        ])

    def test_5(self) -> None:
        self.assertEqual(self.tree.GetPathsByLength(3), [
            [self.root, self.node4, self.node6, self.node7],
            [self.root, self.node12, self.node14, self.node13],
        ])

    def test_6(self) -> None:
        self.assertEqual(self.tree.GetPathsByLength(0), [])
        self.assertEqual(self.tree.GetPathsByLength(1), [])

    def test_7(self) -> None:
        self.assertEqual(self.tree.GetPathsByLength(10), [])

    def test_8(self) -> None:
        self.assertEqual(self.tree.GetPathsByLength(-1), [])

    def test_9(self) -> None:
        root = BSTNode(3, "3", None)
        node2 = BSTNode(2, "2", root)
        node1 = BSTNode(1, "1", node2)
        root.LeftChild = node2
        node2.LeftChild = node1
        tree = BSTWithPathsOfLength(root)
        self.assertEqual(tree.GetPathsByLength(2), [[root, node2, node1]])

    def test_10(self) -> None:
        root = BSTNode(1, "1", None)
        node2 = BSTNode(2, "2", root)
        node3 = BSTNode(3, "3", node2)
        root.RightChild = node2
        node2.RightChild = node3
        tree = BSTWithPathsOfLength(root)
        self.assertEqual(tree.GetPathsByLength(2), [[root, node2, node3]])


class TestGetMaxSumPaths(unittest.TestCase):

    def setUp(self) -> None:
        self.root = BSTNode(8, 5, None)
        self.node4 = BSTNode(4, 3, self.root)
        self.node12 = BSTNode(12, 1, self.root)
        self.node2 = BSTNode(2, 4, self.node4)
        self.node6 = BSTNode(6, 2, self.node4)
        self.node10 = BSTNode(10, 6, self.node12)
        self.node14 = BSTNode(14, 1, self.node12)
        self.root.LeftChild = self.node4
        self.root.RightChild = self.node12
        self.node4.LeftChild = self.node2
        self.node4.RightChild = self.node6
        self.node12.LeftChild = self.node10
        self.node12.RightChild = self.node14
        self.tree = BSTWithMaxSumPaths(self.root)

    def test_1(self) -> None:
        self.assertEqual(BSTWithMaxSumPaths(None).GetMaxSumPaths(), [])

    def test_2(self) -> None:
        root = BSTNode(8, -3, None)
        tree = BSTWithMaxSumPaths(root)
        self.assertEqual(tree.GetMaxSumPaths(), [[root]])

    def test_3(self) -> None:
        self.assertEqual(self.tree.GetMaxSumPaths(), [
            [self.root, self.node4, self.node2],
            [self.root, self.node12, self.node10],
        ])

    def test_4(self) -> None:
        self.node10.NodeValue = 5
        self.assertEqual(self.tree.GetMaxSumPaths(), [
            [self.root, self.node4, self.node2],
        ])

    def test_5(self) -> None:
        self.node6.NodeValue = 4
        self.node14.NodeValue = 6
        self.assertEqual(self.tree.GetMaxSumPaths(), [
            [self.root, self.node4, self.node2],
            [self.root, self.node4, self.node6],
            [self.root, self.node12, self.node10],
            [self.root, self.node12, self.node14],
        ])

    def test_6(self) -> None:
        root = BSTNode(8, 1, None)
        left = BSTNode(4, 4, root)
        right = BSTNode(12, 1, root)
        leaf = BSTNode(10, 3, right)
        root.LeftChild = left
        root.RightChild = right
        right.LeftChild = leaf
        tree = BSTWithMaxSumPaths(root)
        self.assertEqual(tree.GetMaxSumPaths(), [[root, left], [root, right, leaf]])

    def test_7(self) -> None:
        root = BSTNode(8, -5, None)
        node4 = BSTNode(4, -2, root)
        node2 = BSTNode(2, -3, node4)
        root.LeftChild = node4
        node4.LeftChild = node2
        tree = BSTWithMaxSumPaths(root)
        self.assertEqual(tree.GetMaxSumPaths(), [[root, node4, node2]])

    def test_8(self) -> None:
        self.root.NodeValue = -5
        self.node4.NodeValue = -2
        self.node12.NodeValue = -1
        self.node2.NodeValue = -3
        self.node6.NodeValue = -7
        self.node10.NodeValue = -9
        self.node14.NodeValue = -4
        self.assertEqual(self.tree.GetMaxSumPaths(), [
            [self.root, self.node4, self.node2],
            [self.root, self.node12, self.node14],
        ])

    def test_9(self) -> None:
        root = BSTNode(8, 0, None)
        left = BSTNode(4, 0, root)
        right = BSTNode(12, 0, root)
        root.LeftChild = left
        root.RightChild = right
        tree = BSTWithMaxSumPaths(root)
        self.assertEqual(tree.GetMaxSumPaths(), [[root, left], [root, right]])

    def test_10(self) -> None:
        root = BSTNode(1, -1, None)
        node2 = BSTNode(2, -2, root)
        node3 = BSTNode(3, -3, node2)
        root.RightChild = node2
        node2.RightChild = node3
        tree = BSTWithMaxSumPaths(root)
        self.assertEqual(tree.GetMaxSumPaths(), [[root, node2, node3]])

    def test_11(self) -> None:
        root = BSTNode(8, 1, None)
        left = BSTNode(4, 100, root)
        right = BSTNode(12, 2, root)
        root.LeftChild = left
        root.RightChild = right
        left.LeftChild = BSTNode(2, -100, left)
        tree = BSTWithMaxSumPaths(root)
        self.assertEqual(tree.GetMaxSumPaths(), [[root, right]])
