import unittest
from collections.abc import Callable

from task2 import BST, BSTNode
from task4 import BSTBasedOnArray

# Рефлексия


# 2.2 и 2.3

# В исходных решениях обход дерева выполнялся индивидуально для каждой задачи. Выполнил наивную реализацию с рекурсивным
# сбором всех путей с их агрегатами и последующим применением результирующих функций. Передачу вычисления итогового
# результата в рекурсивный алгоритм не осилил в разумное время.

class BSTWithPaths(BST):

    def CollectPaths(self, step: Callable[[int, BSTNode], int], initial: int) -> list[tuple[int, list[BSTNode]]]:
        result: list[tuple[int, list[BSTNode]]] = []
        self.CollectPathsRecursive(self.Root, step, initial, [], result)
        return result

    def CollectPathsRecursive(
        self,
        node: BSTNode | None,
        step: Callable[[int, BSTNode], int],
        accumulator: int,
        path: list[BSTNode],
        result: list[tuple[int, list[BSTNode]]],
    ) -> None:
        if node is None:
            return

        accumulator = step(accumulator, node)
        path = path + [node]

        if node.LeftChild is None and node.RightChild is None:
            result.append((accumulator, path))
            return

        self.CollectPathsRecursive(node.LeftChild, step, accumulator, path, result)
        self.CollectPathsRecursive(node.RightChild, step, accumulator, path, result)

    def AddEdge(self, edges: int, node: BSTNode) -> int:
        return edges + 1

    def AddNodeValue(self, total: int, node: BSTNode) -> int:
        return total + node.NodeValue

    # O(N^2) / O(N^2)
    def GetPathsByLength(self, length: int) -> list[list[BSTNode]]:
        paths = self.CollectPaths(self.AddEdge, -1)
        result: list[list[BSTNode]] = []
        for edges, path in paths:
            if edges == length:
                result.append(path)
        return result

    # O(N^2) / O(N^2)
    def GetMaxSumPaths(self) -> list[list[BSTNode]]:
        paths = self.CollectPaths(self.AddNodeValue, 0)
        if len(paths) == 0:
            return []
        maxSum = max(total for total, _ in paths)
        result: list[list[BSTNode]] = []
        for total, path in paths:
            if total == maxSum:
                result.append(path)
        return result


class TestBSTWithPathsGetPathsByLength(unittest.TestCase):

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
        self.tree = BSTWithPaths(self.root)

    def test_1(self) -> None:
        tree = BSTWithPaths(None)
        self.assertEqual(tree.GetPathsByLength(0), [])
        self.assertEqual(tree.GetPathsByLength(2), [])

    def test_2(self) -> None:
        root = BSTNode(8, "root", None)
        tree = BSTWithPaths(root)
        self.assertEqual(tree.GetPathsByLength(0), [[root]])

    def test_3(self) -> None:
        root = BSTNode(8, "root", None)
        tree = BSTWithPaths(root)
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
        tree = BSTWithPaths(root)
        self.assertEqual(tree.GetPathsByLength(2), [[root, node2, node1]])

    def test_10(self) -> None:
        root = BSTNode(1, "1", None)
        node2 = BSTNode(2, "2", root)
        node3 = BSTNode(3, "3", node2)
        root.RightChild = node2
        node2.RightChild = node3
        tree = BSTWithPaths(root)
        self.assertEqual(tree.GetPathsByLength(2), [[root, node2, node3]])


