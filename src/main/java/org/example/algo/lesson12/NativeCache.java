package org.example.algo.lesson12;

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

        putWithExclusion(key, value);
    }

    public T get(String key) {
        int slot = seekSlot(key);
        if (slot != -1) {
            hits[slot]++;
            return values[slot];
        }
        return null;
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

    private void putWithExclusion(String key, T value) {
        int slotToRemove = findMinHitsIndex();
        slots[slotToRemove] = key;
        values[slotToRemove] = value;
        hits[slotToRemove] = 0;
    }

    private int findMinHitsIndex() {
        int minAt = 0;

        for (int i = 0; i < hits.length; i++) {
            minAt = hits[i] < hits[minAt] ? i : minAt;
        }

        return minAt;
    }
}
