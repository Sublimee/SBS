package org.example.recursion;

public class Recursion02 {

    public long sumDigits(int number) {
        if (number < 10) {
            return number;
        }

        return number % 10 + sumDigits(number / 10);
    }
}
