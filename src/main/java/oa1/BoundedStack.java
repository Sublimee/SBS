package oa1;

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
public class BoundedStack {
}
