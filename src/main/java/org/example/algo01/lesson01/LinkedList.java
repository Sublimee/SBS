package org.example.algo01.lesson01;

import java.util.*;

public class LinkedList {

    public Node head;
    public Node tail;
    public int count;

    public LinkedList() {
        clear();
    }

    public void addInTail(Node item) {
        count++;

        if (this.head == null) {
            this.head = item;
        } else {
            this.tail.next = item;
        }
        this.tail = item;
    }

    public Node find(int value) {
        Node node = this.head;
        while (node != null) {
            if (node.value == value) {
                break;
            }
            node = node.next;
        }
        return node;
    }

    public ArrayList<Node> findAll(int _value) {
        ArrayList<Node> nodes = new ArrayList<>();

        Node node = this.head;
        while (node != null) {
            if (node.value == _value) {
                nodes.add(node);
            }
            node = node.next;
        }

        return nodes;
    }

    public boolean remove(int _value) {
        Node node = this.head;
        Node previousNode = null;

        while (node != null) {
            if (node.value == _value) {
                count--;
                if (head == tail) { // only
                    this.head = null;
                    this.tail = null;
                    return true;
                }
                if (node.next == null) { // last
                    previousNode.next = null;
                    this.tail = previousNode;
                    return true;
                }
                if (this.head != node && this.tail != node) { // in the middle
                    previousNode.next = node.next;
                    return true;
                }
                if (this.head == node) { // first
                    this.head = node.next;
                    return true;
                }
            }
            previousNode = node;
            node = node.next;
        }
        return false;
    }

    public void removeAll(int _value) {
        Node node = this.head;
        Node previousNode = null;

        while (node != null) {
            if (node.value == _value) {
                count--;
                if (this.head == this.tail) { // only
                    this.head = null;
                    this.tail = null;
                } else if (node.next == null) { // last
                    previousNode.next = null;
                    this.tail = previousNode;
                } else if (this.head == node) { // first
                    this.head = node.next;
                } else if (this.tail != node) { // in the middle
                    previousNode.next = node.next;
                    node = previousNode;
                }
            }
            previousNode = node;
            node = node.next;
        }
    }

    public void clear() {
        this.head = null;
        this.tail = null;
        count = 0;
    }

    public int count() {
        return count;
    }

    public void insertAfter(Node _nodeAfter, Node _nodeToInsert) {
        count++;

        if (_nodeAfter == null) {  // add new element first
            if (this.head == null) { // if list empty
                this.head = _nodeToInsert;
                this.tail = _nodeToInsert;
            } else { // else if only or more
                _nodeToInsert.next = this.head;
                this.head = _nodeToInsert;
            }
            return;
        }

        Node node = this.head;
        while (node != null) {
            if (_nodeAfter == node) {
                if (_nodeAfter == this.tail) {
                    _nodeAfter.next = _nodeToInsert;
                    this.tail = _nodeToInsert;
                } else {
                    _nodeToInsert.next = _nodeAfter.next;
                    _nodeAfter.next = _nodeToInsert;
                }
            }
            node = node.next;
        }
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof LinkedList)) return false;
        LinkedList that = (LinkedList) o;
        return count == that.count && Objects.equals(head, that.head) && Objects.equals(tail, that.tail);
    }

    @Override
    public int hashCode() {
        return Objects.hash(head, tail, count);
    }

    @Override
    public String toString() {
        return "LinkedList{" + "head=" + head + ", tail=" + tail + '}';
    }
}