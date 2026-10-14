from task2 import BST, BSTNode


# 2.1. Метод сравнения деревьев

class BSTComparable(BST):

    def Compare(self, otherTree: BST | None) -> bool:
        return self.GetAllNodes() == self.GetAllNodesRecursive(otherTree.Root)

    def GetAllNodes(self) -> list[tuple[int, object]]:
        return self.GetAllNodesRecursive(self.Root)

    def GetAllNodesRecursive(self, node: BSTNode | None) -> list[tuple[int, object]]:
        if node is not None:
            return (
                    [(node.NodeKey, node.NodeValue)]
                    + self.GetAllNodesRecursive(node.LeftChild)
                    + self.GetAllNodesRecursive(node.RightChild)
            )
        else:
            return []


# 2.2. Метод сбора путей заданной величины

class BSTWithPathsOfLength(BST):

    def GetPathsByLength(self, length: int) -> list[list[BSTNode]]:
        return self.GetPathsByLengthRecursive(self.Root, length)

    def GetPathsByLengthRecursive(self, node: BSTNode | None, length: int) -> list[list[BSTNode]]:
        if node is None or length < 0:
            return []

        if length == 0:
            if node.LeftChild is None and node.RightChild is None:
                return [[node]]
            return []

        leftPaths = self.GetPathsByLengthRecursive(node.LeftChild, length - 1)
        rightPaths = self.GetPathsByLengthRecursive(node.RightChild, length - 1)
        allPaths = leftPaths + rightPaths
        result: list[list[BSTNode]] = []
        for path in allPaths:
            result.append([node] + path)
        return result


# 2.3. Метод сбора путей с максимальной суммой узлов

class BSTWithMaxSumPaths(BST):

    def GetMaxSumPaths(self) -> list[list[BSTNode]]:
        if self.Root is None:
            return []

        paths = self.GetPathsWithSumsRecursive(self.Root)
        maxSum = max(pathSum for pathSum, _ in paths)

        result: list[list[BSTNode]] = []
        for pathSum, path in paths:
            if pathSum == maxSum:
                result.append(path)
        return result

    def GetPathsWithSumsRecursive(self, node: BSTNode) -> list[tuple[int, list[BSTNode]]]:
        value = node.NodeValue

        if node.LeftChild is None and node.RightChild is None:
            return [(value, [node])]

        result: list[tuple[int, list[BSTNode]]] = []
        for child in (node.LeftChild, node.RightChild):
            if child is not None:
                childPaths = self.GetPathsWithSumsRecursive(child)
                for pathSum, path in childPaths:
                    result.append((value + pathSum, [node] + path))
        return result


# 2.4. Метод проверки симметричности

class BSTWithSymmetricCheck(BST):

    def IsSymmetric(self) -> bool:
        if self.Root is None:
            return True
        leftNodes = self.GetNodesForLeftDirection(self.Root.LeftChild, 1, True)
        rightNodes = self.GetNodesForRightDirection(self.Root.RightChild, 1, True)

        if len(leftNodes) != len(rightNodes):
            return False

        return leftNodes == rightNodes

    def GetNodesForLeftDirection(self, node: BSTNode | None, level: int, direction: bool) -> list[tuple[int, bool]]:
        if node is not None:
            return (
                    [(level, direction)]
                    + self.GetNodesForLeftDirection(node.LeftChild, level + 1, True)
                    + self.GetNodesForLeftDirection(node.RightChild, level + 1, False)
            )
        else:
            return []

    def GetNodesForRightDirection(self, node: BSTNode | None, level: int, direction: bool) -> list[tuple[int, bool]]:
        if node is not None:
            return (
                    [(level, direction)]
                    + self.GetNodesForRightDirection(node.RightChild, level + 1, True)
                    + self.GetNodesForRightDirection(node.LeftChild, level + 1, False)
            )
        else:
            return []
