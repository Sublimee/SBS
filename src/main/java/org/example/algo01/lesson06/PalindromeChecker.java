package org.example.algo01.lesson06;

import java.util.*;

public class PalindromeChecker {

    public boolean check(String example) {
        if (example == null) {
            return false;
        }

        PalindromeDeque deque = new PalindromeDeque(example);

        while (deque.size() >= 2) {
            if (!Objects.equals(deque.removeFront(), deque.removeTail())) {
                return false;
            }
        }

        return true;
    }
}
