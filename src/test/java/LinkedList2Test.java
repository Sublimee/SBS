import org.example.lesson02.LinkedList2;
import org.example.lesson02.Node;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class LinkedList2Test {

    @Test
    void removeFirstElementFromManyTest() {
        LinkedList2 actualLinkedList = getLinkedList(1, 2, 3);

        actualLinkedList.remove(1);

        Assertions.assertEquals(getLinkedList(2, 3), actualLinkedList);
    }

    @Test
    void removeMiddleElementFromManyTest() {
        LinkedList2 actualLinkedList = getLinkedList(1, 2, 3);

        actualLinkedList.remove(2);

        Assertions.assertEquals(getLinkedList(1, 3), actualLinkedList);
    }

    @Test
    void removeLastElementFromManyTest() {
        LinkedList2 actualLinkedList = getLinkedList(1, 2, 3);

        actualLinkedList.remove(3);

        Assertions.assertEquals(getLinkedList(1, 2), actualLinkedList);
    }

    @Test
    void removeFirstElementFromTwoTest() {
        LinkedList2 actualLinkedList = getLinkedList(1, 2);

        actualLinkedList.remove(1);

        Assertions.assertEquals(getLinkedList(2), actualLinkedList);
    }

    @Test
    void removeLastElementFromTwoTest() {
        LinkedList2 actualLinkedList = getLinkedList(1, 2);

        actualLinkedList.remove(2);

        Assertions.assertEquals(getLinkedList(1), actualLinkedList);
    }

    @Test
    void removeElementFromSingleTest() {
        LinkedList2 actualLinkedList = getLinkedList(1);

        actualLinkedList.remove(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeUnexpectedElementTest() {
        LinkedList2 actualLinkedList = getLinkedList(1);

        actualLinkedList.remove(2);

        Assertions.assertEquals(getLinkedList(1), actualLinkedList);
    }

    @Test
    void removeElementFromEmptyTest() {
        LinkedList2 actualLinkedList = getLinkedList(1);

        actualLinkedList.remove(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void clearNotEmptyTest() {
        LinkedList2 actualLinkedList = getLinkedList(1, 2, 3);
        actualLinkedList.clear();

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void clearSingleTest() {
        LinkedList2 actualLinkedList = getLinkedList(1);
        actualLinkedList.clear();

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void clearEmptyTest() {
        LinkedList2 actualLinkedList = getLinkedList();
        actualLinkedList.clear();

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromManyTest() {
        LinkedList2 actualLinkedList = getLinkedList(1, 1, 1);
        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromTwoTest() {
        LinkedList2 actualLinkedList = getLinkedList(1, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromSingleTest() {
        LinkedList2 actualLinkedList = getLinkedList(1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromEmptyTest() {
        LinkedList2 actualLinkedList = getLinkedList();

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromComplexSequence1Test() {
        LinkedList2 actualLinkedList = getLinkedList(1, 2, 1, 2, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(2, 2), actualLinkedList);
    }

    @Test
    void removeAllFromComplexSequence2Test() {
        LinkedList2 actualLinkedList = getLinkedList(2, 1, 2, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(2, 2), actualLinkedList);
    }

    @Test
    void removeAllFromComplexSequence3Test() {
        LinkedList2 actualLinkedList = getLinkedList(2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(2, 2, 2, 2, 2, 2, 2, 2), actualLinkedList);
    }

    @Test
    void insertAfterNoSpecifiedElementIntoEmptyTest() {
        LinkedList2 actualLinkedList = getLinkedList();

        actualLinkedList.insertAfter(null, new Node(2));

        Assertions.assertEquals(getLinkedList(2), actualLinkedList);
    }

    @Test
    void insertAfterNoSpecifiedElementIntoSingleTest() {
        LinkedList2 actualLinkedList = getLinkedList(1);

        actualLinkedList.insertAfter(null, new Node(2));

        Assertions.assertEquals(getLinkedList(2, 1), actualLinkedList);
    }

    @Test
    void insertAfterNoSpecifiedElementIntoManyTest() {
        LinkedList2 actualLinkedList = getLinkedList(2, 1);

        actualLinkedList.insertAfter(null, new Node(3));

        Assertions.assertEquals(getLinkedList(3, 2, 1), actualLinkedList);
    }

    @Test
    void insertAfterSpecifiedElementIntoSingleTest() {
        LinkedList2 actualLinkedList = getLinkedList();

        Node nodeAfter = new Node(2);
        actualLinkedList.addInTail(nodeAfter);
        actualLinkedList.insertAfter(nodeAfter, new Node(1));

        Assertions.assertEquals(getLinkedList(2, 1), actualLinkedList);
    }

    @Test
    void insertAfterFirstSpecifiedElementIntoManyTest() {
        LinkedList2 actualLinkedList = getLinkedList();

        Node nodeAfter = new Node(1);
        actualLinkedList.addInTail(nodeAfter);
        actualLinkedList.addInTail(new Node(3));
        actualLinkedList.insertAfter(nodeAfter, new Node(2));

        Assertions.assertEquals(getLinkedList(1, 2, 3), actualLinkedList);
    }

    @Test
    void insertAfterLastSpecifiedElementIntoManyTest() {
        LinkedList2 actualLinkedList = getLinkedList();

        Node nodeAfter = new Node(3);
        actualLinkedList.addInTail(new Node(1));
        actualLinkedList.addInTail(nodeAfter);
        actualLinkedList.insertAfter(nodeAfter, new Node(2));

        Assertions.assertEquals(getLinkedList(1, 3, 2), actualLinkedList);
    }

    @Test
    void findAllInManyTest() {
        LinkedList2 actualLinkedList = getLinkedList(2, 1, 2, 1, 2);

        Assertions.assertEquals(3, actualLinkedList.findAll(2).size());
        Assertions.assertEquals(2, actualLinkedList.findAll(1).size());
        Assertions.assertEquals(0, actualLinkedList.findAll(0).size());
    }

    @Test
    void findAllInEmptyTest() {
        LinkedList2 actualLinkedList = getLinkedList();
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

    private LinkedList2 getLinkedList(int... values) {
        LinkedList2 linkedList = new LinkedList2();
        for (Integer value : values) {
            linkedList.addInTail(new Node(value));
        }
        return linkedList;
    }
}