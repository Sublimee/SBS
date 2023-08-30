import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.*;

public class BalancedBSTTest {

    /* fix
    @Test
    void nullInputArrayTest() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(null);
        Assertions.assertTrue(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void emptyInputArrayTest() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray());

        Assertions.assertEquals(List.of(), balancedBST.WideAllNodes());
        Assertions.assertTrue(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void onlyElementInputArrayTest() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1));

        Assertions.assertEquals(List.of(1), balancedBST.WideAllNodes());
        Assertions.assertTrue(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void twoElementsInputArrayTest() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2));

        Assertions.assertEquals(List.of(2, 1), balancedBST.WideAllNodes());
        Assertions.assertTrue(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void threeElementsInputArrayTest() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(3, 2, 1));

        Assertions.assertEquals(List.of(2, 1, 3), balancedBST.WideAllNodes());
        Assertions.assertTrue(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void sevenElementsInputArrayTest() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));

        Assertions.assertEquals(List.of(4, 2, 6, 1, 3, 5, 7), balancedBST.WideAllNodes());
        Assertions.assertTrue(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void seven_array2() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        balancedBST.Root.LeftChild.LeftChild.RightChild = new BSTNode(0, balancedBST.Root.LeftChild.LeftChild);
        Assertions.assertTrue(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void seven_array3() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        balancedBST.Root.LeftChild.RightChild.LeftChild = new BSTNode(0, balancedBST.Root.LeftChild.RightChild);
        Assertions.assertTrue(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void seven_array4() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        balancedBST.Root.LeftChild.RightChild.LeftChild = new BSTNode(0, balancedBST.Root.LeftChild.RightChild);
        Assertions.assertTrue(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void seven_array5() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        balancedBST.Root.RightChild.LeftChild.LeftChild = new BSTNode(0, balancedBST.Root.RightChild.LeftChild);
        Assertions.assertTrue(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void seven_array6() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        balancedBST.Root.RightChild.LeftChild.RightChild = new BSTNode(0, balancedBST.Root.RightChild.LeftChild);
        Assertions.assertTrue(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void seven_array7() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        balancedBST.Root.RightChild.RightChild.LeftChild = new BSTNode(0, balancedBST.Root.RightChild.RightChild);
        Assertions.assertTrue(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void seven_array8() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        balancedBST.Root.RightChild.RightChild.LeftChild = new BSTNode(0, balancedBST.Root.RightChild.RightChild);
        Assertions.assertTrue(balancedBST.IsBalanced(balancedBST.Root));
    }


    @Test
    void seven_array10() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        BSTNode newNode = new BSTNode(0, balancedBST.Root.LeftChild.LeftChild);
        balancedBST.Root.LeftChild.LeftChild.LeftChild = newNode;
        newNode.LeftChild = new BSTNode(0, newNode);
        Assertions.assertFalse(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void seven_array20() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        BSTNode rightChild = new BSTNode(0, balancedBST.Root.LeftChild.LeftChild);
        balancedBST.Root.LeftChild.LeftChild.RightChild = rightChild;
        rightChild.RightChild = new BSTNode(0, rightChild);
        Assertions.assertFalse(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void seven_array30() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        BSTNode newNode = new BSTNode(0, balancedBST.Root.LeftChild.RightChild);
        balancedBST.Root.LeftChild.RightChild.LeftChild = newNode;
        newNode.LeftChild = new BSTNode(0, newNode);
        Assertions.assertFalse(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void seven_array40() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        BSTNode newNode = new BSTNode(0, balancedBST.Root.LeftChild.RightChild);
        balancedBST.Root.LeftChild.RightChild.RightChild = newNode;
        newNode.RightChild = new BSTNode(0, newNode);
        Assertions.assertFalse(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void seven_array50() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        BSTNode newNode = new BSTNode(0, balancedBST.Root.RightChild.LeftChild);
        balancedBST.Root.RightChild.LeftChild.LeftChild = newNode;
        newNode.LeftChild = new BSTNode(0, newNode);
        Assertions.assertFalse(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void seven_array60() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        BSTNode rightChild = new BSTNode(0, balancedBST.Root.RightChild.LeftChild);
        balancedBST.Root.RightChild.LeftChild.RightChild = rightChild;
        rightChild.RightChild = new BSTNode(0, rightChild);
        Assertions.assertFalse(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void seven_array70() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        BSTNode newNode = new BSTNode(0, balancedBST.Root.RightChild.RightChild);
        balancedBST.Root.RightChild.RightChild.LeftChild = newNode;
        newNode.LeftChild = new BSTNode(0, newNode);
        Assertions.assertFalse(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void seven_array80() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 2, 3, 4, 5, 6, 7));
        BSTNode newNode = new BSTNode(0, balancedBST.Root.RightChild.RightChild);
        newNode.RightChild = new BSTNode(0, newNode);
        balancedBST.Root.RightChild.RightChild.RightChild = newNode;
        Assertions.assertFalse(balancedBST.IsBalanced(balancedBST.Root));
    }

    @Test
    void fifth_array() {
        BalancedBST balancedBST = new BalancedBST();
        balancedBST.GenerateTree(getArray(1, 1, 1, 1, 1, 1, 1));
        Assertions.assertTrue(balancedBST.IsBalanced(balancedBST.Root));
    }
    */

    private int[] getArray(int... expected) {
        return expected;
    }
}