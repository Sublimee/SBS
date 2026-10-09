import unittest
from task1 import SimpleTree, SimpleTreeNode
from task1_2 import SimpleTreeNodeWithLevel, SimpleTreeWithLevels, SimpleTreeWithAutoLevels


class TreeTestCase(unittest.TestCase):

    def setUp(self):
        self.root = SimpleTreeNode(1, None)
        self.first = SimpleTreeNode(2, self.root)
        self.second = SimpleTreeNode(2, self.root)
        self.third = SimpleTreeNode(3, self.first)
        self.fourth = SimpleTreeNode(4, self.first)
        self.fifth = SimpleTreeNode(3, self.second)
        self.sixth = SimpleTreeNode(5, self.third)
        self.root.Children = [self.first, self.second]
        self.first.Children = [self.third, self.fourth]
        self.second.Children = [self.fifth]
        self.third.Children = [self.sixth]
        self.tree = SimpleTree(self.root)
        self.nodes = [
            self.root, self.first, self.second, self.third,
            self.fourth, self.fifth, self.sixth,
        ]


class TestAddChild(TreeTestCase):

    def test_1(self):
        root = SimpleTreeNode(1, None)
        tree = SimpleTree(root)
        child = SimpleTreeNode(2, None)
        tree.AddChild(root, child)
        self.assertEqual(root.Children, [child])
        self.assertIs(child.Parent, root)
        self.assertIs(tree.Root, root)

    def test_2(self):
        child = SimpleTreeNode(6, None)
        self.tree.AddChild(self.root, child)
        self.assertEqual(self.root.Children, [self.first, self.second, child])
        self.assertIs(child.Parent, self.root)
        self.assertIs(self.first.Parent, self.root)
        self.assertIs(self.second.Parent, self.root)

    def test_3(self):
        child = SimpleTreeNode(6, None)
        self.tree.AddChild(self.sixth, child)
        self.assertEqual(self.sixth.Children, [child])
        self.assertIs(child.Parent, self.sixth)
        self.assertEqual(self.third.Children, [self.sixth])

    def test_4(self):
        child = SimpleTreeNode(2, None)
        self.tree.AddChild(self.root, child)
        self.assertEqual(self.root.Children, [self.first, self.second, child])
        self.assertIs(child.Parent, self.root)
        self.assertIsNot(child, self.first)
        self.assertIsNot(child, self.second)


class TestDeleteNode(TreeTestCase):

    def test_1(self):
        tree = SimpleTree(None)
        node = SimpleTreeNode(1, None)
        tree.DeleteNode(node)
        self.assertIsNone(tree.Root)
        self.assertIsNone(node.Parent)

    def test_2(self):
        self.tree.DeleteNode(None)
        self.assertEqual(self.root.Children, [self.first, self.second])
        self.assertCountEqual(self.tree.GetAllNodes(), self.nodes)

    def test_3(self):
        self.tree.DeleteNode(self.root)
        self.assertIs(self.tree.Root, self.root)
        self.assertIsNone(self.root.Parent)
        self.assertCountEqual(self.tree.GetAllNodes(), self.nodes)

    def test_4(self):
        self.tree.DeleteNode(self.fourth)
        self.assertEqual(self.first.Children, [self.third])
        self.assertIsNone(self.fourth.Parent)
        self.assertCountEqual(
            self.tree.GetAllNodes(),
            [self.root, self.first, self.second, self.third, self.fifth, self.sixth],
        )

    def test_5(self):
        self.tree.DeleteNode(self.first)
        self.assertEqual(self.root.Children, [self.second])
        self.assertIsNone(self.first.Parent)
        self.assertEqual(self.first.Children, [self.third, self.fourth])
        self.assertIs(self.third.Parent, self.first)
        self.assertIs(self.fourth.Parent, self.first)
        self.assertEqual(self.third.Children, [self.sixth])
        self.assertIs(self.sixth.Parent, self.third)
        self.assertCountEqual(
            self.tree.GetAllNodes(), [self.root, self.second, self.fifth],
        )

    def test_6(self):
        self.tree.DeleteNode(self.second)
        self.assertEqual(self.root.Children, [self.first])
        self.assertIs(self.first.Parent, self.root)
        self.assertIsNone(self.second.Parent)
        self.assertIs(self.fifth.Parent, self.second)
        self.assertCountEqual(
            self.tree.GetAllNodes(),
            [self.root, self.first, self.third, self.fourth, self.sixth],
        )

    def test_7(self):
        self.tree.DeleteNode(self.sixth)
        self.assertEqual(self.third.Children, [])
        self.assertIsNone(self.sixth.Parent)
        self.assertEqual(self.first.Children, [self.third, self.fourth])
        self.assertCountEqual(self.tree.GetAllNodes(), self.nodes[:-1])


