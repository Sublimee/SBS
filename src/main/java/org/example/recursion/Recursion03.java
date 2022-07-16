package org.example.recursion;

import java.util.*;

public class Recursion03 {

    public long getSize(Deque<Integer> values) {
        try {
            values.pop();
        } catch (NoSuchElementException e) {
            return 0;
        }

        return 1 + getSize(values);
    }
}
