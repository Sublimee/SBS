import java.util.*;
import java.util.stream.Collectors;

import static java.util.function.Predicate.not;

public class PowerSet {

    private static final int CAPACITY = 20000;

    private final HashTable elements;

    public PowerSet() {
        this.elements = new HashTable(CAPACITY);
    }

    private PowerSet(ArrayList<String> elements) {
        this();
        elements.forEach(this.elements::put);
    }

    public int size() {
        return this.elements.size;
    }

    public List<String> getList() {
        return this.elements.getElements();
    }

    public void put(String value) {
        this.elements.put(value);
    }

    public boolean get(String value) {
        return this.elements.contains(value);
    }

    public boolean remove(String value) {
        return this.elements.remove(value);
    }

    public PowerSet intersection(PowerSet set2) {
        if (set2 == null) {
            return new PowerSet();
        }

        PowerSet result = new PowerSet();
        set2.getList().forEach(x -> {
                    if (this.elements.contains(x)) {
                        result.put(x);
                    }
                }
        );
        return result;
    }

    public PowerSet union(PowerSet set2) {
        PowerSet result = new PowerSet();
        if (set2 != null) {
            set2.getList().forEach(result::put);
        }
        this.getList().forEach(result::put);
        return result;
    }

    public PowerSet difference(PowerSet set2) {
        if (set2 == null) {
            return new PowerSet(elements.getElements());
        }

        return new PowerSet(this.getList().stream().filter(not(set2::get)).collect(Collectors.toCollection(ArrayList::new)));
    }

    public boolean isSubset(PowerSet set2) {
        return set2 != null && set2.getList().stream().allMatch(this::get);
    }

    static class HashTable {
        public int capacity;
        public int size;

        public LinkedList<String>[] slots;

        public HashTable(int capacity) {
            this.capacity = capacity;
            slots = (LinkedList<String>[]) new LinkedList[capacity];
        }

        public int seekSlot(String value) {
            return value == null ? -1 : hashFun(value);
        }

        public void put(String value) {
            int slot = seekSlot(value);
            if (slot == -1) {
                return;
            }

            if (slots[slot] == null) {
                slots[slot] = new LinkedList<>();
            }

            if (slots[slot].contains(value)) {
                return;
            }

            slots[slot].add(value);
            this.size++;
        }

        public boolean remove(String value) {
            int slot = seekSlot(value);
            if (slot == -1 || slots[slot] == null) {
                return false;
            }

            boolean remove = slots[slot].remove(value);
            if (remove) {
                this.size--;
            }
            return remove;
        }

        public ArrayList<String> getElements() {
            ArrayList<String> result = new ArrayList<>();
            for (int i = 0; i < capacity; i++) {
                if (slots[i] != null) {
                    result.addAll(slots[i]);
                }
            }
            return result;
        }

        public boolean contains(String value) {
            int slot = seekSlot(value);
            return slot != -1 && slots[slot] != null && slots[slot].contains(value);
        }

        private int hashFun(String value) {
            return Math.abs(value.hashCode()) % capacity;
        }
    }
}
