package oa1;

import java.util.ArrayList;
import java.util.List;

/* АТД BoundedStack

abstract class BoundedStack<T>

    интерфейс класса, реализующий АТД BoundedStack

    public final int PUSH_NIL = 0;  // push() ещё не вызывалась
    public final int PUSH_OK = 1;   // последняя push() отработала нормально
    public final int PUSH_ERR = 2;  // стек полон

    public final int POP_NIL = 0;   // pop() ещё не вызывалась
    public final int POP_OK = 1;    // последняя pop() отработала нормально
    public final int POP_ERR = 2;   // стек пуст

    public final int PEEK_NIL = 0;  // peek() ещё не вызывалась
    public final int PEEK_OK = 1;   // последняя peek() вернула корректное значение
    public final int PEEK_ERR = 2;  // стек пуст

    // конструкторы

    // постусловие: создан новый пустой стек на максимум 32 элемента
    public BoundedStack<T> BoundedStack();

    // постусловие: создан новый пустой стек на максимум size элементов
    public BoundedStack<T> BoundedStack(int size);

    // команды:

    // предусловие: стек не полон;
    // постусловие: в стек добавлено новое значение
    public void push(T value);

    // предусловие: стек не пустой;
    // постусловие: из стека удалён верхний элемент
    public void pop();

    // постусловие: из стека удалятся все значения
    public void clear();

    // запросы:

    // предусловие: стек не пустой
    public T peek();

    public int size();

    // дополнительные запросы:

    public int get_push_status();   // возвращает значение PUSH_
    public int get_pop_status();    // возвращает значение POP_
    public int get_peek_status();   // возвращает значение PEEK_

*/
public class BoundedStack<T> {

    // размер стека по умолчанию, если размер не задан явно
    private static final int DEFAULT_INITIAL_CAPACITY = 32;

    // интерфейс класса, реализующий АТД BoundedStack

    public static final int PUSH_NIL = 0;   // push() ещё не вызывалась
    public static final int PUSH_OK = 1;    // последняя push() отработала нормально
    public static final int PUSH_ERR = 2;   // стек полон

    public static final int POP_NIL = 0;    // pop() ещё не вызывалась
    public static final int POP_OK = 1;     // последняя pop() отработала нормально
    public static final int POP_ERR = 2;    // стек пуст

    public static final int PEEK_NIL = 0;   // peek() ещё не вызывалась
    public static final int PEEK_OK = 1;    // последняя peek() вернула корректное значение
    public static final int PEEK_ERR = 2;   // стек пуст

    // скрытые поля
    private List<T> stack;          // основное хранилище стека

    public final int capacity;      // емкость стека

    private int push_status;        // статус запроса push()
    private int peek_status;        // статус запроса peek()
    private int pop_status;         // статус команды pop()

    // конструкторы

    // постусловие: создан новый пустой стек на максимум 32 элемента
    public BoundedStack() {
        this(DEFAULT_INITIAL_CAPACITY);
    }

    // постусловие: создан новый пустой стек на максимум size элементов
    public BoundedStack(int capacity) {
        this.stack = new ArrayList<>(capacity); // пустой список/стек
        this.capacity = capacity;               // фиксируем емкость
        reset_commands_statuses();
    }

    // команды:

    // предусловие: стек не полон
    // постусловие: в стек добавлено новое значение
    public void push(T value) {
        if (size() != capacity) {
            stack.add(value);
            push_status = PUSH_OK;
        } else {
            push_status = PUSH_ERR;
        }
    }

    // предусловие: стек не пустой
    // постусловие: из стека удалён верхний элемент
    public void pop() {
        if (size() > 0) {
            stack.remove(stack.size() - 1);
            pop_status = POP_OK;
        } else {
            pop_status = POP_ERR;
        }
    }

    // постусловие: из стека удалятся все значения
    public void clear() {
        stack = new ArrayList<>(capacity); // пустой список/стек
        reset_commands_statuses();
    }

    // запросы:

    // предусловие: стек не пустой
    public T peek() {
        T result;
        if (size() > 0) {
            result = stack.get(stack.size() - 1);
            peek_status = PEEK_OK;
        } else {
            result = null;
            peek_status = PEEK_ERR;
        }
        return result;
    }

    public int size() {
        return stack.size();
    }

    // дополнительные запросы:

    // возвращает значение PUSH_
    public int get_push_status() {
        return push_status;
    }

    // возвращает значение POP_
    public int get_pop_status() {
        return pop_status;
    }

    // возвращает значение PEEK_
    public int get_peek_status() {
        return peek_status;
    }

    // возвращает емкость стека
    public int capacity() {
        return capacity;
    }

    private void reset_commands_statuses() {
        // начальные статусы для предусловий push(), peek() и pop()
        push_status = PUSH_NIL;
        pop_status = POP_NIL;
        peek_status = PEEK_NIL;
    }
}
