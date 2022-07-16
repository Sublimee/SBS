package org.example.recursion;

public class Recursion04 {

    private static boolean isPalindrome(String test) {
        if (test.length() < 2) {
            return true;
        }

        boolean areEndsEqual = test.endsWith(getFirstChar(test));

        if (!areEndsEqual) {
            return false;
        }

        return isPalindrome(trimEnds(test));
    }

    private static String trimEnds(String test) {
        return test.substring(1, test.length() - 1);
    }

    private static String getFirstChar(String test) {
        return test.substring(0, 1);
    }
}

