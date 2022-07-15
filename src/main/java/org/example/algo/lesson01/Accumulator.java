package org.example.algo.lesson01;

public class Accumulator {

    public static LinkedList process(LinkedList first, LinkedList second) {
        if (first.count() != second.count()) {
            return null;
        }

        LinkedList result = new LinkedList();
        Node firstNode = first.head;
        Node secondNode = second.head;
        while (firstNode != null) {
            result.addInTail(new Node(firstNode.value + secondNode.value));
            firstNode = firstNode.next;
            secondNode = secondNode.next;
        }
        return result;
    }

}