package org.example.lesson12;

import java.lang.reflect.Array;

public class NativeCache<T> {
    public int size;
    public String[] slots;
    public T[] values;
    public int[] hits;

    public NativeCache(int sz, Class clazz) {
        size = sz;
        slots = new String[size];
        values = (T[]) Array.newInstance(clazz, this.size);
        hits = new int[size];
    }

    public int hashFun(String key) {
        return key == null ? -1 : Math.abs(key.hashCode()) % size;
    }

    public boolean isKey(String key) {
        int slot = seekSlot(key);
        return slot != -1 && slots[slot] != null;
    }

    public void put(String key, T value) {
        int slot = seekSlot(key);
        if (slot != -1) {
            slots[slot] = key;
            values[slot] = value;
            return;
        }

        int slotToRemove = findMinValueIndex(hits);
        slots[slotToRemove] = key;
        values[slotToRemove] = value;
        hits[slotToRemove] = 0;
    }

    int findMinValueIndex(int[] array) {
        int minAt = 0;

        for (int i = 0; i < array.length; i++) {
            minAt = array[i] < array[minAt] ? i : minAt;
        }

        return minAt;
    }

    public T get(String key) {
        int slot = seekSlot(key);
        return slot != -1 ? update(slot) : null;
    }

    public T update(int slot) {
        hits[slot]++;
        return values[slot];
    }


    private int seekSlot(String value) {
        int hash = hashFun(value);
        if (hash == -1) {
            return -1;
        }
        int slot = hash;
        while (slots[slot] != null) {
            if (slots[slot].equals(value)) {
                return slot;
            }
            slot = (slot + 1) % size;
            if (slot == hash) {
                return -1;
            }
        }
        return slot;
    }
}
