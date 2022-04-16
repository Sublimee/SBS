import org.example.LinkedList;
import org.example.Node;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class LinkedListTest {

    @Test
    void removeFirstElementFromManyTest() {
        LinkedList actualLinkedList = getLinkedList(1, 2, 3);

        actualLinkedList.remove(1);

        Assertions.assertEquals(getLinkedList(2, 3), actualLinkedList);
    }

    @Test
    void removeMiddleElementFromManyTest() {
        LinkedList actualLinkedList = getLinkedList(1, 2, 3);

        actualLinkedList.remove(2);

        Assertions.assertEquals(getLinkedList(1, 3), actualLinkedList);
    }

    @Test
    void removeLastElementFromManyTest() {
        LinkedList actualLinkedList = getLinkedList(1, 2, 3);

        actualLinkedList.remove(3);

        Assertions.assertEquals(getLinkedList(1, 2), actualLinkedList);
    }

    @Test
    void removeFirstElementFromTwoTest() {
        LinkedList actualLinkedList = getLinkedList(1, 2);

        actualLinkedList.remove(1);

        Assertions.assertEquals(getLinkedList(2), actualLinkedList);
    }

    @Test
    void removeLastElementFromTwoTest() {
        LinkedList actualLinkedList = getLinkedList(1, 2);

        actualLinkedList.remove(2);

        Assertions.assertEquals(getLinkedList(1), actualLinkedList);
    }

    @Test
    void removeElementFromSingleTest() {
        LinkedList actualLinkedList = getLinkedList(1);

        actualLinkedList.remove(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeUnexpectedElementTest() {
        LinkedList actualLinkedList = getLinkedList(1);

        actualLinkedList.remove(2);

        Assertions.assertEquals(getLinkedList(1), actualLinkedList);
    }

    @Test
    void removeElementFromEmptyTest() {
        LinkedList actualLinkedList = getLinkedList(1);

        actualLinkedList.remove(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void clearNotEmptyTest() {
        LinkedList actualLinkedList = getLinkedList(1, 2, 3);
        actualLinkedList.clear();

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void clearSingleTest() {
        LinkedList actualLinkedList = getLinkedList(1);
        actualLinkedList.clear();

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void clearEmptyTest() {
        LinkedList actualLinkedList = getLinkedList();
        actualLinkedList.clear();

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromManyTest() {
        LinkedList actualLinkedList = getLinkedList(1, 1, 1);
        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromTwoTest() {
        LinkedList actualLinkedList = getLinkedList(1, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromSingleTest() {
        LinkedList actualLinkedList = getLinkedList(1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromEmptyTest() {
        LinkedList actualLinkedList = getLinkedList();

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(), actualLinkedList);
    }

    @Test
    void removeAllFromComplexSequence1Test() {
        LinkedList actualLinkedList = getLinkedList(1, 2, 1, 2, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(2, 2), actualLinkedList);
    }

    @Test
    void removeAllFromComplexSequence2Test() {
        LinkedList actualLinkedList = getLinkedList(2, 1, 2, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(2, 2), actualLinkedList);
    }

    @Test
    void removeAllFromComplexSequence3Test() {
        LinkedList actualLinkedList = getLinkedList(2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1);

        actualLinkedList.removeAll(1);

        Assertions.assertEquals(getLinkedList(2, 2, 2, 2, 2, 2, 2, 2), actualLinkedList);
    }

    @Test
    void insertAfterNoSpecifiedElementIntoEmptyTest() {
        LinkedList actualLinkedList = getLinkedList();

        actualLinkedList.insertAfter(null, new Node(2));

        Assertions.assertEquals(getLinkedList(2), actualLinkedList);
    }

    @Test
    void insertAfterNoSpecifiedElementIntoSingleTest() {
        LinkedList actualLinkedList = getLinkedList(1);

        actualLinkedList.insertAfter(null, new Node(2));

        Assertions.assertEquals(getLinkedList(2, 1), actualLinkedList);
    }

    @Test
    void insertAfterNoSpecifiedElementIntoManyTest() {
        LinkedList actualLinkedList = getLinkedList(2, 1);

        actualLinkedList.insertAfter(null, new Node(3));

        Assertions.assertEquals(getLinkedList(3, 2, 1), actualLinkedList);
    }

    @Test
    void insertAfterSpecifiedElementIntoSingleTest() {
        LinkedList actualLinkedList = getLinkedList();

        Node nodeAfter = new Node(2);
        actualLinkedList.addInTail(nodeAfter);
        actualLinkedList.insertAfter(nodeAfter, new Node(1));

        Assertions.assertEquals(getLinkedList(2, 1), actualLinkedList);
    }

    @Test
    void insertAfterFirstSpecifiedElementIntoManyTest() {
        LinkedList actualLinkedList = getLinkedList();

        Node nodeAfter = new Node(1);
        actualLinkedList.addInTail(nodeAfter);
        actualLinkedList.addInTail(new Node(3));
        actualLinkedList.insertAfter(nodeAfter, new Node(2));

        Assertions.assertEquals(getLinkedList(1, 2, 3), actualLinkedList);
    }

    @Test
    void insertAfterLastSpecifiedElementIntoManyTest() {
        LinkedList actualLinkedList = getLinkedList();

        Node nodeAfter = new Node(3);
        actualLinkedList.addInTail(new Node(1));
        actualLinkedList.addInTail(nodeAfter);
        actualLinkedList.insertAfter(nodeAfter, new Node(2));

        Assertions.assertEquals(getLinkedList(1, 3, 2), actualLinkedList);
    }

    @Test
    void findAllInManyTest() {
        LinkedList actualLinkedList = getLinkedList(2, 1, 2, 1, 2);

        Assertions.assertEquals(3, actualLinkedList.findAll(2).size());
        Assertions.assertEquals(2, actualLinkedList.findAll(1).size());
        Assertions.assertEquals(0, actualLinkedList.findAll(0).size());
    }

    @Test
    void findAllInEmptyTest() {
        LinkedList actualLinkedList = getLinkedList();
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

    private LinkedList getLinkedList(int... values) {
        LinkedList linkedList = new LinkedList();
        for (Integer value : values) {
            linkedList.addInTail(new Node(value));
        }
        return linkedList;
    }
}