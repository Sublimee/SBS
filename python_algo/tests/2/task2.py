class BSTNode:

    def __init__(self, key: int, val: object, parent: BSTNode | None):
        self.NodeKey: int = key
        self.NodeValue: object = val
        self.Parent: BSTNode | None = parent
        self.LeftChild: BSTNode | None = None
        self.RightChild: BSTNode | None = None


class BSTFind:

    def __init__(self):
        self.Node: BSTNode | None = None

        self.NodeHasKey: bool = False
        self.ToLeft: bool = False


class BST:

    def __init__(self, node: BSTNode | None):
        self.Root: BSTNode | None = node

    def FindNodeByKey(self, key: int) -> BSTFind:
        return self.FindNodeByKeyRecursive(self.Root, key)

    def FindNodeByKeyRecursive(self, node: BSTNode | None, key: int) -> BSTFind:
        if node is None:
            return BSTFind()

        if node.NodeKey == key:
            result = BSTFind()
            result.Node = node
            result.NodeHasKey = True
            return result

        toLeft = key < node.NodeKey
        child = node.LeftChild if toLeft else node.RightChild
        result = self.FindNodeByKeyRecursive(child, key)

        if result.Node is None:
            result.Node = node
            result.ToLeft = toLeft

        return result

    def AddKeyValue(self, key: int, val: object) -> bool:
        candidate = self.FindNodeByKey(key)
        if candidate.Node is None:
            self.Root = BSTNode(key, val, None)
            return True

        if candidate.NodeHasKey:
            return False

        toLeft = candidate.ToLeft
        newNode = BSTNode(key, val, candidate.Node)
        if toLeft:
            candidate.Node.LeftChild = newNode
        else:
            candidate.Node.RightChild = newNode
        return True

    def FinMinMax(self, FromNode: BSTNode | None, FindMax: bool | None) -> BSTNode | None:
        if FromNode is None or FindMax is None:
            return None

        if FindMax:
            return self.FindMax(FindMax, FromNode)
        else:
            return self.FindMin(FindMax, FromNode)

    def FindMin(self, FindMax: bool | None, FromNode: BSTNode) -> BSTNode | None:
        if FromNode.LeftChild is not None:
            return self.FinMinMax(FromNode.LeftChild, FindMax)
        else:
            return FromNode

    def FindMax(self, FindMax: bool | None, FromNode: BSTNode) -> BSTNode | None:
        if FromNode.RightChild is not None:
            return self.FinMinMax(FromNode.RightChild, FindMax)
        else:
            return FromNode

    def DeleteNodeByKey(self, key: int) -> bool:
        candidate = self.FindNodeByKey(key)
        if not candidate.NodeHasKey or candidate.Node is None:
            return False

        node: BSTNode = candidate.Node

        if node.LeftChild is None or node.RightChild is None:
            self.ReplaceNode(node, node.LeftChild if node.LeftChild is not None else node.RightChild)
            return True

        swap: BSTNode | None = self.FinMinMax(node.RightChild, False)

        if swap is not node.RightChild:
            self.ReplaceNode(swap, swap.RightChild)
            swap.RightChild = node.RightChild
            swap.RightChild.Parent = swap

        swap.LeftChild = node.LeftChild
        swap.LeftChild.Parent = swap

        self.ReplaceNode(node, swap)
        return True

    def ReplaceNode(self, node: BSTNode, replacement: BSTNode | None) -> None:
        parent = node.Parent
        if parent is None:
            self.Root = replacement
        elif parent.LeftChild is node:
            parent.LeftChild = replacement
        else:
            parent.RightChild = replacement

        if replacement is not None:
            replacement.Parent = parent

    def Count(self) -> int:
        return self.CountRecursive(self.Root)

    def CountRecursive(self, node: BSTNode | None) -> int:
        if node is None:
            return 0
        return 1 + self.CountRecursive(node.LeftChild) + self.CountRecursive(node.RightChild)
