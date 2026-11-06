# 6.1. Строим сбалансированное BST с уровнями узлов

# Рефлексия

# Используем тот же алгоритм, что и в предыдущем задании: сортируем массив -> рекурсивно выбираем середину каждого
# диапазона -> создаём узел и связываем его с родителем и потомками. Уровень вычисляем на основании знания об уровне
# родителя. При переходе на более глубокие уровни так же "отрезаем" от исходного отсортированного массива по два его
# поддерева.


class BSTNode:

    def __init__(self, key: int, parent: BSTNode | None):
        self.NodeKey: int = key
        self.Parent: BSTNode | None = parent
        self.LeftChild: BSTNode | None = None
        self.RightChild: BSTNode | None = None
        self.Level: int = 0


class BalancedBST:

    def __init__(self):
        self.Root: BSTNode | None = None

    # O(N log N) / O(N)
    def GenerateTree(self, a: list[int]) -> None:
        sortedValues: list[int] = sorted(a)
        self.Root = self.GenerateTreeRecursive(sortedValues, 0, len(sortedValues), None)

    def GenerateTreeRecursive(self, sortedValues: list[int], left: int, right: int,
                              parent: BSTNode | None) -> BSTNode | None:
        if left >= right:
            return None

        middle = (left + right) // 2
        node = BSTNode(sortedValues[middle], parent)
        if parent is not None:
            node.Level = parent.Level + 1

        node.LeftChild = self.GenerateTreeRecursive(sortedValues, left, middle, node)
        node.RightChild = self.GenerateTreeRecursive(sortedValues, middle + 1, right, node)
        return node

    # 6.3. Проверка сбалансированности дерева

    # Рефлексия

    # Обрабатываем дерево в порядке post-order. Поднимаясь, проверяем разницу между высотами левого и правого поддерева.
    # Если в какой-то момент разница высот между левым и правым поддеревьями оказалась больше 1, то дерево
    # несбалансировано. Если проверка прошла успешно, то текущая высота определяется высотой самого высокого поддерева.

    # O(N) / O(N)
    def IsBalanced(self, root_node: BSTNode | None) -> bool:
        return self.GetHeightRecursive(root_node) != -1

    def GetHeightRecursive(self, node: BSTNode | None) -> int:
        if node is None:
            return 0

        leftHeight = self.GetHeightRecursive(node.LeftChild)
        if leftHeight == -1:
            return -1

        rightHeight = self.GetHeightRecursive(node.RightChild)
        if rightHeight == -1:
            return -1

        if abs(leftHeight - rightHeight) > 1:
            return -1

        return max(leftHeight, rightHeight) + 1