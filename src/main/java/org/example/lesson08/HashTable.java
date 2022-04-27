package org.example.lesson08;

import java.util.*;

public class HashTable {
    public int size;
    public int step;
    public String[] slots;

    public HashTable(int sz, int stp) {
        size = sz;
        step = stp;
        slots = new String[size];
        for (int i = 0; i < size; i++) slots[i] = null;
    }

    public int hashFun(String value) {
        return value.hashCode() % size;
    }

    public int seekSlot(String value) {
        int hash = hashFun(value);
        int slot = hash;
        while (slots[slot] != null) {
            if (slots[slot].equals(value)){
                return slot;
            }
            slot = (slot + step) % size;
            if (slot == hash) {
                return -1;
            }
        }
        return slot;
    }

    public int put(String value) {
        int slot = seekSlot(value);
        if (slot != -1) {
            slots[slot] = value;
        }
        return slot;
    }

    public int find(String value) {
        for (int i = 0; i < slots.length; i++) {
            if (Objects.equals(slots[i], value)) {
                return i;
            }
        }
        return -1;
    }
}