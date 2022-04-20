package org.example.lesson04;

import java.util.*;

public class Stack<T> {
    public final List<T> elements;

    public Stack() {
        elements = new ArrayList<>();
    }

    public int size() {
        return elements.size();
    }

    public T pop() {
        return elements.size() > 0 ? elements.remove(elements.size() - 1) : null;
    }

    public void push(T val) {
        elements.add(val);
    }

    public T peek() {
        return elements.size() > 0 ? elements.get(elements.size() - 1) : null;
    }
}