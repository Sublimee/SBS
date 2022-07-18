import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.*;


public class SimpleTreeTest {

    @Test
    public void AddChildTest() {
        SimpleTreeNode<Integer> root = getSimpleTreeNode(1);
        SimpleTreeNode<Integer> second = getSimpleTreeNode(2);
        SimpleTreeNode<Integer> third = getSimpleTreeNode(3);
        SimpleTreeNode<Integer> fourth = getSimpleTreeNode(4);
        SimpleTreeNode<Integer> fifth = getSimpleTreeNode(5);

        SimpleTree<Integer> simpleTree = new SimpleTree<>(root);
        simpleTree.AddChild(root, second);
        simpleTree.AddChild(root, third);
        simpleTree.AddChild(second, fourth);
        simpleTree.AddChild(third, fifth);

        List<SimpleTreeNode<Integer>> nodes = simpleTree.GetAllNodes();

        Assertions.assertTrue(nodes.contains(root));
        Assertions.assertTrue(nodes.contains(second));
        Assertions.assertTrue(nodes.contains(third));
        Assertions.assertTrue(nodes.contains(fourth));
        Assertions.assertTrue(nodes.contains(fifth));

        Assertions.assertEquals(5, nodes.size());
        Assertions.assertEquals(simpleTree.Count(), nodes.size());
        Assertions.assertEquals(2, simpleTree.LeafCount());

        Assertions.assertArrayEquals(nodes.toArray(), simpleTree.GetAllNodes().toArray());
    }

    @Test
    public void DeleteNodeTest() {
        SimpleTreeNode<Integer> root = getSimpleTreeNode(1);
        SimpleTreeNode<Integer> second = getSimpleTreeNode(2);
        SimpleTreeNode<Integer> third = getSimpleTreeNode(3);
        SimpleTreeNode<Integer> fourth = getSimpleTreeNode(4);
        SimpleTreeNode<Integer> fifth = getSimpleTreeNode(5);

        SimpleTree<Integer> simpleTree = new SimpleTree<>(root);
        simpleTree.AddChild(root, second);
        simpleTree.AddChild(root, third);
        simpleTree.AddChild(second, fourth);
        simpleTree.AddChild(third, fifth);

        simpleTree.DeleteNode(second);
        simpleTree.DeleteNode(fifth);

        List<SimpleTreeNode<Integer>> nodes = simpleTree.GetAllNodes();

        Assertions.assertTrue(nodes.contains(root));
        Assertions.assertTrue(nodes.contains(third));

        Assertions.assertEquals(2, nodes.size());
        Assertions.assertEquals(simpleTree.Count(), nodes.size());
    }

    @Test
    public void FindNodesByValueTest() {
        SimpleTreeNode<Integer> root = getSimpleTreeNode(1);
        SimpleTreeNode<Integer> second = getSimpleTreeNode(2);
        SimpleTreeNode<Integer> otherSecond = getSimpleTreeNode(2);
        SimpleTreeNode<Integer> anotherSecond = getSimpleTreeNode(2);
        SimpleTreeNode<Integer> third = getSimpleTreeNode(3);
        SimpleTreeNode<Integer> fourth = getSimpleTreeNode(4);
        SimpleTreeNode<Integer> fifth = getSimpleTreeNode(5);

        SimpleTree<Integer> simpleTree = new SimpleTree<>(root);
        simpleTree.AddChild(root, second);
        simpleTree.AddChild(root, third);
        simpleTree.AddChild(second, fourth);
        simpleTree.AddChild(second, otherSecond);
        simpleTree.AddChild(third, fifth);
        simpleTree.AddChild(fifth, anotherSecond);

        List<SimpleTreeNode<Integer>> nodes = simpleTree.FindNodesByValue(2);

        Assertions.assertTrue(nodes.contains(second));
        Assertions.assertTrue(nodes.contains(otherSecond));
        Assertions.assertTrue(nodes.contains(anotherSecond));

        Assertions.assertEquals(3, nodes.size());
    }

    @Test
    public void MoveNodeTest() {
        SimpleTreeNode<Integer> root = getSimpleTreeNode(1);
        SimpleTreeNode<Integer> second = getSimpleTreeNode(2);
        SimpleTreeNode<Integer> third = getSimpleTreeNode(3);
        SimpleTreeNode<Integer> fourth = getSimpleTreeNode(4);
        SimpleTreeNode<Integer> fifth = getSimpleTreeNode(5);

        SimpleTree<Integer> simpleTree = new SimpleTree<>(root);
        simpleTree.AddChild(root, second);
        simpleTree.AddChild(root, third);
        simpleTree.AddChild(second, fourth);
        simpleTree.AddChild(third, fifth);

        simpleTree.MoveNode(second, fifth);

        List<SimpleTreeNode<Integer>> nodes = simpleTree.GetAllNodes();

        Assertions.assertTrue(nodes.contains(root));
        Assertions.assertTrue(nodes.contains(second));
        Assertions.assertTrue(nodes.contains(third));
        Assertions.assertTrue(nodes.contains(fourth));
        Assertions.assertTrue(nodes.contains(fifth));

        Assertions.assertEquals(fifth, second.Parent);
        Assertions.assertEquals(second, fifth.Children.get(0));
        Assertions.assertEquals(1, root.Children.size());

        Assertions.assertEquals(5, nodes.size());
    }

    @Test
    public void SetLevelTest() {
        SimpleTreeNode<Integer> root = getSimpleTreeNode(1);
        SimpleTreeNode<Integer> second = getSimpleTreeNode(2);
        SimpleTreeNode<Integer> third = getSimpleTreeNode(3);
        SimpleTreeNode<Integer> fourth = getSimpleTreeNode(4);
        SimpleTreeNode<Integer> fifth = getSimpleTreeNode(5);

        SimpleTree<Integer> simpleTree = new SimpleTree<>(root);
        simpleTree.AddChild(root, second);
        simpleTree.AddChild(root, third);
        simpleTree.AddChild(second, fourth);
        simpleTree.AddChild(third, fifth);

        simpleTree.SetLevel();

        Assertions.assertEquals(0, root.level);
        Assertions.assertEquals(1, second.level);
        Assertions.assertEquals(1, third.level);
        Assertions.assertEquals(2, fourth.level);
        Assertions.assertEquals(2, fifth.level);
    }

    private SimpleTreeNode<Integer> getSimpleTreeNode(int value) {
        return new SimpleTreeNode<>(value, null);
    }
}