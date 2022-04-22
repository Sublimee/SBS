package org.example.lesson06;

import java.util.*;

public class Deque<T> {

    public final LinkedList<T> list;

    public Deque() {
        list = new LinkedList<>();
    }

    public void addFront(T item) {
        list.addFirst(item);
        // добавление в голову
    }

    public void addTail(T item) {
        list.addLast(item);
        // добавление в хвост
    }

    public T removeFront() {
        // удаление из головы
        return (size() > 0) ? list.removeFirst() : null;
    }

    public T removeTail() {
        // удаление из хвоста
        return (size() > 0) ? list.removeLast() : null;
    }

    public int size() {
        return list.size(); // размер очереди
    }
}
