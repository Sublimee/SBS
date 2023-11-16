package oa1.bloom_filter;

/*
    АТД BloomFilter

abstract class BloomFilter<T> {

    // конструктор

    // постусловие: создан новый пустой фильтр Блюма
    public BloomFilter(int capacity);


    // команды

    // постусловие: в фильтр Блюма добавлено новое значение
    public void add(T value);


    // запросы

    public boolean isValue(T value); // отвечает на вопрос: содержит ли фильтр Блюма переданное значение value?
                                     // допускаются ложноположительные, но не ложноотрицательные срабатывания
}
 */

public class BloomFilter<T> {

    public int capacity;
    public int bitArray;

    public BloomFilter(int capacity) {
        this.capacity = capacity;
        bitArray = 0;
    }

    public void add(T value) {
        updateBitArray(hash1(value));
        updateBitArray(hash2(value));
    }

    public boolean isValue(T value) {
        return checkBit(bitArray, hash1(value)) && checkBit(bitArray, hash2(value));
    }

    private int hash1(T value) {
        return hash(value, 17);
    }

    private int hash2(T value) {
        return hash(value, 223);
    }

    private int hash(T value, int random) {
        int hash = value.hashCode();
        return (random * hash + (hash >>> random)) % capacity;
    }

    private void updateBitArray(int bit) {
        bitArray |= 1 << bit;
    }

    private boolean checkBit(int bitArray, int bit) {
        return (bitArray >> bit & 1) == 1;
    }
}