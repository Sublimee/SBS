package oa1.native_dictionary;

/*
    АТД NativeDictionary

abstract class NativeDictionary<T> {

    // интерфейс класса, реализующий АТД NativeDictionary

    public final int PUT_NIL = 0;       // put() ещё не вызывалась
    public final int PUT_OK = 1;        // последняя команда put() отработала нормально
    public final int PUT_ERR = 2;       // ассоциативный массив полон или (ключ или значение) == null

    public final int REMOVE_NIL = 0;    // remove() ещё не вызывалась
    public final int REMOVE_OK = 1;     // последняя команда remove() отработала нормально
    public final int REMOVE_ERR = 2;    // ассоциативный массив не содержит переданный ключ key или он равен null

    public final int GET_NIL = 0;       // get() ещё не вызывалась
    public final int GET_OK = 1;        // последняя команда получения значения по ключу key отработала нормально
    public final int GET_ERR = 2;       // ассоциативный массив не содержит переданный ключ key или он равен null

    // конструктор

    // постусловие: создана новый пустой ассоциативный массив
    public NativeDictionary<T> NativeDictionary(int capacity);


    // команды

    // предусловие: ассоциативный массив не полон, ключ key и значение value не равны null
    // постусловие: в ассоциативный массив добавлено новое значение value по ключу key, если он не содержит ключ key,
    //              иначе значение по ключу key обновляется на value
    public void put(String key, T value);

    // предусловие: ключ key не равен null, ассоциативный массив содержит ключ key
    // постусловие: из ассоциативного массива удален ключ key и соответствующее ему значение
    public void remove(String key);


    // запросы

    // предусловие: ключ key не равен null, ассоциативный массив содержит ключ key
    public T get(String key);               // получить значение по ключу key

    public boolean containsKey(String key); // содержит ли ассоциативный массив ключ key?

    public int capacity();                  // получить емкость ассоциативного массива

    public int size();                      // получить количество элементов в ассоциативном массиве


    // запросы

    // возвращает значение PUT_
    public int get_put_status();

    // возвращает значение REMOVE_
    public int get_remove_status();

    // возвращает значение GET_
    public int get_get_status();
}
*/

public class NativeDictionary<T> {

    public final int PUT_NIL = 0;
    public final int PUT_OK = 1;
    public final int PUT_ERR = 2;

    public final int REMOVE_NIL = 0;
    public final int REMOVE_OK = 1;
    public final int REMOVE_ERR = 2;

    public final int GET_NIL = 0;
    public final int GET_OK = 1;
    public final int GET_ERR = 2;

    public int capacity;
    public int size;

    public String[] slots;
    public T[] values;

    int putStatus;
    int removeStatus;
    int getStatus;


    public NativeDictionary(int capacity) {
        this.capacity = capacity;
        slots = new String[capacity];
        values = (T[]) new Object[capacity];

        putStatus = PUT_NIL;
        removeStatus = REMOVE_NIL;
        getStatus = GET_NIL;
    }


    public void put(String key, T value) {
        int slot = seekSlot(key);
        if (slot == -1 || value == null) {
            putStatus = PUT_ERR;
        } else {
            slots[slot] = key;
            values[slot] = value;
            size++;
            putStatus = PUT_OK;
        }
    }

    public void remove(String key) {
        int slot = seekSlot(key);
        if (slot == -1) {
            removeStatus = REMOVE_ERR;
        } else {
            slots[slot] = null;
            values[slot] = null;
            size--;
            removeStatus = REMOVE_OK;
        }
    }


    public T get(String key) {
        T result;
        int slot = seekSlot(key);
        if (slot == -1 || values[slot] == null) {
            result = null;
            getStatus = GET_ERR;
        } else {
            result = values[slot];
            getStatus = GET_OK;
        }
        return result;
    }

    public boolean containsKey(String key) {
        int slot = seekSlot(key);
        return slot != -1 && slots[slot] != null;
    }

    public int size() {
        return size;
    }

    public int getCapacity() {
        return capacity;
    }


    public int get_put_status(){
        return putStatus;
    }

    public int get_remove_status(){
        return removeStatus;
    }

    public int get_get_status(){
        return getStatus;
    }


    private int seekSlot(String key) {
        int hash = hashFun(key);
        if (hash == -1) {
            return -1;
        }
        int slot = hash;
        while (slots[slot] != null) {
            if (slots[slot].equals(key)) {
                return slot;
            }
            slot = (slot + 1) % capacity;
            if (slot == hash) {
                return -1;
            }
        }
        return slot;
    }

    private int hashFun(String key) {
        return key == null ? -1 : Math.abs(key.hashCode()) % capacity;
    }
}
