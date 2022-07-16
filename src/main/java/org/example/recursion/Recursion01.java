package org.example.recursion;

public class Recursion01 {

    private static long exponentiation(long base, long power) {
        if (power == 0) {
            return 1;
        }

        if (power == 1) {
            return base;
        }

        return base * exponentiation(base, power - 1);
    }
}