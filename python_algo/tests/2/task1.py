class SimpleTreeNode:

    def __init__(self, val: int, parent: SimpleTreeNode | None):
        self.NodeValue: int = val
        self.Parent: SimpleTreeNode | None = parent
        self.Children: list[SimpleTreeNode] = []


class SimpleTree:

    def __init__(self, root: SimpleTreeNode | None):
        self.Root: SimpleTreeNode | None = root

    def AddChild(self, ParentNode: SimpleTreeNode, NewChild: SimpleTreeNode) -> None:
        NewChild.Parent = ParentNode
        ParentNode.Children.append(NewChild)

    def DeleteNode(self, NodeToDelete: SimpleTreeNode | None) -> None:
        if self.Root is None or self.Root == NodeToDelete or NodeToDelete is None:
            return
        self.DeleteNodeRecursive(self.Root, NodeToDelete)

    def DeleteNodeRecursive(self, NodeNext: SimpleTreeNode, NodeToDelete: SimpleTreeNode) -> None:
        thisNode = NodeNext
        if thisNode == NodeToDelete:
            thisNode.Parent.Children.remove(thisNode)
            thisNode.Parent = None
            return

        for child in thisNode.Children:
            self.DeleteNodeRecursive(child, NodeToDelete)

    def GetAllNodes(self) -> list[SimpleTreeNode]:
        if self.Root is None:
            return []
        result: list[SimpleTreeNode] = [self.Root]
        result.extend(self.GetAllNodesRecursive(self.Root.Children))
        return result

    def GetAllNodesRecursive(self, ChildrenNodes: list[SimpleTreeNode]) -> list[SimpleTreeNode]:
        result: list[SimpleTreeNode] = []
        for child in ChildrenNodes:
            result.append(child)
            result.extend(self.GetAllNodesRecursive(child.Children))
        return result

    def FindNodesByValue(self, val: int) -> list[SimpleTreeNode]:
        result: list[SimpleTreeNode] = []
        allNodes = self.GetAllNodes()
        for node in allNodes:
            if node.NodeValue == val:
                result.append(node)
        return result

    def MoveNode(self, OriginalNode: SimpleTreeNode, NewParent: SimpleTreeNode) -> None:
        self.DeleteNode(OriginalNode)
        self.AddChild(NewParent, OriginalNode)

    def Count(self) -> int:
        return len(self.GetAllNodes())

    def LeafCount(self) -> int:
        if self.Root is None:
            return 0

        return self.LeafCountRecursive(self.Root)

    def LeafCountRecursive(self, NextNode: SimpleTreeNode) -> int:
        result = 0
        if not NextNode.Children:
            return 1
        for child in NextNode.Children:
            result += self.LeafCountRecursive(child)
        return result
