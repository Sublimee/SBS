import java.util.*;

public class SimpleTreeNode<T> {
    public T NodeValue; // значение в узле
    public SimpleTreeNode<T> Parent; // родитель или null для корня
    public List<SimpleTreeNode<T>> Children; // список дочерних узлов или null
    public int level;

    public SimpleTreeNode(T val, SimpleTreeNode<T> parent) {
        NodeValue = val;
        Parent = parent;
        Children = null;
    }
}

class SimpleTree<T> {
    public SimpleTreeNode<T> Root; // корень, может быть null

    public SimpleTree(SimpleTreeNode<T> root) {
        Root = root;
    }

    public void AddChild(SimpleTreeNode<T> ParentNode, SimpleTreeNode<T> NewChild) {
        // ваш код добавления нового дочернего узла существующему ParentNode
        if (ParentNode.Children == null) {
            ParentNode.Children = new LinkedList<>();
        }

        NewChild.Parent = ParentNode;
        ParentNode.Children.add(NewChild);
    }

    public void DeleteNode(SimpleTreeNode<T> NodeToDelete) {
        // ваш код удаления существующего узла NodeToDelete
        NodeToDelete.Parent.Children.remove(NodeToDelete);
        NodeToDelete.Parent = null;
    }

    public List<SimpleTreeNode<T>> GetAllNodes() {
        // ваш код выдачи всех узлов дерева в определённом порядке
        return GetAllNodes(Root);
    }

    private List<SimpleTreeNode<T>> GetAllNodes(SimpleTreeNode<T> node) {
        if (node == null) {
            return Collections.emptyList();
        }

        List<SimpleTreeNode<T>> result = new LinkedList<>();
        result.add(node);

        if (node.Children == null) {
            return result;
        }

        node.Children.forEach(child -> result.addAll(GetAllNodes(child)));
        return result;
    }

    public List<SimpleTreeNode<T>> FindNodesByValue(T val) {
        // ваш код поиска узлов по значению
        return FindNodesByValue(val, Root);
    }

    private List<SimpleTreeNode<T>> FindNodesByValue(T val, SimpleTreeNode<T> node) {
        if (node == null) {
            return Collections.emptyList();
        }

        List<SimpleTreeNode<T>> result = new LinkedList<>();
        if (node.NodeValue.equals(val)) {
            result.add(node);
        }

        if (node.Children == null) {
            return result;
        }

        node.Children.forEach(child -> result.addAll(FindNodesByValue(val, child)));
        return result;
    }

    public void MoveNode(SimpleTreeNode<T> OriginalNode, SimpleTreeNode<T> NewParent) {
        // ваш код перемещения узла вместе с его поддеревом --
        // в качестве дочернего для узла NewParent
        DeleteNode(OriginalNode);
        AddChild(NewParent, OriginalNode);
    }

    public int Count() {
        // количество всех узлов в дереве
        return Count(Root);
    }

    private int Count(SimpleTreeNode<T> node) {
        // количество всех узлов в дереве
        if (node == null) {
            return 0;
        }

        int result = 1;
        if (node.Children == null) {
            return result;
        }

        for (SimpleTreeNode<T> child : node.Children) {
            result += Count(child);
        }

        return result;
    }

    public int LeafCount() {
        // количество листьев в дереве
        return LeafCount(Root);
    }

    private int LeafCount(SimpleTreeNode<T> node) {
        // количество листьев в дереве
        if (node == null) {
            return 0;
        }

        if (node.Children == null) {
            return 1;
        }

        int result = 0;
        for (SimpleTreeNode<T> child : node.Children) {
            result += LeafCount(child);
        }

        return result;
    }

    public void SetLevel() {
        SetLevel(Root, 0);
    }

    public void SetLevel(SimpleTreeNode<T> node, int level) {
        if (node == null) {
            return;
        }

        node.level = level;

        if (node.Children == null) {
            return;
        }

        for (SimpleTreeNode<T> child : node.Children) {
            SetLevel(child, level + 1);
        }
    }
}