package algo01.lesson02;

import org.example.algo01.lesson02.DoubledLinkedList;
import org.example.algo01.lesson02.Node;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class DoubledLinkedListTest {

    @Test
    void removeFirstElementFromManyTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(1, 2, 3);

        actualLinkedList.remove(1);

        Assertions.assertEquals(getLinkedList(2, 3), actualLinkedList);
    }

    @Test
    void removeMiddleElementFromManyTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(1, 2, 3);

        actualLinkedList.remove(2);

        Assertions.assertEquals(getLinkedList(1, 3), actualLinkedList);
    }

    @Test
    void removeLastElementFromManyTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(1, 2, 3);

        actualLinkedList.remove(3);

        Assertions.assertEquals(getLinkedList(1, 2), actualLinkedList);
    }

    @Test
    void removeFirstElementFromTwoTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(1, 2);

        actualLinkedList.remove(1);

        Assertions.assertEquals(getLinkedList(2), actualLinkedList);
    }

    @Test
    void removeLastElementFromTwoTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(1, 2);

        actualLinkedList.remove(2);

        Assertions.assertEquals(getLinkedList(1), actualLinkedList);
    }

    @Test
    void removeElementFromSingleTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(1);

        actualLinkedList.remove(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeUnexpectedElementTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(1);

        actualLinkedList.remove(2);

        Assertions.assertEquals(getLinkedList(1), actualLinkedList);
    }

    @Test
    void removeElementFromEmptyTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(1);

        actualLinkedList.remove(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void clearNotEmptyTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(1, 2, 3);
        actualLinkedList.clear();

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void clearSingleTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(1);
        actualLinkedList.clear();

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void clearEmptyTest() {
        DoubledLinkedList actualLinkedList = getLinkedList();
        actualLinkedList.clear();

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromManyTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(1, 1, 1);
        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromTwoTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(1, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromSingleTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromEmptyTest() {
        DoubledLinkedList actualLinkedList = getLinkedList();

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromComplexSequence1Test() {
        DoubledLinkedList actualLinkedList = getLinkedList(1, 2, 1, 2, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(2, 2), actualLinkedList);
    }

    @Test
    void removeAllFromComplexSequence2Test() {
        DoubledLinkedList actualLinkedList = getLinkedList(2, 1, 2, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(2, 2), actualLinkedList);
    }

    @Test
    void removeAllFromComplexSequence3Test() {
        DoubledLinkedList actualLinkedList = getLinkedList(2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(2, 2, 2, 2, 2, 2, 2, 2), actualLinkedList);
    }

    @Test
    void insertAfterNoSpecifiedElementIntoEmptyTest() {
        DoubledLinkedList actualLinkedList = getLinkedList();

        actualLinkedList.insertAfter(null, new Node(2));

        Assertions.assertEquals(getLinkedList(2), actualLinkedList);
    }

    @Test
    void insertAfterNoSpecifiedElementIntoSingleTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(1);

        actualLinkedList.insertAfter(null, new Node(2));

        Assertions.assertEquals(getLinkedList(2, 1), actualLinkedList);
    }

    @Test
    void insertAfterNoSpecifiedElementIntoManyTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(2, 1);

        actualLinkedList.insertAfter(null, new Node(3));

        Assertions.assertEquals(getLinkedList(3, 2, 1), actualLinkedList);
    }

    @Test
    void insertAfterSpecifiedElementIntoSingleTest() {
        DoubledLinkedList actualLinkedList = getLinkedList();

        Node nodeAfter = new Node(2);
        actualLinkedList.addInTail(nodeAfter);
        actualLinkedList.insertAfter(nodeAfter, new Node(1));

        Assertions.assertEquals(getLinkedList(2, 1), actualLinkedList);
    }

    @Test
    void insertAfterFirstSpecifiedElementIntoManyTest() {
        DoubledLinkedList actualLinkedList = getLinkedList();

        Node nodeAfter = new Node(1);
        actualLinkedList.addInTail(nodeAfter);
        actualLinkedList.addInTail(new Node(3));
        actualLinkedList.insertAfter(nodeAfter, new Node(2));

        Assertions.assertEquals(getLinkedList(1, 2, 3), actualLinkedList);
    }

    @Test
    void insertAfterLastSpecifiedElementIntoManyTest() {
        DoubledLinkedList actualLinkedList = getLinkedList();

        Node nodeAfter = new Node(3);
        actualLinkedList.addInTail(new Node(1));
        actualLinkedList.addInTail(nodeAfter);
        actualLinkedList.insertAfter(nodeAfter, new Node(2));

        Assertions.assertEquals(getLinkedList(1, 3, 2), actualLinkedList);
    }

    @Test
    void findAllInManyTest() {
        DoubledLinkedList actualLinkedList = getLinkedList(2, 1, 2, 1, 2);

        Assertions.assertEquals(3, actualLinkedList.findAll(2).size());
        Assertions.assertEquals(2, actualLinkedList.findAll(1).size());
        Assertions.assertEquals(0, actualLinkedList.findAll(0).size());
    }

    @Test
    void findAllInEmptyTest() {
        DoubledLinkedList actualLinkedList = getLinkedList();
        Assertions.assertEquals(0, actualLinkedList.findAll(2).size());
    }

    @Test
    void countManyTest() {
        Assertions.assertEquals(5, getLinkedList(2, 1, 2, 1, 2).count());
    }

    @Test
    void countEmptyTest() {
        Assertions.assertEquals(0, getLinkedList().count());
    }

    @Test
    void countSingleTest() {
        Assertions.assertEquals(1, getLinkedList(1).count());
    }

    private DoubledLinkedList getLinkedList(int... values) {
        DoubledLinkedList linkedList = new DoubledLinkedList();
        for (Integer value : values) {
            linkedList.addInTail(new Node(value));
        }
        return linkedList;
    }
}