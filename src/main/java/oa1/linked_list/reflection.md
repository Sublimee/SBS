1. В предлагаемом решении для меня были не совсем понятны комментарии:

```
    public const int POP_NIL = 0; // push() ещё не вызывалась
    public const int PEEK_NIL = 0; // push() ещё не вызывалась
```

Какое поведение должно быть в соответствии с комментариями выше?

Если вызвать, например, get_pop_status() ПОСЛЕ вызова push(T value), то ни один из статусов в соответствии с АТД (POP_NIL, POP_OK и POP_ERR) не будет отражать сложившуюся ситуацию.

Какое ожидаемое поведение хотим увидеть?

Мы можем вызвать get_pop_status() и get_peek_status() ДО вызова push(T value) и хотим получить соответствующие статусы POP_NIL и PEEK_NIL, которые будут свидетельствовать о том, что pop() и peek() еще не вызывались.

Мы можем вызвать get_pop_status() и get_peek_status() ПОСЛЕ вызова push(T value) и хотим получить соответствующие статусы POP_NIL и PEEK_NIL, которые будут свидетельствовать о том, что pop() и peek() еще не вызывались.

Мной в решении были даны следующие комментарии:

```
    public const int POP_NIL = 0; // pop() ещё не вызывалась
    public const int PEEK_NIL = 0; // peek() ещё не вызывалась
```

2. Для полноты мной был добавлен статус:

```
    public final int POP_NIL = 0;   // pop() ещё не вызывалась
```

3. В моем АТД присутствует 2 конструктора:

```
   // постусловие: создан новый пустой стек на максимум 32 элемента
   public BoundedStack<T> BoundedStack();

   // постусловие: создан новый пустой стек на максимум size элементов
   public BoundedStack<T> BoundedStack(int size);
```

Вариант public BoundedStack<T> BoundedStack(int size); является объемлющим для public BoundedStack<T> BoundedStack(); и если он задан, то через него может быть выражено создание стека любого размера, в том числе конструктор по умолчанию, который формирует стек максимум на 32 элемента. Поэтому можно оставить один конструктор:

```
    public BoundedStack<T> BoundedStack(int size);
```

4. В моем АТД нет метода, который возвращает емкость стека (max_size()), хотя в реализации я этот метод добавил (capacity()). Такой метод стоило добавить для более удобной работы со стеком, хотя он и не является обязательным.