package org.example.algo.lesson05;

import java.util.*;

public class Queue<T> {

    public final LinkedList<T> queue;

    public Queue() {
        queue = new LinkedList<>();
    }

    public void enqueue(T item) {
        queue.addLast(item);
    }

    public T dequeue() {
        return size() == 0 ? null : queue.removeFirst();
    }

    public int size() {
        return queue.size();
    }

}