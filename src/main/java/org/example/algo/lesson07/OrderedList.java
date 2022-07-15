package org.example.algo.lesson07;

import java.util.*;

public class OrderedList<T> {
    public Node<T> head, tail;
    private boolean _ascending;
    private int count;

    public OrderedList(boolean asc) {
        clear(asc);
    }

    public int compare(T v1, T v2) {
        if (v1 instanceof Integer && v2 instanceof Integer) {
            return ((Integer) v1).compareTo((Integer) v2);
        }
        if (v1 instanceof String && v2 instanceof String) {
            return ((String) v1).trim().compareTo(((String) v2).trim());
        }
        throw new ClassCastException();
    }

    public void add(T value) {
        Node<T> node = new Node<>(value);

        if (count++ == 0) {
            head = node;
            tail = node;
            return;
        }

        Node<T> nextNode = head;
        while (nextNode != null) {
            if ((compare(nextNode.value, value) > 0 && _ascending) || (compare(nextNode.value, value) < 0 && !_ascending)) {
                node.prev = nextNode.prev;
                node.next = nextNode;
                if (nextNode == head) {
                    nextNode.prev = node;
                    head = node;
                    return;
                } else {
                    nextNode.prev.next = node;
                    nextNode.prev = node;
                    return;
                }
            } else {
                nextNode = nextNode.next;
            }
        }

        tail.next = node;
        node.prev = tail;
        tail = node;
    }

    public Node<T> find(T val) {
        Node<T> node = this.head;

        if (Objects.nonNull(node) && ((compare(val, node.value) == -1 && _ascending) || (compare(val, node.value) == 1 && !_ascending))) {
            return null;
        }

        while (node != null) {
            if (node.value.equals(val)) {
                return node;
            }
            node = node.next;
        }

        return null;
    }

    public void delete(T val) {
        Node<T> node = find(val);
        if (node == null) {
            return;
        }
        if (head == tail) { // only
            this.head = null;
            this.tail = null;
        } else if (node.next == null) { // last
            node.prev.next = null;
            this.tail = node.prev;
        } else if (this.head != node && this.tail != node) { // in the middle
            node.prev.next = node.next;
            node.next.prev = node.prev;
        } else if (this.head == node) { // first
            this.head = node.next;
            node.next.prev = null;
        }
        count--;
    }

    public void clear(boolean asc) {
        head = null;
        tail = null;
        _ascending = asc;
        count = 0;
    }

    public int count() {
        return count;
    }

    public ArrayList<Node<T>> getAll() {
        ArrayList<Node<T>> result = new ArrayList<>();
        Node<T> node = head;
        while (node != null) {
            result.add(node);
            node = node.next;
        }
        return result;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof OrderedList)) return false;
        OrderedList other = (OrderedList) o;
        if (other._ascending != this._ascending) {
            return false;
        }
        if (this.head == null && other.head == null && this.tail == null && other.tail == null) {
            return true;
        }
        if (((this.head != null) && (other.head == null)) || ((this.head == null) && (other.head != null))) {
            return false;
        }
        if (this.head != null && (other.head != null) && (this.head.value != other.head.value)) {
            return false;
        }
        if (((this.tail != null) && (other.tail == null)) || ((this.tail == null) && (other.tail != null))) {
            return false;
        }
        if (this.tail != null && (other.tail != null) && (this.tail.value != other.tail.value)) {
            return false;
        }

        Node thisPrevNode = tail.prev;
        Node otherPrevNode = other.tail.prev;
        boolean prevNodesAreEquals = true;

        while (prevNodesAreEquals) {
            if (thisPrevNode == null && otherPrevNode == null) {
                break;
            }
            if (thisPrevNode != null && otherPrevNode != null && thisPrevNode.value == otherPrevNode.value) {
                thisPrevNode = thisPrevNode.prev;
                otherPrevNode = otherPrevNode.prev;
                continue;
            }
            prevNodesAreEquals = false;
        }

        return prevNodesAreEquals;
    }
}