class TestBSTWithPathsGetMaxSumPaths(unittest.TestCase):

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
        self.tree = BSTWithPaths(self.root)

    def test_1(self) -> None:
        self.assertEqual(BSTWithPaths(None).GetMaxSumPaths(), [])

    def test_2(self) -> None:
        root = BSTNode(8, -3, None)
        tree = BSTWithPaths(root)
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
        tree = BSTWithPaths(root)
        self.assertEqual(tree.GetMaxSumPaths(), [[root, left], [root, right, leaf]])

    def test_7(self) -> None:
        root = BSTNode(8, -5, None)
        node4 = BSTNode(4, -2, root)
        node2 = BSTNode(2, -3, node4)
        root.LeftChild = node4
        node4.LeftChild = node2
        tree = BSTWithPaths(root)
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
        tree = BSTWithPaths(root)
        self.assertEqual(tree.GetMaxSumPaths(), [[root, left], [root, right]])

    def test_10(self) -> None:
        root = BSTNode(1, -1, None)
        node2 = BSTNode(2, -2, root)
        node3 = BSTNode(3, -3, node2)
        root.RightChild = node2
        node2.RightChild = node3
        tree = BSTWithPaths(root)
        self.assertEqual(tree.GetMaxSumPaths(), [[root, node2, node3]])

    def test_11(self) -> None:
        root = BSTNode(8, 1, None)
        left = BSTNode(4, 100, root)
        right = BSTNode(12, 2, root)
        root.LeftChild = left
        root.RightChild = right
        left.LeftChild = BSTNode(2, -100, left)
        tree = BSTWithPaths(root)
        self.assertEqual(tree.GetMaxSumPaths(), [[root, right]])


# 2.4.

# В своём исходном решении не уловил идею правильного рекурсивного погружения на более глубокие уровни дерева (что и с
# чем сравнивать), поэтому не мог завершать работу алгоритма при нахождении расхождений формы вовремя, так как поздно
# фиксировал эти самые расхождения. Также не сравнивал сами значения, думая только о форме дерева.

# Исправленное решение:

class BSTWithSymmetricCheck(BST):

    # O(N) / O(N)
    def IsSymmetric(self) -> bool:
        if self.Root is None:
            return True
        return self.IsSymmetricRecursive(self.Root.LeftChild, self.Root.RightChild)

    def IsSymmetricRecursive(self, left: BSTNode | None, right: BSTNode | None) -> bool:
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        if left.NodeValue != right.NodeValue:
            return False
        return (
                self.IsSymmetricRecursive(left.LeftChild, right.RightChild)
                and self.IsSymmetricRecursive(left.RightChild, right.LeftChild)
        )


class TestBSTWithSymmetricCheckIsSymmetric(unittest.TestCase):

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

    def test_12(self) -> None:
        self.rightOuter.NodeValue = "3"
        self.assertFalse(self.tree.IsSymmetric())

    def test_13(self) -> None:
        root = BSTNode(8, "8", None)
        root.LeftChild = BSTNode(4, "4", root)
        root.RightChild = BSTNode(12, "12", root)
        self.assertFalse(BSTWithSymmetricCheck(root).IsSymmetric())


# 4.2. LCA

# Рефлексия

# Массив в отличие от нод неявно хранит информацию об уровнях ключей (либо надо сразу закладываться на уровни в
# рекурсивной реализации, либо делать автономные проходы по дереву). Если они есть, то алгоритмы "поочередного
# взбирания" к родителям очень похожи. Только в нашем случае это арифметика, а в случае рекурсивной схемы — переходы
# по ссылкам родителей.

class BSTBasedOnArrayWithLCA(BSTBasedOnArray):

    # O(log N) / O(1)
    def FindLCA(self, key1: int, key2: int) -> int | None:
        index1 = self.FindKeyIndex(key1)
        if index1 is None or index1 < 0 or self.Tree[index1] != key1:
            return None

        index2 = self.FindKeyIndex(key2)
        if index2 is None or index2 < 0 or self.Tree[index2] != key2:
            return None

        while index1 != index2:
            if index1 > index2:
                index1 = (index1 - 1) // 2
            else:
                index2 = (index2 - 1) // 2

        return index1

# 4.3. Обход в ширину

# Рефлексия

# Значения в массиве уже упорядочены по уровням. Нам остаётся только отфильтровать отсутствующие ноды.

class BSTBasedOnArrayWithWideAllNodes(BSTBasedOnArray):

    # O(N) / O(N)
    def WideAllNodes(self) -> tuple[int, ...]:
        keys: list[int] = []
        for key in self.Tree:
            if key is not None:
                keys.append(key)
        return tuple(keys)
