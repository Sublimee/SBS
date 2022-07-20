import java.io.*;
import java.util.*;

class BSTNode<T> {
    public int NodeKey; // ключ узла
    public T NodeValue; // значение в узле
    public BSTNode<T> Parent; // родитель или null для корня
    public BSTNode<T> LeftChild; // левый потомок
    public BSTNode<T> RightChild; // правый потомок	

    public BSTNode(int key, T val, BSTNode<T> parent) {
        NodeKey = key;
        NodeValue = val;
        Parent = parent;
        LeftChild = null;
        RightChild = null;
    }
}

// промежуточный результат поиска
class BSTFind<T> {
    // null если в дереве вообще нет узлов
    public BSTNode<T> Node;

    // true если узел найден
    public boolean NodeHasKey;

    // true, если родительскому узлу надо добавить новый левым
    public boolean ToLeft;

    public BSTFind() {
        Node = null;
    }

    public BSTFind(BSTNode<T> Node, boolean NodeHasKey, boolean ToLeft) {
        this.Node = Node;
        this.NodeHasKey = NodeHasKey;
        this.ToLeft = ToLeft;
    }
}

class BST<T> {
    BSTNode<T> Root; // корень дерева, или null

    public BST(BSTNode<T> node) {
        Root = node;
    }

    public BSTFind<T> FindNodeByKey(int key) {
        // ищем в дереве узел и сопутствующую информацию по ключу
        if (Root == null) {
            return new BSTFind<>(null, false, false);
        }

        return FindNodeByKey(key, Root);
    }

    public BSTFind<T> FindNodeByKey(int key, BSTNode<T> node) {
        if (node.NodeKey == key) {
            return new BSTFind<>(node, true, false);
        }

        if (key < node.NodeKey) {
            if (node.LeftChild == null) {
                return new BSTFind<>(node, false, true);
            } else {
                return FindNodeByKey(key, node.LeftChild);
            }
        } else {
            if (node.RightChild == null) {
                return new BSTFind<>(node, false, false);
            } else {
                return FindNodeByKey(key, node.RightChild);
            }
        }
    }

    public boolean AddKeyValue(int key, T val) {
        // добавляем ключ-значение в дерево
        BSTFind<T> findNodeByKey = FindNodeByKey(key);

        if (findNodeByKey.Node == null) {
            Root = new BSTNode<>(key, val, null);
            return true;
        }

        if (findNodeByKey.NodeHasKey) {
            return false; // если ключ уже есть
        }

        BSTNode<T> parent = findNodeByKey.Node;
        BSTNode<T> child = new BSTNode<>(key, val, parent);

        if (findNodeByKey.ToLeft) {
            parent.LeftChild = child;
        } else {
            parent.RightChild = child;
        }

        return true;
    }

    public BSTNode<T> FinMinMax(BSTNode<T> FromNode, boolean FindMax) {
        // ищем максимальный/минимальный ключ в поддереве
        if (FromNode == null) {
            return null;
        }

        BSTNode<T> NextFromNode;
        if (FindMax) {
            NextFromNode = FromNode.RightChild;
        } else {
            NextFromNode = FromNode.LeftChild;
        }

        if (NextFromNode != null) {
            return FinMinMax(NextFromNode, FindMax);
        } else {
            return FromNode;
        }
    }

    public boolean DeleteNodeByKey(int key) {
        // удаляем узел по ключу
        BSTFind<T> findNodeByKey = FindNodeByKey(key);

        if (findNodeByKey.Node == null || !findNodeByKey.NodeHasKey) {
            return false;
        }

        BSTNode<T> nodeToDelete = findNodeByKey.Node;

        if (Root.NodeKey == nodeToDelete.NodeKey) {
            Root = null;
            return true;
        }

        if (nodeToDelete.LeftChild == null && nodeToDelete.RightChild == null) {
            removeFromParent(nodeToDelete, null);
            return true;
        }

        if (nodeToDelete.LeftChild != null && nodeToDelete.RightChild == null) {
            nodeToDelete.LeftChild.Parent = nodeToDelete.Parent;
            removeFromParent(nodeToDelete, nodeToDelete.LeftChild);
            return true;
        }

        if (nodeToDelete.LeftChild == null) {
            nodeToDelete.RightChild.Parent = nodeToDelete.Parent;
            removeFromParent(nodeToDelete, nodeToDelete.RightChild);
            return true;
        }

        BSTNode<T> minInRight = FinMinMax(nodeToDelete.RightChild, false);
        if (minInRight.RightChild == null) {
            minInRight.Parent.LeftChild = null;
        } else {
            minInRight.Parent.LeftChild = minInRight.RightChild;
        }

        minInRight.Parent = nodeToDelete.Parent;
        removeFromParent(nodeToDelete, minInRight);

        minInRight.LeftChild = nodeToDelete.LeftChild;
        nodeToDelete.LeftChild.Parent = minInRight;

        minInRight.RightChild = nodeToDelete.RightChild;
        nodeToDelete.RightChild.Parent = minInRight;

        return true;
    }

    private void removeFromParent(BSTNode<T> node, BSTNode<T> exchange) {
        if (node.Parent.LeftChild != null && node.Parent.LeftChild.NodeKey == node.NodeKey) {
            node.Parent.LeftChild = exchange;
        }
        if (node.Parent.RightChild != null && node.Parent.RightChild.NodeKey == node.NodeKey) {
            node.Parent.RightChild = exchange;
        }
    }

    public int Count() {
        // количество узлов в дереве
        if (Root == null) {
            return 0;
        }

        return Count(Root);
    }

    private int Count(BSTNode<T> node) {
        if (node == null) {
            return 0;
        }

        return 1 + Count(node.LeftChild) + Count(node.RightChild);
    }
}