class TestGetAllNodes(TreeTestCase):

    def test_1(self):
        self.assertEqual(SimpleTree(None).GetAllNodes(), [])

    def test_2(self):
        root = SimpleTreeNode(1, None)
        self.assertEqual(SimpleTree(root).GetAllNodes(), [root])

    def test_3(self):
        self.assertCountEqual(self.tree.GetAllNodes(), self.nodes)

    def test_4(self):
        parents = [node.Parent for node in self.nodes]
        children = [list(node.Children) for node in self.nodes]
        first_result = self.tree.GetAllNodes()
        second_result = self.tree.GetAllNodes()
        self.assertCountEqual(first_result, self.nodes)
        self.assertCountEqual(second_result, self.nodes)
        for node, parent, child_nodes in zip(self.nodes, parents, children):
            self.assertIs(node.Parent, parent)
            self.assertEqual(node.Children, child_nodes)

    def test_5(self):
        result = self.tree.GetAllNodes()
        result.clear()
        self.assertCountEqual(self.tree.GetAllNodes(), self.nodes)
        self.assertEqual(self.root.Children, [self.first, self.second])


class TestFindNodesByValue(TreeTestCase):

    def test_1(self):
        self.assertEqual(SimpleTree(None).FindNodesByValue(1), [])

    def test_2(self):
        self.assertEqual(self.tree.FindNodesByValue(99), [])

    def test_3(self):
        self.assertEqual(self.tree.FindNodesByValue(1), [self.root])

    def test_4(self):
        self.assertCountEqual(
            self.tree.FindNodesByValue(2), [self.first, self.second],
        )

    def test_5(self):
        self.assertCountEqual(
            self.tree.FindNodesByValue(3), [self.third, self.fifth],
        )
        self.assertEqual(self.tree.FindNodesByValue(5), [self.sixth])

    def test_6(self):
        self.tree.DeleteNode(self.first)
        self.assertEqual(self.tree.FindNodesByValue(2), [self.second])
        self.assertEqual(self.tree.FindNodesByValue(3), [self.fifth])
        self.assertEqual(self.tree.FindNodesByValue(5), [])


class TestMoveNode(TreeTestCase):

    def test_1(self):
        self.tree.MoveNode(self.fourth, self.second)
        self.assertNotIn(self.fourth, self.first.Children)
        self.assertEqual(self.first.Children, [self.third])
        self.assertEqual(self.second.Children, [self.fifth, self.fourth])
        self.assertIs(self.fourth.Parent, self.second)
        self.assertCountEqual(self.tree.GetAllNodes(), self.nodes)

    def test_2(self):
        self.tree.MoveNode(self.first, self.second)
        self.assertEqual(self.root.Children, [self.second])
        self.assertEqual(self.second.Children, [self.fifth, self.first])
        self.assertIs(self.first.Parent, self.second)
        self.assertEqual(self.first.Children, [self.third, self.fourth])
        self.assertIs(self.third.Parent, self.first)
        self.assertIs(self.fourth.Parent, self.first)
        self.assertEqual(self.third.Children, [self.sixth])
        self.assertIs(self.sixth.Parent, self.third)
        self.assertIs(self.tree.Root, self.root)
        self.assertCountEqual(self.tree.GetAllNodes(), self.nodes)

    def test_3(self):
        self.tree.MoveNode(self.third, self.root)
        self.assertEqual(self.first.Children, [self.fourth])
        self.assertEqual(self.root.Children, [self.first, self.second, self.third])
        self.assertIs(self.third.Parent, self.root)
        self.assertEqual(self.third.Children, [self.sixth])
        self.assertIs(self.sixth.Parent, self.third)
        self.assertCountEqual(self.tree.GetAllNodes(), self.nodes)

    def test_4(self):
        self.tree.MoveNode(self.second, self.sixth)
        self.assertEqual(self.root.Children, [self.first])
        self.assertEqual(self.sixth.Children, [self.second])
        self.assertIs(self.second.Parent, self.sixth)
        self.assertEqual(self.second.Children, [self.fifth])
        self.assertIs(self.fifth.Parent, self.second)
        self.assertCountEqual(self.tree.GetAllNodes(), self.nodes)


