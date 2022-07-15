package lesson01;

import org.example.algo.lesson01.LinkedList;
import org.example.algo.lesson01.Node;

public class TestUtils {

    public static LinkedList getLinkedList(int... values) {
        LinkedList linkedList = new LinkedList();
        for (Integer value : values) {
            linkedList.addInTail(new Node(value));
        }
        return linkedList;
    }

}