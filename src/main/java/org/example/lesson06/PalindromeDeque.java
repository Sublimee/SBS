package org.example.lesson06;

import java.util.*;
import java.util.stream.Collectors;

public class PalindromeDeque {

    public final LinkedList<Character> list;

    public PalindromeDeque(String example) {
        list = example.chars().mapToObj(x -> ((char) x)).collect(Collectors.toCollection(LinkedList::new));
    }

    public Character removeFront() {
        return (size() > 0) ? list.removeFirst() : null;
    }

    public Character removeTail() {
        return (size() > 0) ? list.removeLast() : null;
    }

    public int size() {
        return list.size();
    }
}
