package org.example.algo01.lesson03;

import java.lang.reflect.Array;
import java.util.*;

public class DynArray<T> {
    public static final double CAPACITY_DECREASE_FACTOR = 1.5;
    public static final int DECREASE_COUNT_RATIO = 2;
    public static final int MIN_CAPACITY = 16;

    public T[] array;
    public int count;
    public int capacity;
    Class clazz;

    public DynArray(Class clz) {
        clazz = clz;
        count = 0;
        makeArray(MIN_CAPACITY);
    }

    public void makeArray(int new_capacity) {
        if (new_capacity < MIN_CAPACITY) {
            new_capacity = MIN_CAPACITY;
        }

        T[] newArray = (T[]) Array.newInstance(this.clazz, new_capacity);
        if (this.array != null) {
            System.arraycopy(this.array, 0, newArray, 0, count);
        }

        this.array = newArray;
        this.capacity = new_capacity;
    }

    public T getItem(int index) {
        if (index < 0 || index >= capacity) {
            throw new ArrayIndexOutOfBoundsException();
        }

        return array[index];
    }

    public void append(T itm) {
        if (count == capacity) {
            makeArray(capacity * 2);
        }

        array[count] = itm;
        count++;
    }

    public void insert(T itm, int index) {
        if (index < 0 || index > count) {
            throw new ArrayIndexOutOfBoundsException();
        }

        if (count == capacity) {
            makeArray(capacity * 2);
        }

        System.arraycopy(this.array, index, this.array, index + 1, count - index);
        array[index] = itm;
        count++;
    }

    public void remove(int index) {
        if (index < 0 || count == 0 || index >= count) {
            throw new ArrayIndexOutOfBoundsException();
        }

        System.arraycopy(this.array, index + 1, this.array, index, capacity - index - 1);
        count--;

        if (DECREASE_COUNT_RATIO * count < capacity) {
            makeArray((int) (capacity / CAPACITY_DECREASE_FACTOR));
        }
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof DynArray)) return false;
        DynArray<?> dynArray = (DynArray<?>) o;
        return count == dynArray.count && capacity == dynArray.capacity && Arrays.equals(array, dynArray.array) && Objects.equals(clazz, dynArray.clazz);
    }

    @Override
    public int hashCode() {
        int result = Objects.hash(count, capacity, clazz);
        result = 31 * result + Arrays.hashCode(array);
        return result;
    }
}