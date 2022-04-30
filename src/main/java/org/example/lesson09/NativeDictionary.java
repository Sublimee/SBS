package org.example.lesson09;

import java.lang.reflect.Array;

public class NativeDictionary<T> {
    public int size;
    public String[] slots;
    public T[] values;

    public NativeDictionary(int sz, Class clazz) {
        size = sz;
        slots = new String[size];
        values = (T[]) Array.newInstance(clazz, this.size);
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
        }
    }

    public T get(String key) {
        int slot = seekSlot(key);
        return slot != -1 ? values[slot] : null;
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