class TestCount(TreeTestCase):

    def test_1(self):
        self.assertEqual(SimpleTree(None).Count(), 0)

    def test_2(self):
        root = SimpleTreeNode(1, None)
        self.assertEqual(SimpleTree(root).Count(), 1)

    def test_3(self):
        self.assertEqual(self.tree.Count(), 7)

    def test_4(self):
        self.tree.AddChild(self.fourth, SimpleTreeNode(6, None))
        self.assertEqual(self.tree.Count(), 8)
        self.tree.DeleteNode(self.first)
        self.assertEqual(self.tree.Count(), 3)

    def test_5(self):
        self.tree.MoveNode(self.first, self.second)
        self.assertEqual(self.tree.Count(), 7)


class TestLeafCount(TreeTestCase):

    def test_1(self):
        self.assertEqual(SimpleTree(None).LeafCount(), 0)

    def test_2(self):
        root = SimpleTreeNode(1, None)
        self.assertEqual(SimpleTree(root).LeafCount(), 1)

    def test_3(self):
        root = SimpleTreeNode(1, None)
        first = SimpleTreeNode(2, root)
        second = SimpleTreeNode(3, first)
        root.Children = [first]
        first.Children = [second]
        self.assertEqual(SimpleTree(root).LeafCount(), 1)

    def test_4(self):
        self.assertEqual(self.tree.LeafCount(), 3)

    def test_5(self):
        self.tree.DeleteNode(self.sixth)
        self.assertEqual(self.tree.LeafCount(), 3)
        self.tree.DeleteNode(self.first)
        self.assertEqual(self.tree.LeafCount(), 1)
        self.tree.DeleteNode(self.second)
        self.assertEqual(self.tree.LeafCount(), 1)

    def test_6(self):
        self.tree.AddChild(self.fourth, SimpleTreeNode(6, None))
        self.assertEqual(self.tree.LeafCount(), 3)
        self.tree.AddChild(self.root, SimpleTreeNode(7, None))
        self.assertEqual(self.tree.LeafCount(), 4)

    def test_7(self):
        self.tree.MoveNode(self.fourth, self.sixth)
        self.assertEqual(self.tree.LeafCount(), 2)


class TestSetNodeLevels(unittest.TestCase):

    def setUp(self):
        self.root = SimpleTreeNodeWithLevel(1, None)
        self.first = SimpleTreeNodeWithLevel(2, self.root)
        self.second = SimpleTreeNodeWithLevel(2, self.root)
        self.third = SimpleTreeNodeWithLevel(3, self.first)
        self.fourth = SimpleTreeNodeWithLevel(4, self.first)
        self.fifth = SimpleTreeNodeWithLevel(3, self.second)
        self.sixth = SimpleTreeNodeWithLevel(5, self.third)
        self.root.Children = [self.first, self.second]
        self.first.Children = [self.third, self.fourth]
        self.second.Children = [self.fifth]
        self.third.Children = [self.sixth]
        self.tree = SimpleTreeWithLevels(self.root)
        self.nodes = [
            self.root, self.first, self.second, self.third,
            self.fourth, self.fifth, self.sixth,
        ]

    def test_1(self):
        tree = SimpleTreeWithLevels(None)
        tree.SetNodeLevels()
        self.assertIsNone(tree.Root)

    def test_2(self):
        root = SimpleTreeNodeWithLevel(1, None)
        tree = SimpleTreeWithLevels(root)
        tree.SetNodeLevels()
        self.assertEqual(root.Level, 0)

    def test_3(self):
        self.tree.SetNodeLevels()
        self.assertEqual(
            [node.Level for node in self.nodes], [0, 1, 1, 2, 2, 2, 3],
        )

    def test_4(self):
        root = SimpleTreeNodeWithLevel(1, None)
        first = SimpleTreeNodeWithLevel(2, root)
        second = SimpleTreeNodeWithLevel(3, first)
        third = SimpleTreeNodeWithLevel(4, second)
        root.Children = [first]
        first.Children = [second]
        second.Children = [third]
        tree = SimpleTreeWithLevels(root)
        tree.SetNodeLevels()
        self.assertEqual(
            [node.Level for node in [root, first, second, third]], [0, 1, 2, 3],
        )

    def test_5(self):
        self.tree.SetNodeLevels()
        self.tree.SetNodeLevels()
        self.assertEqual(
            [node.Level for node in self.nodes], [0, 1, 1, 2, 2, 2, 3],
        )
        for node in self.nodes:
            node.Level = 99
        self.tree.SetNodeLevels()
        self.assertEqual(
            [node.Level for node in self.nodes], [0, 1, 1, 2, 2, 2, 3],
        )

    def test_6(self):
        self.tree.SetNodeLevels()
        child = SimpleTreeNodeWithLevel(6, None)
        self.tree.AddChild(self.sixth, child)
        self.tree.SetNodeLevels()
        self.assertEqual(child.Level, 4)
        self.assertEqual(
            [node.Level for node in self.nodes], [0, 1, 1, 2, 2, 2, 3],
        )

    def test_7(self):
        self.tree.SetNodeLevels()
        self.tree.MoveNode(self.third, self.root)
        self.tree.SetNodeLevels()
        self.assertEqual(
            [node.Level for node in self.nodes], [0, 1, 1, 1, 2, 2, 2],
        )

    def test_8(self):
        self.tree.SetNodeLevels()
        self.tree.MoveNode(self.first, self.fifth)
        self.tree.SetNodeLevels()
        self.assertEqual(
            [node.Level for node in self.nodes], [0, 3, 1, 4, 4, 2, 5],
        )

    def test_9(self):
        parents = [node.Parent for node in self.nodes]
        children = [list(node.Children) for node in self.nodes]
        values = [node.NodeValue for node in self.nodes]
        self.tree.SetNodeLevels()
        self.assertIs(self.tree.Root, self.root)
        self.assertCountEqual(self.tree.GetAllNodes(), self.nodes)
        for node, parent, child_nodes, value in zip(
            self.nodes, parents, children, values,
        ):
            self.assertIs(node.Parent, parent)
            self.assertEqual(node.Children, child_nodes)
            self.assertEqual(node.NodeValue, value)


