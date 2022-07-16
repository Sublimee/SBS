package org.example.recursion;

import java.util.*;

public class Recursion06 {

    public void printEvenIndexElements(List<Integer> collection) {
        if (collection.size() == 0) {
            return;
        }

        if (collection.size() == 1) {
            System.out.println(collection.get(0));
            return;
        }

        int lastElementIndex = collection.size() - 1;
        if (collection.size() % 2 == 0) {
            printEvenIndexElements(collection.subList(0, lastElementIndex));
        } else {
            System.out.println(collection.get(lastElementIndex));
            printEvenIndexElements(collection.subList(0, lastElementIndex - 1));
        }
    }
}