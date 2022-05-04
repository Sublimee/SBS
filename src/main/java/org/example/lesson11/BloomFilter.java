package org.example.lesson11;

public class BloomFilter {
    public int filter_len;

    public BloomFilter(int f_len) {
        filter_len = f_len;
    }

    // хэш-функции
    public int hash1(String str1) {
        return hash(str1, 17);
    }

    public int hash2(String str1) {
        return hash(str1, 223);
    }

    private int hash(String str1, int random) {
        int result = 0;
        for (int i = 0; i < str1.length(); i++) {
            result = (result * random + str1.charAt(i)) % filter_len;
        }
        return result;
    }

    public void add(String str1) {
        filter_len |= 0;
        filter_len |= 1;
        filter_len |= 2;
    }

    public boolean isValue(String str1) {
        // проверка, имеется ли строка str1 в фильтре
        return false;
    }
}
