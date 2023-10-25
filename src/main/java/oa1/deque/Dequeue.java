package oa1.deque;

/*

АТД ParentQueue

abstract class ParentQueue<T> {

    // интерфейс класса, реализующий АТД ParentQueue

    public final int REMOVE_FRONT_NIL = 0;    // remove_front() еще не вызывалась
    public final int REMOVE_FRONT_OK = 1;     // последняя команда отработала нормально
    public final int REMOVE_FRONT_ERR = 2;    // очередь пуста

    public final int GET_FRONT_NIL = 0;      // get_front() ещё не вызывалась
    public final int GET_FRONT_OK = 1;       // последняя get_front() вернула корректное значение
    public final int GET_FRONT_ERR = 2;      // очередь пуста

    // конструктор

    // постусловие: создана новая пустая очередь
    public ParentQueue<T> ParentQueue();


    // команды

    // постусловие: значение добавлено в хвост очереди
    public void add_tail(T item);

    // предусловие: очередь не пуста
    // постусловие: элемент удален из головы очереди
    public void remove_front();


    // запросы

    // предусловие: очередь не пуста
    public T get_front();    // получить элемент из головы очереди

    public int size();  // получить количество элементов в очереди


    // дополнительные запросы:

    // возвращает значение REMOVE_FRONT_
    public int get_remove_front_status();

    // возвращает значение GET_FRONT_
    public int get_get_front_status();
}


АТД Queue

abstract class Queue<T> : ParentQueue<T> {

    // конструктор

    // постусловие: создана новая пустая очередь
    public Queue<T> Queue();
}


АТД Deque

abstract class Deque<T> : ParentQueue<T> {

    // интерфейс класса, реализующий АТД Deque

    public final int REMOVE_TAIL_NIL = 0;    // remove_tail() еще не вызывалась
    public final int REMOVE_TAIL_OK = 1;     // последняя команда отработала нормально
    public final int REMOVE_TAIL_ERR = 2;    // очередь пуста

    public final int GET_TAIL_NIL = 0;      // get_tail() ещё не вызывалась
    public final int GET_TAIL_OK = 1;       // последняя get_tail() вернула корректное значение
    public final int GET_TAIL_ERR = 2;      // очередь пуста

    // конструктор

    // постусловие: создана новая пустая очередь
    public Deque<T> Deque();


    // команды

    // постусловие: значение добавлено в голову очереди
    public void add_front(T item);

    // предусловие: очередь не пуста
    // постусловие: элемент удален из хвоста очереди
    public void remove_tail();


    // запросы

    // предусловие: очередь не пуста
    public T get_tail(); // получить элемент из хвоста очереди


    // дополнительные запросы:

    // возвращает значение REMOVE_TAIL_
    public int get_remove_tail_status();

    // возвращает значение GET_TAIL_
    public int get_get_tail_status();
}
*/

import java.util.LinkedList;

abstract class ParentQueue<T> {

    public final int REMOVE_FRONT_NIL = 0;
    public final int REMOVE_FRONT_OK = 1;
    public final int REMOVE_FRONT_ERR = 2;

    public final int GET_FRONT_NIL = 0;
    public final int GET_FRONT_OK = 1;
    public final int GET_FRONT_ERR = 2;

    protected final LinkedList<T> queue;

    private int removeFrontStatus;
    private int getFrontStatus;


    public ParentQueue() {
        queue = new LinkedList<>();
        removeFrontStatus = REMOVE_FRONT_NIL;
        getFrontStatus = GET_FRONT_NIL;
    }


    public void add_tail(T item) {
        queue.addLast(item);
    }

    public void remove_front() {
        if (size() == 0) {
            removeFrontStatus = REMOVE_FRONT_ERR;
        } else {
            queue.removeFirst();
            removeFrontStatus = REMOVE_FRONT_OK;
        }
    }


    public T get_front() {
        T result;
        if (size() == 0) {
            result = null;
            getFrontStatus = GET_FRONT_ERR;
        } else {
            result = queue.getFirst();
            getFrontStatus = GET_FRONT_OK;
        }
        return result;
    }

    public int size() {
        return queue.size();
    }


    public int get_remove_front_status() {
        return removeFrontStatus;
    }

    public int get_get_front_status() {
        return getFrontStatus;
    }
}

class Queue<T> extends ParentQueue<T> {
}

class Dequeue<T> extends ParentQueue<T> {

    public final int REMOVE_TAIL_NIL = 0;
    public final int REMOVE_TAIL_OK = 1;
    public final int REMOVE_TAIL_ERR = 2;

    public final int GET_TAIL_NIL = 0;
    public final int GET_TAIL_OK = 1;
    public final int GET_TAIL_ERR = 2;

    private int removeTailStatus;
    private int getTailStatus;


    public Dequeue() {
        super();
        removeTailStatus = REMOVE_TAIL_NIL;
        getTailStatus = GET_TAIL_NIL;
    }


    public void add_front(T item) {
        queue.addFirst(item);
    }

    public void remove_tail() {
        if (size() == 0) {
            removeTailStatus = REMOVE_TAIL_ERR;
        } else {
            queue.removeLast();
            removeTailStatus = REMOVE_TAIL_OK;
        }
    }


    public T get_tail() {
        T result;
        if (size() == 0) {
            result = null;
            getTailStatus = GET_TAIL_ERR;
        } else {
            result = queue.getLast();
            getTailStatus = GET_TAIL_OK;
        }
        return result;
    }


    public int get_remove_tail_status() {
        return removeTailStatus;
    }

    public int get_get_tail_status() {
        return getTailStatus;
    }
}