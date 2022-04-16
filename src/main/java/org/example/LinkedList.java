package org.example;

import java.util.*;

public class LinkedList {

    public Node head;
    public Node tail;

    public LinkedList() {
        head = null;
        tail = null;
    }

    public void addInTail(Node item) {
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
                return node;
            }
            node = node.next;
        }
        return null;
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
            if (node.value == _value && head == tail) { // only
                this.head = null;
                this.tail = null;
                return true;
            }
            if (node.value == _value && node.next == null) { // last
                previousNode.next = null;
                this.tail = previousNode;
                return true;
            }
            if (node.value == _value && (this.head != node) && (this.tail != node)) { // in the middle
                previousNode.next = node.next;
                return true;
            }
            if (node.value == _value && this.head == node) { // first
                this.head = node.next;
                return true;
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
            if (node.value == _value && (this.head == this.tail)) { // only
                this.head = null;
                this.tail = null;
            } else if (node.value == _value && node.next == null) { // last
                previousNode.next = null;
                this.tail = previousNode;
            }  else if (node.value == _value && (this.head == node)) { // first
                this.head = node.next;
            } else if (node.value == _value && (this.tail != node)) { // in the middle
                previousNode.next = node.next;
                node = previousNode;
            }
            previousNode = node;
            node = node.next;
        }
    }

    public void clear() {
        this.head = null;
        this.tail = null;
    }

    public int count() {
        int size = 0;
        Node node = this.head;

        while (node != null) {
            size++;
            node = node.next;
        }
        return size;
    }

    public void insertAfter(Node _nodeAfter, Node _nodeToInsert) {
        if (_nodeAfter == null) {  // add new element first
            if (this.head == null) { // if list empty
                this.head = _nodeToInsert;
                this.tail = _nodeToInsert;
            } else { // else if only or more
                _nodeToInsert.next = this.head;
                this.head = _nodeToInsert;
            }
        } else {
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
    }
}

class Node {
    public int value;
    public Node next;

    public Node(int _value) {
        value = _value;
        next = null;
    }
}