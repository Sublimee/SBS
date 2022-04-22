package org.example.lesson05;

import org.example.lesson04.Stack;

public class QueueOnStacks<T> {

    public final Stack<T> stack1;
    public final Stack<T> stack2;

    private Stack<T> head;
    private Stack<T> tail;
    boolean reversed;

    public QueueOnStacks() {
        this.stack1 = new Stack<>();
        this.stack2 = new Stack<>();

        head = this.stack1;
        tail = this.stack2;
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
