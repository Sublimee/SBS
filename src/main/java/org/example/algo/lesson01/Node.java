package org.example.algo.lesson01;

import java.util.*;

public class Node {
    public int value;
    public Node next;

    public Node(int _value) {
        value = _value;
        next = null;
    }

    @Override
    public String toString() {
        return "Node{" +
                "value=" + value +
                ", next=" + next +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Node)) return false;
        Node node = (Node) o;
        return value == node.value && Objects.equals(next, node.next);
    }

    @Override
    public int hashCode() {
        return Objects.hash(value, next);
    }
}