class TestAutoNodeLevels(unittest.TestCase):

    def setUp(self):
        self.root = SimpleTreeNodeWithLevel(1, None)
        self.first = SimpleTreeNodeWithLevel(2, self.root)
        self.second = SimpleTreeNodeWithLevel(2, self.root)
        self.third = SimpleTreeNodeWithLevel(3, self.first)
        self.fourth = SimpleTreeNodeWithLevel(4, self.first)
        self.fifth = SimpleTreeNodeWithLevel(3, self.second)
        self.sixth = SimpleTreeNodeWithLevel(5, self.third)
        self.root.Children = [self.first, self.second]
        self.first.Children = [self.third, self.fourth]
        self.second.Children = [self.fifth]
        self.third.Children = [self.sixth]
        self.tree = SimpleTreeWithAutoLevels(self.root)
        self.nodes = [
            self.root, self.first, self.second, self.third,
            self.fourth, self.fifth, self.sixth,
        ]

    def test_1(self):
        root = SimpleTreeNodeWithLevel(1, None)
        child = SimpleTreeNodeWithLevel(2, None)
        tree = SimpleTreeWithAutoLevels(root)
        tree.AddChild(root, child)
        self.assertEqual(root.Level, 0)
        self.assertEqual(child.Level, 1)

    def test_2(self):
        root = SimpleTreeNodeWithLevel(1, None, 0)
        child = SimpleTreeNodeWithLevel(2, None)
        grandchild = SimpleTreeNodeWithLevel(3, child)
        child.Children = [grandchild]
        tree = SimpleTreeWithAutoLevels(root)
        tree.AddChild(root, child)
        self.assertEqual(
            [root.Level, child.Level, grandchild.Level], [0, 1, 2],
        )
        self.assertIs(child.Parent, root)
        self.assertIs(grandchild.Parent, child)

    def test_3(self):
        self.tree.SetNodeLevels()
        child = SimpleTreeNodeWithLevel(6, None)
        self.tree.AddChild(self.sixth, child)
        self.assertEqual(child.Level, 4)
        self.assertEqual(
            [node.Level for node in self.nodes], [0, 1, 1, 2, 2, 2, 3],
        )

    def test_4(self):
        self.tree.SetNodeLevels()
        self.tree.MoveNode(self.first, self.fifth)
        self.assertEqual(
            [node.Level for node in self.nodes], [0, 3, 1, 4, 4, 2, 5],
        )
        self.assertEqual(self.root.Children, [self.second])
        self.assertEqual(self.fifth.Children, [self.first])
        self.assertIs(self.first.Parent, self.fifth)
        self.assertCountEqual(self.tree.GetAllNodes(), self.nodes)

    def test_5(self):
        self.tree.SetNodeLevels()
        self.tree.DeleteNode(self.first)
        self.assertEqual(
            [node.Level for node in [self.root, self.second, self.fifth]],
            [0, 1, 2],
        )
        self.assertCountEqual(
            self.tree.GetAllNodes(), [self.root, self.second, self.fifth],
        )
