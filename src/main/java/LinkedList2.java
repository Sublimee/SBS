import java.util.*;

public class LinkedList2 {
    public Node head;
    public Node tail;

    public LinkedList2() {
        head = null;
        tail = null;
    }

    public void addInTail(Node _item) {
        if (head == null) {
            this.head = _item;
            this.head.next = null;
            this.head.prev = null;
        } else {
            this.tail.next = _item;
            _item.prev = tail;
        }
        this.tail = _item;
    }

    public Node find(int _value) {
        Node node = this.head;
        while (node != null) {
            if (node.value == _value) {
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

        while (node != null) {
            if (node.value == _value && head == tail) { // only
                this.head = null;
                this.tail = null;
                return true;
            }
            if (node.value == _value && node.next == null) { // last
                node.prev.next = null;
                this.tail = node.prev;
                return true;
            }
            if (node.value == _value && (this.head != node) && (this.tail != node)) { // in the middle
                node.prev.next = node.next;
                node.next.prev = node.prev;
                return true;
            }
            if (node.value == _value && this.head == node) { // first
                this.head = node.next;
                node.next.prev = null;
                return true;
            }
            node = node.next;
        }
        return false;
    }

    public void removeAll(int _value) {
        Node node = this.head;

        while (node != null) {
            if (node.value == _value && (this.head == this.tail)) { // only
                this.head = null;
                this.tail = null;
            } else if (node.value == _value && node.next == null) { // last
                node.prev.next = null;
                this.tail = node.prev;
            } else if (node.value == _value && (this.head == node)) { // first
                node.next.prev = null;
                this.head = node.next;
            } else if (node.value == _value && (this.tail != node)) { // in the middle
                node.next.prev = node.prev;
                node.prev.next = node.next;
            }
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
                this.head.prev = _nodeToInsert;
                _nodeToInsert.next = this.head;
                this.head = _nodeToInsert;
            }
        } else {
            Node node = this.head;
            while (node != null) {
                if (_nodeAfter == node) {
                    if (_nodeAfter == this.tail) {
                        _nodeToInsert.prev = this.tail;
                        _nodeAfter.next = _nodeToInsert;
                        this.tail = _nodeToInsert;
                    } else {
                        _nodeToInsert.next = _nodeAfter.next;
                        _nodeToInsert.prev = _nodeAfter;
                        _nodeAfter.next.prev = _nodeToInsert;
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
    public Node prev;

    public Node(int _value) {
        value = _value;
        next = null;
        prev = null;
    }
}