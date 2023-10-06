package oa1.two_way_list;

public class Node<T> {
    T value;
    Node<T> next;
    Node<T> prev;

    Node(T value) {
        this.value = value;
    }
}