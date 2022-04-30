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
        return Math.abs(value.hashCode()) % size;
    }

    public int seekSlot(String value) {
        int hash = hashFun(value);
        int slot = hash;
        while (slots[slot] != null) {
            if (slots[slot].equals(value)) {
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
        int slot = seekSlot(value);
        if (slot == -1 || !Objects.equals(slots[slot], value)) {
            return -1;
        } else {
            return slot;
        }
    }
}