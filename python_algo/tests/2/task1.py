class SimpleTreeNode:

    def __init__(self, val, parent):
        self.NodeValue = val
        self.Parent = parent
        self.Children = []

class SimpleTree:

    def __init__(self, root):
        self.Root = root

    def AddChild(self, ParentNode, NewChild):
        NewChild.Parent = ParentNode
        ParentNode.Children.append(NewChild)

    def DeleteNode(self, NodeToDelete):
        if self.Root is None or self.Root == NodeToDelete or NodeToDelete is None:
            return
        self.DeleteNodeRecursive(self.Root, NodeToDelete)

    def DeleteNodeRecursive(self, NodeNext, NodeToDelete):
        thisNode = NodeNext
        if thisNode == NodeToDelete:
            thisNode.Parent.Children.remove(thisNode)
            thisNode.Parent = None
            return

        for child in thisNode.Children:
            self.DeleteNodeRecursive(child, NodeToDelete)

    def GetAllNodes(self):
        if self.Root is None:
            return []
        result = [self.Root]
        result.extend(self.GetAllNodesRecursive(self.Root.Children))
        return result

    def GetAllNodesRecursive(self, ChildrenNodes):
        result = []
        for child in ChildrenNodes:
            result.append(child)
            result.extend(self.GetAllNodesRecursive(child.Children))
        return result

    def FindNodesByValue(self, val):
        result = []
        allNodes = self.GetAllNodes()
        for node in allNodes:
            if node.NodeValue == val:
                result.append(node)
        return result

    def MoveNode(self, OriginalNode, NewParent):
        self.DeleteNode(OriginalNode)
        self.AddChild(NewParent, OriginalNode)

    def Count(self):
        return len(self.GetAllNodes())

    def LeafCount(self):
        if self.Root is None:
            return 0

        return self.LeafCountRecursive(self.Root)

    def LeafCountRecursive(self, NextNode):
        result = 0
        if not NextNode.Children:
            return 1
        for child in NextNode.Children:
            result += self.LeafCountRecursive(child)
        return result
