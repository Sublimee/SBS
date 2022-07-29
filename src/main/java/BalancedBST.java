import java.util.*;
import java.util.stream.Collectors;

class BSTNode {
    public int NodeKey; // ключ узла
    public BSTNode Parent; // родитель или null для корня
    public BSTNode LeftChild; // левый потомок
    public BSTNode RightChild; // правый потомок
    public int Level; // глубина узла

    public BSTNode(int key, BSTNode parent) {
        NodeKey = key;
        Parent = parent;
        LeftChild = null;
        RightChild = null;
    }
}

class BalancedBST {
    public BSTNode Root; // корень дерева

    public BalancedBST() {
        Root = null;
    }

    public void GenerateTree(int[] a) {
        if (a == null) {
            return;
        }

        Arrays.sort(a);
        GenerateTree(a, null, 0, null);
    }

    private void GenerateTree(int[] a, BSTNode parent, int level, Boolean isLeft) {
        int aLength = a.length;
        if (aLength == 0) {
            return;
        }
        int middleIndex = aLength / 2;

        BSTNode nextParent = new BSTNode(a[middleIndex], parent);
        nextParent.Level = level;

        if (parent == null) {
            Root = nextParent;
        } else if (isLeft) {
            parent.LeftChild = nextParent;
        } else {
            parent.RightChild = nextParent;
        }

        GenerateTree(Arrays.copyOfRange(a, 0, middleIndex), nextParent, level + 1, true);
        GenerateTree(Arrays.copyOfRange(a, middleIndex + 1, aLength), nextParent, level + 1, false);
    }

    public boolean IsBalanced(BSTNode root_node) {
        try {
            getLevel(root_node);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    public int getLevel(BSTNode node) {
        if (node == null) {
            return 0;
        }

        int leftLevel = getLevel(node.LeftChild);
        int rightLevel = getLevel(node.RightChild);

        int diff = Math.abs(leftLevel - rightLevel);
        if (diff > 1) {
            throw new RuntimeException();
        }

        return 1 + diff;
    }

    ArrayList<Integer> WideAllNodes() {
        List<List<Integer>> nodesByLevel = new ArrayList<>();

        WideAllNodes(nodesByLevel, 0, Root);

        return nodesByLevel.stream()
                .filter(Objects::nonNull)
                .flatMap(List::stream)
                .collect(Collectors.toCollection(ArrayList::new));
    }

    void WideAllNodes(List<List<Integer>> nodesByLevel, int level, BSTNode node) {
        if (node == null) {
            return;
        }

        addWideNode(nodesByLevel, level, node);

        WideAllNodes(nodesByLevel, level + 1, node.LeftChild);
        WideAllNodes(nodesByLevel, level + 1, node.RightChild);
    }

    private void addWideNode(List<List<Integer>> nodesByLevel, int level, BSTNode node) {
        if (level >= nodesByLevel.size()) {
            List<Integer> newLevelNodes = new ArrayList<>();
            newLevelNodes.add(node.NodeKey);
            nodesByLevel.add(level, newLevelNodes);
        } else {
            List<Integer> levelNodes = nodesByLevel.get(level);
            levelNodes.add(node.NodeKey);
        }
    }
}