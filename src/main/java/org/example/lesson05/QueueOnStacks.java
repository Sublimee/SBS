package org.example.lesson05;

import org.example.lesson04.Stack;

public class QueueOnStacks<T> {

    private boolean reversed;
    private Stack<T> head;
    private Stack<T> tail;

    public QueueOnStacks() {
        head = new Stack<>();
        tail = new Stack<>();
        reversed = true;
    }

    public void enqueue(T item) {
        if (!reversed) {
            exchangeStacks();
        }
        head.push(item);
    }

    public T dequeue() {
        if (reversed) {
            exchangeStacks();
        }
        return head.size() > 0 ? head.pop() : null;
    }

    private void exchangeStacks() {
        while (head.size() > 0) {
            tail.push(head.pop());
        }

        Stack<T> stackTemp = head;
        head = tail;
        tail = stackTemp;

        reversed = !reversed;
    }

    public int size() {
        return head.size();
    }
}
