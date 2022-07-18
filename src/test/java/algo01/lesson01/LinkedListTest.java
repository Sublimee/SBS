package algo01.lesson01;

import org.example.algo01.lesson01.LinkedList;
import org.example.algo01.lesson01.Node;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class LinkedListTest {

    @Test
    void removeFirstElementFromManyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(1, 2, 3);

        Assertions.assertTrue(actualLinkedList.remove(1));
        Assertions.assertEquals(TestUtils.getLinkedList(2, 3), actualLinkedList);
    }

    @Test
    void removeMiddleElementFromManyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(1, 2, 3);

        Assertions.assertTrue(actualLinkedList.remove(2));
        Assertions.assertEquals(TestUtils.getLinkedList(1, 3), actualLinkedList);
    }

    @Test
    void removeLastElementFromManyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(1, 2, 3);

        Assertions.assertTrue(actualLinkedList.remove(3));
        Assertions.assertEquals(TestUtils.getLinkedList(1, 2), actualLinkedList);
    }

    @Test
    void removeFirstElementFromTwoTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(1, 2);

        Assertions.assertTrue(actualLinkedList.remove(1));
        Assertions.assertEquals(TestUtils.getLinkedList(2), actualLinkedList);
    }

    @Test
    void removeLastElementFromTwoTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(1, 2);

        Assertions.assertTrue(actualLinkedList.remove(2));
        Assertions.assertEquals(TestUtils.getLinkedList(1), actualLinkedList);
    }

    @Test
    void removeElementFromSingleTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(1);

        Assertions.assertTrue(actualLinkedList.remove(1));
        Assertions.assertEquals(TestUtils.getLinkedList(), actualLinkedList);
    }

    @Test
    void removeUnexpectedElementTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(1);

        Assertions.assertFalse(actualLinkedList.remove(2));
        Assertions.assertEquals(TestUtils.getLinkedList(1), actualLinkedList);
    }

    @Test
    void removeElementFromEmptyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList();

        Assertions.assertFalse(actualLinkedList.remove(1));
        Assertions.assertEquals(TestUtils.getLinkedList(), actualLinkedList);
    }

    @Test
    void clearNotEmptyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(1, 2, 3);
        actualLinkedList.clear();

        Assertions.assertEquals(TestUtils.getLinkedList(), actualLinkedList);
    }

    @Test
    void clearSingleTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(1);
        actualLinkedList.clear();

        Assertions.assertEquals(TestUtils.getLinkedList(), actualLinkedList);
    }

    @Test
    void clearEmptyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList();
        actualLinkedList.clear();

        Assertions.assertEquals(TestUtils.getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromManyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(1, 1, 1);
        actualLinkedList.removeAll(1);

        Assertions.assertEquals(TestUtils.getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromTwoTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(1, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(TestUtils.getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromSingleTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(TestUtils.getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromEmptyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList();

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(TestUtils.getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromComplexSequence1Test() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(1, 2, 1, 2, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(TestUtils.getLinkedList(2, 2), actualLinkedList);
    }

    @Test
    void removeAllFromComplexSequence2Test() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(2, 1, 2, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(TestUtils.getLinkedList(2, 2), actualLinkedList);
    }

    @Test
    void removeAllFromComplexSequence3Test() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(TestUtils.getLinkedList(2, 2, 2, 2, 2, 2, 2, 2), actualLinkedList);
    }

    @Test
    void insertAfterNoSpecifiedElementIntoEmptyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList();

        actualLinkedList.insertAfter(null, new Node(2));

        Assertions.assertEquals(TestUtils.getLinkedList(2), actualLinkedList);
    }

    @Test
    void insertAfterNoSpecifiedElementIntoSingleTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(1);

        actualLinkedList.insertAfter(null, new Node(2));

        Assertions.assertEquals(TestUtils.getLinkedList(2, 1), actualLinkedList);
    }

    @Test
    void insertAfterNoSpecifiedElementIntoManyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(2, 1);

        actualLinkedList.insertAfter(null, new Node(3));

        Assertions.assertEquals(TestUtils.getLinkedList(3, 2, 1), actualLinkedList);
    }

    @Test
    void insertAfterSpecifiedElementIntoSingleTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList();

        Node nodeAfter = new Node(2);
        actualLinkedList.addInTail(nodeAfter);
        actualLinkedList.insertAfter(nodeAfter, new Node(1));

        Assertions.assertEquals(TestUtils.getLinkedList(2, 1), actualLinkedList);
    }

    @Test
    void insertAfterFirstSpecifiedElementIntoManyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList();

        Node nodeAfter = new Node(1);
        actualLinkedList.addInTail(nodeAfter);
        actualLinkedList.addInTail(new Node(3));
        actualLinkedList.insertAfter(nodeAfter, new Node(2));

        Assertions.assertEquals(TestUtils.getLinkedList(1, 2, 3), actualLinkedList);
    }

    @Test
    void insertAfterLastSpecifiedElementIntoManyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList();

        Node nodeAfter = new Node(3);
        actualLinkedList.addInTail(new Node(1));
        actualLinkedList.addInTail(nodeAfter);
        actualLinkedList.insertAfter(nodeAfter, new Node(2));

        Assertions.assertEquals(TestUtils.getLinkedList(1, 3, 2), actualLinkedList);
    }

    @Test
    void findAllInManyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(2, 1, 2, 1, 2);

        Assertions.assertEquals(3, actualLinkedList.findAll(2).size());
        Assertions.assertEquals(2, actualLinkedList.findAll(1).size());
        Assertions.assertEquals(0, actualLinkedList.findAll(0).size());
    }

    @Test
    void findAllInEmptyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList();
        Assertions.assertEquals(0, actualLinkedList.findAll(2).size());
    }

    @Test
    void findInManyTest() {
        LinkedList actualLinkedList = TestUtils.getLinkedList(2, 1, 2, 4, 3);

        Assertions.assertEquals(1, actualLinkedList.find(2).next.value);
        Assertions.assertEquals(2, actualLinkedList.find(1).next.value);
        Assertions.assertNull(actualLinkedList.find(3).next);
    }

    @Test
    void findInEmptyTest() {
        Assertions.assertNull(TestUtils.getLinkedList().find(2));
    }

    @Test
    void countManyTest() {
        Assertions.assertEquals(5, TestUtils.getLinkedList(2, 1, 2, 1, 2).count());
    }

    @Test
    void countEmptyTest() {
        Assertions.assertEquals(0, TestUtils.getLinkedList().count());
    }

    @Test
    void countSingleTest() {
        Assertions.assertEquals(1, TestUtils.getLinkedList(1).count());
    }

}