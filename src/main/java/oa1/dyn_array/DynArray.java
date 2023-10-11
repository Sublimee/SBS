package oa1.dyn_array;

/*

АТД DynArray

abstract class DynArray<T> {

    // интерфейс класса, реализующий АТД DynArray

    public final int INSERT_NIL = 0;    // insert() еще не вызывалась
    public final int INSERT_OK = 1;     // последняя команда отработала нормально
    public final int INSERT_ERR = 2;    // переданный индекс отрицательный или он больше числа элементов в массиве

    public final int REMOVE_NIL = 0;    // remove() еще не вызывалась
    public final int REMOVE_OK = 1;     // последняя команда отработала нормально
    public final int REMOVE_ERR = 2;    // переданный индекс отрицательный или он больше или равен числу элементов в массиве

    public final int GET_NIL = 0;       // get() ещё не вызывалась
    public final int GET_OK = 1;        // последняя команда отработала нормально
    public final int GET_ERR = 2;       // переданный индекс отрицательный или он больше или равен числу элементов в массиве


    // конструктор

    // постусловие: создан новый динамический массив
    public DynArray();


    // команды

    // постусловие: в хвост вставлено новое значение. Если для нового элемента не хватает места, то емкость
    // предварительно увеличивается
    public void append(T itm);

    // предусловие: переданный индекс неотрицательный и он меньше или равен числу элементов в массиве
    // постусловие: в позицию index вставлено новое значение, а все последующие элементы (если таковые есть) сдвинуты
    // вперед. Если для сдвига элементов не хватает места, то емкость массива предварительно увеличивается
    public void insert(T itm, int index);

    // предусловие: переданный индекс неотрицательный и он меньше числа элементов в массиве
    // постусловие: значение по указанному индексу удалено
    public void remove(int index);


    // запросы

    // предусловие: переданный индекс неотрицательный и он меньше числа элементов в массиве
    public T get(int index);    // получить значение по индексу в массиве

    public int size();          // получить количество элементов в массиве


    // дополнительные запросы:

    // возвращает значение INSERT_
    public int get_insert_status();

    // возвращает значение REMOVE_
    public int get_remove_status();

    // возвращает значение GET_
    public int get_get_status();
}
*/

public class DynArray<T> {

    public final int INSERT_NIL = 0;    // insert() еще не вызывалась
    public final int INSERT_OK = 1;     // последняя команда отработала нормально
    public final int INSERT_ERR = 2;    // переданный индекс отрицательный или он больше числа элементов в массиве

    public final int REMOVE_NIL = 0;    // remove() еще не вызывалась
    public final int REMOVE_OK = 1;     // последняя команда отработала нормально
    public final int REMOVE_ERR = 2;    // переданный индекс отрицательный или он больше или равен числу элементов в массиве

    public final int GET_NIL = 0;       // get() ещё не вызывалась
    public final int GET_OK = 1;        // последняя команда отработала нормально
    public final int GET_ERR = 2;       // переданный индекс отрицательный или он больше или равен числу элементов в массиве


    private T[] array;
    private int size;

    private int insertStatus;
    private int removeStatus;
    private int getStatus;


    // конструктор

    // постусловие: создан новый динамический массив
    public DynArray() {
        array = (T[]) new Object[16];
        size = 0;
        insertStatus = INSERT_NIL;
        removeStatus = REMOVE_NIL;
        getStatus = GET_NIL;
    }


    // команды

    // постусловие: в хвост вставлено новое значение. Если для нового элемента не хватает места, то емкость
    // предварительно увеличивается
    public void append(T itm) {
        if (size == array.length) {
            increaseCapacity();
        }
        array[size] = itm;
        size++;
        insertStatus = INSERT_OK;
    }

    // предусловие: переданный индекс неотрицательный и он меньше или равен числу элементов в массиве
    // постусловие: в позицию index вставлено новое значение, а все последующие элементы (если таковые есть) сдвинуты
    // вперед. Если для сдвига элементов не хватает места, то емкость массива предварительно увеличивается
    public void insert(T itm, int index) {
        if (index < 0 || index > size) {
            insertStatus = INSERT_ERR;
        } else {
            if (size == array.length) {
                increaseCapacity();
            }
            System.arraycopy(this.array, index, this.array, index + 1, size - index);
            array[index] = itm;
            size++;
            insertStatus = INSERT_OK;
        }
    }

    // предусловие: переданный индекс неотрицательный и он меньше числа элементов в массиве
    // постусловие: значение по указанному индексу удалено
    public void remove(int index) {
        if (index < 0 || index >= size) {
            removeStatus = REMOVE_ERR;

        } else {
            System.arraycopy(this.array, index + 1, this.array, index, array.length - index - 1);
            size--;
            removeStatus = REMOVE_OK;
        }
    }


    // запросы

    // предусловие: переданный индекс неотрицательный и он меньше числа элементов в массиве
    public T get(int index) { // получить значение по индексу в массиве
        T result;
        if (index < 0 || index >= size) {
            result = null;
            getStatus = GET_ERR;
        } else {
            result = array[index];
            getStatus = GET_OK;
        }
        return result;
    }

    public int size() { // получить количество элементов в массиве
        return size;
    }


    // дополнительные запросы:

    // возвращает значение INSERT_
    public int get_insert_status() {
        return insertStatus;
    }

    // возвращает значение REMOVE_
    public int get_remove_status() {
        return removeStatus;
    }

    // возвращает значение GET_
    public int get_get_status() {
        return getStatus;
    }

    private void increaseCapacity() {
        int newCapacity = array.length * 2;
        T[] newArray = (T[]) new Object[newCapacity];
        System.arraycopy(array, 0, newArray, 0, size);
        array = newArray;
    }
}