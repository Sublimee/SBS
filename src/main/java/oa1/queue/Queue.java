package oa1.queue;

/*

АТД Queue

abstract class Queue<T> {

    // интерфейс класса, реализующий АТД Queue

    public final int DEQUEUE_NIL = 0;    // dequeue() еще не вызывалась
    public final int DEQUEUE_OK = 1;     // последняя команда отработала нормально
    public final int DEQUEUE_ERR = 2;    // очередь пуста

    public final int PEEK_NIL = 0;      // peek() ещё не вызывалась
    public final int PEEK_OK = 1;       // последняя peek() вернула корректное значение
    public final int PEEK_ERR = 2;      // очередь пуста

    // конструктор

    // постусловие: создана новая пустая очередь
    public Queue();


    // команды

    // постусловие: значение добавлено в хвост очереди
    public void enqueue(T item);

    // предусловие: очередь не пуста
    // постусловие: элемент удален из головы очереди
    public void dequeue();


    // запросы

    // предусловие: очередь не пуста
    public T peek();    // получить элемент из головы очереди

    public int size();  // получить количество элементов в очереди


    // дополнительные запросы:

    // возвращает значение DEQUEUE_
    public int get_dequeue_status();

    // возвращает значение PEEK_
    public int get_peek_status();
}
*/

import java.util.LinkedList;

public class Queue<T> {

    public final int DEQUEUE_NIL = 0;
    public final int DEQUEUE_OK = 1;
    public final int DEQUEUE_ERR = 2;

    public final int PEEK_NIL = 0;
    public final int PEEK_OK = 1;
    public final int PEEK_ERR = 2;

    private final LinkedList<T> queue;

    private int dequeueStatus;
    private int peekStatus;

    public Queue() {
        queue = new LinkedList<>();
        dequeueStatus = DEQUEUE_NIL;
        peekStatus = PEEK_NIL;
    }

    public void enqueue(T item) {
        queue.addLast(item);
    }

    public void dequeue() {
        if (size() == 0) {
            dequeueStatus = DEQUEUE_ERR;
        } else {
            queue.removeFirst();
            dequeueStatus = DEQUEUE_OK;
        }
    }

    // предусловие: очередь не пуста
    public T peek() {
        T result;
        if (size() == 0) {
            result = null;
            peekStatus = PEEK_ERR;
        } else {
            result = queue.getFirst();
            peekStatus = PEEK_OK;
        }
        return result;
    }

    public int size() {
        return queue.size();
    }
}
