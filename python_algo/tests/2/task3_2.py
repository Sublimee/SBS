from task3 import BST, BSTNode


# 3.3. Инвертирование дерева

class BSTWithInvert(BST):

    def Invert(self) -> None:
        self.InvertRecursive(self.Root)

    def InvertRecursive(self, node: BSTNode | None) -> None:
        if node is None:
            return

        left: BSTNode | None = node.LeftChild
        node.LeftChild = node.RightChild
        node.RightChild = left

        self.InvertRecursive(node.LeftChild)
        self.InvertRecursive(node.RightChild)


# 3.4. Уровень с максимальной суммой

class BSTWithMaxSumLevel(BST):

    def GetMaxSumLevel(self) -> int:
        if self.Root is None:
            return -1

        levelSums: list[int] = []
        levelNodes: list[BSTNode] = [self.Root]
        while len(levelNodes) > 0:
            levelSums.append(self.SumValues(levelNodes))
            levelNodes = self.GetChildren(levelNodes)

        return levelSums.index(max(levelSums))

    def SumValues(self, nodes: list[BSTNode]) -> int:
        result = 0
        for node in nodes:
            result += node.NodeValue
        return result

    def GetChildren(self, nodes: list[BSTNode]) -> list[BSTNode]:
        result: list[BSTNode] = []
        for node in nodes:
            if node.LeftChild is not None:
                result.append(node.LeftChild)
            if node.RightChild is not None:
                result.append(node.RightChild)
        return result


# 3.5. Восстановление дерева

# Префиксный и инфиксный обходы нужны для того, чтобы разобраться с формой дерева (в том числе с неполностью
# заполненными уровнями). Префиксный даёт информацию о корне дерева и в дальнейшем поддеревьев, а инфиксный с учётом
# этого знания покажет набор узлов левого и правого поддеревьев.

class BSTWithRestore(BST):

    def Restore(self, prefix: list[int], infix: list[int]) -> None:
        self.Root = self.RestoreRecursive(prefix, infix, None)

    def RestoreRecursive(self, prefix: list[int], infix: list[int], parent: BSTNode | None) -> BSTNode | None:
        if len(prefix) == 0:
            return None

        key = prefix[0]
        node = BSTNode(key, key, parent)

        middle = infix.index(key)
        node.LeftChild = self.RestoreRecursive(prefix[1:middle + 1], infix[:middle], node)
        node.RightChild = self.RestoreRecursive(prefix[middle + 1:], infix[middle + 1:], node)

        return node
