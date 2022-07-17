package org.example.recursion;

import java.util.*;

public class Recursion07 {

    public Integer findPreMax(List<Integer> collection) {
        return findPreMax(collection, null, null);
    }

    private Integer findPreMax(List<Integer> collection, Integer max, Integer preMax) {
        if (collection.size() == 0) {
            return preMax;
        }

        int lastElementIndex = getLastElementIndex(collection);
        int lastElement = collection.get(lastElementIndex);

        if (isMaxNotSetOrLower(max, lastElement)) {
            preMax = max;
            max = lastElement;
        } else if (lastElement < max && isMaxNotSetOrLower(preMax, lastElement)) {
            preMax = lastElement;
        }

        return findPreMax(collection.subList(0, lastElementIndex), max, preMax);
    }

    private boolean isMaxNotSetOrLower(Integer max, Integer contender) {
        return max == null || contender > max;
    }

    private int getLastElementIndex(List<Integer> collection) {
        return collection.size() - 1;
    }
}
