from task1 import SimpleTree, SimpleTreeNode


# 1.1 Фиксируем уровни

class SimpleTreeNodeWithLevel(SimpleTreeNode):

    def __init__(self, val, parent, Level=None):
        super().__init__(val, parent)
        self.Level = Level


class SimpleTreeWithLevels(SimpleTree):

    def SetNodeLevels(self):
        if self.Root is None:
            return
        self.Root.Level = 0
        for child in self.Root.Children:
            self.SetNodeLevelsRecursive(child, 1)

    def SetNodeLevelsRecursive(self, Node, Level):
        Node.Level = Level
        for child in Node.Children:
            self.SetNodeLevelsRecursive(child, Level + 1)


# 1.2 Фиксируем уровни без анализа всего дерева

class SimpleTreeWithAutoLevels(SimpleTreeWithLevels):

    def AddChild(self, ParentNode, NewChild):
        super().AddChild(ParentNode, NewChild)
        if ParentNode.Level is None:
            self.SetNodeLevels() # можно обойтись без этого
        else:
            self.SetNodeLevelsRecursive(NewChild, ParentNode.Level + 1)
