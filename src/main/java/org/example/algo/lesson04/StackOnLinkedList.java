package org.example.algo.lesson04;

import java.util.*;

public class StackOnLinkedList<T> {
    public final List<T> elements;

    public StackOnLinkedList() {
        elements = new LinkedList<>();
    }

    public int size() {
        return elements.size();
    }

    public T pop() {
        return elements.size() > 0 ? elements.remove(0) : null;
    }

    public void push(T val) {
        elements.add(0, val);
    }

    public T peek() {
        return elements.size() > 0 ? elements.get(0) : null;
    }
}