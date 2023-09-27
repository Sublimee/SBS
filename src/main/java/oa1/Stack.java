package oa1;

import java.util.ArrayList;
import java.util.List;

/**
 * АТД Stack
 *
 * abstract class Stack<T>
 *
 *  интерфейс класса, реализующий АТД Stack
 *  public final int PUSH_NIL = 0;  // push() ещё не вызывалась
 *  public final int PUSH_OK = 1;   // последняя push() отработала нормально
 *
 *  public final int POP_NIL = 0;   // pop() ещё не вызывалась
 *  public final int POP_OK = 1;    // последняя pop() отработала нормально
 *  public final int POP_ERR = 2;   // стек пуст
 *
 *  public final int PEEK_NIL = 0;  // peek() ещё не вызывалась
 *  public final int PEEK_OK = 1;   // последняя peek() вернула корректное значение
 *  public final int PEEK_ERR = 2;  // стек пуст
 *
 *  // конструктор
 *  // постусловие: создан новый пустой стек
 *  public Stack<T> Stack();
 *
 *  // команды:
 *
 *  // постусловие: в стек добавлено новое значение
 *  public void push(T value);
 *
 *  // предусловие: стек не пустой;
 *  // постусловие: из стека удалён верхний элемент
 *  public void pop();
 *
 *  // постусловие: из стека удалятся все значения
 *  public void clear();
 *
 *  // запросы:
 *
 *  // предусловие: стек не пустой
 *  public T peek();
 *
 *  public int size();
 *
 *  // дополнительные запросы:
 *
 *  public int get_push_status(); // возвращает значение PUSH_*
 *  public int get_pop_status(); // возвращает значение POP_*
 *  public int get_peek_status(); // возвращает значение PEEK_*
 */
public class Stack<T> {

    // интерфейс класса, реализующий АТД Stack
    public final int PUSH_NIL = 0;  // push() ещё не вызывалась
    public final int PUSH_OK = 1;   // последняя push() отработала нормально

    public final int POP_NIL = 0;   // pop() ещё не вызывалась
    public final int POP_OK = 1;    // последняя pop() отработала нормально
    public final int POP_ERR = 2;   // стек пуст

    public final int PEEK_NIL = 0;  // peek() ещё не вызывалась
    public final int PEEK_OK = 1;   // последняя peek() вернула корректное значение
    public final int PEEK_ERR = 2;  // стек пуст

    // скрытые поля
    private List<T> stack;          // основное хранилище стека
    private int push_status;        // статус запроса push()
    private int peek_status;        // статус запроса peek()
    private int pop_status;         // статус команды pop()

    // конструктор
    // постусловие: создан новый пустой стек
    public Stack() {
        clear();
    }

    // команды:

    // постусловие: в стек добавлено новое значение
    public void push(T value) {
        stack.add(value);
        push_status = PUSH_OK;
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
        stack = new ArrayList<>(); // пустой список/стек

        // начальные статусы для push() и предусловий peek() и pop()
        push_status = PUSH_NIL;
        peek_status = PEEK_NIL;
        pop_status = POP_NIL;
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

    // возвращает значение PUSH_*
    public int get_push_status() {
        return push_status;
    }

    // возвращает значение POP_*
    public int get_pop_status() {
        return pop_status;
    }

    // возвращает значение PEEK_*
    public int get_peek_status() {
        return peek_status;
    }
}