package org.example.recursion;

import java.util.*;

public class Recursion05 {

    public void printEvenElements(List<Integer> collection) {
        if (collection.size() == 0) {
            return;
        }

        int lastElementIndex = collection.size() - 1;
        Integer lastElement = collection.get(lastElementIndex);

        if (lastElement % 2 == 0) {
            System.out.println(lastElement);
        }

        printEvenElements(collection.subList(0, lastElementIndex));
    }
}
