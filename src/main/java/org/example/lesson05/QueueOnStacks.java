package org.example.lesson05;

import org.example.lesson04.Stack;

public class QueueOnStacks<T> {

    public final Stack<T> stack1;
    public final Stack<T> stack2;

    private Stack<T> head;
    private Stack<T> tail;
    boolean reverse;

    public QueueOnStacks() {
        this.stack1 = new Stack<>();
        this.stack2 = new Stack<>();

        head = this.stack1;
        tail = this.stack2;
        reverse = true;
    }

    public void enqueue(T item) {
        if (reverse) {
            head.push(item);
        } else {
            while (head.size() > 0) {
                tail.push(head.pop());
            }
            tail.push(item);

            Stack<T> stackTemp = head;
            head = tail;
            tail = stackTemp;

            reverse = true;
        }
        // вставка в хвост
    }

    public T dequeue() {
        if (reverse) {
            while (head.size() > 1) {
                tail.push(head.pop());
            }

            Stack<T> stackTemp = head;
            head = tail;
            tail = stackTemp;

            reverse = false;
            // выдача из головы
            return tail.pop(); // null если очередь пустая
        } else {
            return head.pop();
        }
    }

    public int size() {
        return 0; // размер очереди
    }
}
