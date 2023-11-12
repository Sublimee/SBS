package oa1.power_set;

/*
    АТД Hashtable

abstract class Hashtable<T> {

    // интерфейс класса, реализующий АТД Hashtable

    public final int PUT_NIL = 0;       // put() ещё не вызывалась
    public final int PUT_OK = 1;        // последняя команда добавления нового значения отработала нормально
    public final int PUT_ERR = 2;       // хэш-таблица полна

    public final int REMOVE_NIL = 0;    // remove() ещё не вызывалась
    public final int REMOVE_OK = 1;     // последняя команда удаления отработала нормально
    public final int REMOVE_ERR = 2;    // хэш-таблица не содержит искомого значения

    // конструктор

    // постусловие: создана новая пустая хэш-таблица
    public Hashtable<T> Hashtable(int capacity);


    // команды

    // предусловие: хэш-таблица не полна
    // постусловие: в хэш-таблицу добавлено новое значение value
    public void put(T value);

    // предусловие: хэш-таблица содержит значение value
    // постусловие: из хэш-таблицы удалено значение value
    public void remove(T value);


    // запросы

    public boolean contains(T value); // содержит ли хэш-таблица значение value?

    public int size(); // посчитать количество элементов в хэш-таблице


    // запросы

    // возвращает значение PUT_
    public int get_put_status();

    // возвращает значение REMOVE_
    public int get_remove_status();
}


    АТД PowerSet

abstract class PowerSet<T> : HashTable<T> {

    // конструктор

    // постусловие: создано новое пустое множество
    public PowerSet<T> PowerSet(int capacity);


    // запросы

    public PowerSet<T>  intersection(PowerSet<T> set);  // возвращает пересечение текущего множества с переданным множеством set

    public PowerSet<T>  union(PowerSet<T> set);         // возвращает объединение текущего множества с переданным множеством set

    public PowerSet<T>  difference(PowerSet<T> set);    // возвращает разницу текущего множества с переданным множеством set

    public boolean      isSubset(PowerSet<T> set);      // отвечает на вопрос: является ли переданное множество set подмножеством текущего множества?
}
*/

import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.stream.Stream;

class Hashtable<T> {

    public final int PUT_NIL = 0;
    public final int PUT_OK = 1;
    public final int PUT_ERR = 2;

    public final int REMOVE_NIL = 0;
    public final int REMOVE_OK = 1;
    public final int REMOVE_ERR = 2;

    private final int DEFAULT_STEP_SIZE = 1;

    private final int capacity;
    private final T[] slots;

    private int size;

    private int putStatus;
    private int removeStatus;


    public Hashtable(int capacity) {
        this.capacity = capacity;
        this.size = 0;
        this.slots = (T[]) new Object[capacity];
        for (int i = 0; i < this.capacity; i++) slots[i] = null;
        this.putStatus = PUT_NIL;
        this.removeStatus = REMOVE_NIL;
    }


    public void put(T value) {
        int slot = seekSlot(value);
        if (slot != -1) {
            slots[slot] = value;
            size++;
            putStatus = PUT_OK;
        } else {
            putStatus = PUT_ERR;
        }
    }

    public void remove(T value) {
        int indexToRemove = find(value);
        if (indexToRemove != -1) {
            slots[indexToRemove] = null;
            size--;
            removeStatus = REMOVE_OK;
        } else {
            removeStatus = REMOVE_ERR;
        }
    }


    public boolean contains(T value) {
        return find(value) != -1;
    }

    public int size() {
        return size;
    }

    public int capacity() {
        return capacity;
    }

    public List<T> getElements() {
        return Arrays.stream(slots).filter(Objects::nonNull).toList();
    }


    public int get_put_status() {
        return putStatus;
    }

    public int get_remove_status() {
        return removeStatus;
    }


    private int hashFun(T value) {
        return value == null ? 0 : Math.abs(value.hashCode()) % capacity;
    }

    private int seekSlot(T value) {
        int hash = hashFun(value);
        int slot = hash;
        while (slots[slot] != null) {
            if (slots[slot].equals(value)) {
                return slot;
            }
            slot = (slot + DEFAULT_STEP_SIZE) % capacity;
            if (slot == hash) {
                return -1;
            }
        }
        return slot;
    }

    private int find(T value) {
        int slot = seekSlot(value);
        if (slot == -1 || !Objects.equals(slots[slot], value)) {
            return -1;
        } else {
            return slot;
        }
    }
}

class PowerSet<T> extends Hashtable<T> {

    public PowerSet(int capacity) {
        super(capacity);
    }

    public PowerSet<T> intersection(PowerSet<T> set) {
        PowerSet<T> result = new PowerSet<>(capacity());
        if (set != null) {
            set.getElements().stream()
                    .filter(this::contains)
                    .forEach(result::put);
        }
        return result;
    }

    public PowerSet<T> union(PowerSet<T> set) {
        PowerSet<T> result = new PowerSet<>(capacity());
        Stream.concat(this.getElements().stream(), Stream.ofNullable(set).flatMap(s -> s.getElements().stream()))
                .forEach(result::put);
        return result;
    }

    public PowerSet<T> difference(PowerSet<T> set) {
        PowerSet<T> result = new PowerSet<>(capacity());
        getElements().stream()
                .filter(item -> set == null || !set.contains(item))
                .forEach(result::put);
        return result;
    }

    public boolean isSubset(PowerSet<T> set) {
        return set != null && set.getElements().stream().allMatch(this::contains);
    }
}