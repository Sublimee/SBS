package org.example.recursion;

public class Recursion04 {

    public boolean isPalindrome(String test) {
        if (test.length() < 2) {
            return true;
        }

        boolean areEndsEqual = test.endsWith(getFirstChar(test));

        if (!areEndsEqual) {
            return false;
        }

        return isPalindrome(trimEnds(test));
    }

    private String trimEnds(String test) {
        return test.substring(1, test.length() - 1);
    }

    private String getFirstChar(String test) {
        return test.substring(0, 1);
    }
}

