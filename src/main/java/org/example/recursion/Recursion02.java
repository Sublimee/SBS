package org.example.recursion;

public class Recursion02 {

    public static void main(String[] args) {
        System.out.println(sumDigits(90090));
    }

    private static int sumDigits(int number) {
        if (number < 10) {
            return number;
        }

        return number % 10 + sumDigits(number / 10);
    }
}
