# Пример 1 и Вывод

Рассмотрим пример со стеком из основной статьи со стеком. Если у нас есть какая-то реализация стека:

```java
class MyStack<T> {
    void push(T item) {...}
    T pop() {...}
    T peek() {...}
    boolean isEmpty() {...}
    int size() {...}
}
```

то в Java у нас нет возможности влоб подстроить содержимое интерфейса под реализацию: два разных интерфейса будут идентичны с точностью до самого названия интерфейса ввиду необходимости имплеменировать методы с той же сигнатурой:

```java
interface Stack<T> {
    void push(T item);
    T pop();
    T peek();
    boolean isEmpty();
    int size();
}

class SomeStack<T> implements Stack<T> {
    ...
    
    @Override
    public void push(T item) {...}
    @Override
    public T pop() {...}
    @Override
    public T peek() {...}
    @Override
    public boolean isEmpty() {...}
    @Override
    public int size() {...}
}

class OtherStack<T> implements Stack<T> { // Class 'OtherStack' must either be declared abstract or implement abstract method 'size()' in 'Stack'
    ...
    
    @Override
    public void push(T item) {...}
    @Override
    public T pop() {...}
    @Override
    public T peek() {...}
    @Override
    public boolean isEmpty() {...}
    public int otherSize() {...}
}
```

Можно, конечно, сделать так:

```java
class OtherStack<T> implements Stack<T> {
    ...
    
    @Override
    public void push(T item) {...}
    @Override
    public T pop() {...}
    @Override
    public T peek() {...}
    @Override
    public boolean isEmpty() {...}
    @Override
    public int size() {
        return this.otherSize();
    }
    public int otherSize() {...}
}
```

но выглядит это не очень выразительно. Обычно методы класса все же называют достаточно конкретно, такие же конкретные имена будет содержать и интерфейс. Наверное, имеено поэтому идея "реализация может удовлетворять нескольким интерфейсам" не получает столь большой популярности в массах.

В качестве более взрослой реализации можно рассмотреть использование делегата:

```java
interface CommandHistory {
    void saveCommand(Command command);
    Command undo();
}

interface PlateStack {
    void putPlate(Plate plate);
    Plate takePlate();
}

class CommandHistoryImpl implements CommandHistory {
    private final SomeStack<Command> commands = new SomeStack<>();

    public void saveCommand(Command command) {
        stack.push(command);
    }

    public Command undo() {
        return stack.pop();
    }
}

class PlateStackImpl implements PlateStack {
    private final SomeStack<Plate> plates = new SomeStack<>();

    public void putPlate(Plate plate) {
        stack.push(plate);
    }

    public Plate takePlate() {
        return stack.pop();
    }
}
```

или интерфейсы с дефолтными методами:

```java
interface CommandHistory {
    void push(Command command);
    Command pop();

    default Command undo() {
        return pop();
    }

    default void saveCommand(Command command) {
        push(command);
    }
}

class CommandHistoryImpl implements CommandHistory {
    private final SomeStack<Command> stack = new SomeStack<>();

    public void push(Command item) {
        stack.push(item);
    }

    public Command pop() {
        return stack.pop();
    }
}
```

В обоих этих случаях идет завязка на конкретные типы, от которых можно уйти с помощью дженериков:

```java
interface History<T> {
    void push(T item);
    T pop();

    default T undo() {
        return pop();
    }

    default void save(T item) {
        push(item);
    }
}
```

В таком случае мы приблизились к получению отношения "многие ко многим", вычленив из частных интерфейсов -- общие, которые сможем переиспользовать не только в классическом "интерфейс может иметь несколько реализаций". Единственное -- остается невыразительность их применения.

В Kotlin можно воспользоваться следующим трюком:

```kotlin
interface History<T> {
    fun save(command: T)
    fun undo(): T
}

fun <T> SomeStack<T>.asHistory(): History<T> = object : History<T> {
    override fun save(command: T) = push(command)
    override fun undo(): T = pop()
}

fun main() {
    val history: History<Command> = Stack<Command>().asHistory() // можно завернуть в фабрику
    history.save(Command())
    history.save(Command())
    println(history.undo())
}
```

# Пример 2

```kotlin
class TimeSequence {
    private val times = mutableListOf<Instant>()

    fun add(time: Instant) {
        times.add(time)
        times.sort()
    }

    fun pollNext(): Instant? = times.removeFirstOrNull()
    fun count(): Int = times.size
}

// список будущих попыток выполнения задачи
interface RetrySchedule {
    fun nextRetry(): Instant?
    fun addRetryTime(time: Instant)
    fun retriesLeft(): Int
}

// список ключевых кадров анимации
interface AnimationTimeline {
    fun nextFrameTime(): Instant?
    fun addKeyFrame(time: Instant)
    fun totalFrames(): Int
}

fun TimeSequence.asRetrySchedule(): RetrySchedule = object : RetrySchedule {
    override fun nextRetry(): Instant? = pollNext()
    override fun addRetryTime(time: Instant) = add(time)
    override fun retriesLeft(): Int = count()
}

fun TimeSequence.asAnimationTimeline(): AnimationTimeline = object : AnimationTimeline {
    override fun nextFrameTime(): Instant? = pollNext()
    override fun addKeyFrame(time: Instant) = add(time)
    override fun totalFrames(): Int = count()
}
```

# Пример 3

```kotlin
class CounterMap {
    private val counts = mutableMapOf<String, Int>()

    fun increment(key: String, by: Int = 1) {
        counts[key] = counts.getOrDefault(key, 0) + by
    }

    fun get(key: String): Int = counts.getOrDefault(key, 0)

    fun total(): Int = counts.values.sum()
}

// считает количество голосов от пользователей
interface UserVoteCounter {
    fun vote(userId: String)
    fun voteCount(userId: String): Int
    fun totalVotes(): Int
}

// считает количество предметов на складе
interface InventoryCounter {
    fun addItem(itemId: String, quantity: Int = 1)
    fun itemCount(itemId: String): Int
    fun totalItems(): Int
}

fun CounterMap.asUserVoteCounter(): UserVoteCounter = object : UserVoteCounter {
    override fun vote(userId: String) = this@asUserVoteCounter.increment(userId)
    override fun voteCount(userId: String): Int = this@asUserVoteCounter.get(userId)
    override fun totalVotes(): Int = this@asUserVoteCounter.total()
}

fun CounterMap.asInventoryCounter(): InventoryCounter = object : InventoryCounter {
    override fun addItem(itemId: String, quantity: Int) = increment(itemId, quantity)
    override fun itemCount(itemId: String): Int = get(itemId)
    override fun totalItems(): Int = total()
}
```