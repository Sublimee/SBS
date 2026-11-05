### Генерико-подобные абстракции

#### выражают абстрактные свойства

* не из ФП

Свойство (из Javadoc): This interface imposes a total ordering on the objects of each class that implements it.

```java
interface Comparable<T> {
    int compareTo(T other);
}

class Item implements Comparable<Item> {
    ...
}

<T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) >= 0 ? a : b;
}

Item result = max(...);
```

Нам здесь важно не только то, как называется интерфейс и какая сигнатура у предоставляемого им метода, но и "зашитые" в
него законы, которым должна следовать конкретная реализация. Например, транзитивность.

Comparable здесь вшивает свойство непосредственно в тип, в отличие, например, от Comparator. Это удобно, когда
сравнение идёт всегда по одному сценарию, иначе -- будет скорее сбивать с толку. Comparator'ов же может быть несколько:
каждый под свой сценарий.

* из ФП

```kotlin
interface Monoid<T> {
    val empty: T
    fun combine(a: T, b: T): T
}

val sumMonoid = object : Monoid<Int> {
    override val empty = 0
    override fun combine(a: Int, b: Int) = a + b
}

val multiplicationMonoid = object : Monoid<Int> {
    override val empty = 1
    override fun combine(a: Int, b: Int) = a * b
}

fun <T> fold(xs: List<T>, m: Monoid<T>): T = xs.fold(m.empty, m::combine)

val numbers = listOf(1, 2, 3, 4, 5)

val sum = fold(numbers, sumMonoid)
val multiplication = fold(numbers, multiplicationMonoid)
```

Продолжая идею, затронутую в Comparable, стоит отметить, что хотя контракт для empty и combine не задан явно (значения
можно объединять с помощью ассоциативной операции, для которой есть нейтральный элемент), сама абстракция Monoid его
неявно подразумевает. И мы в реализациях должны его обеспечивать.

Как и Comparator, Monoid сам несёт в себе свойство и не привязан к конкретным классам: для одного класса может быть
несколько моноидов и Comparator'ов.

#### спецификации бессрочны

Так как мы выражаем абстрактные свойства (спецификации), то эти свойства и остаются актуальными независимо от того, с
какими бизнес-требованиями мы сейчас работаем.

* не из ФП

Интерфейс Iterable отвечает за последовательный обход элементов (содержание которых нас не интересует):

```java
interface Iterable<T> {
    Iterator<T> iterator();
}

<T> int count(Iterable<T> elements) {
    int count = 0;

    for (T element : elements) {
        count++;
    }

    return count;
}
```

Идея (спецификация) не поменяется, даже если поменяется объявление интерфейса. Ну и, понятно, что на основе Iterable
могут появляться новые реализации, а старые -- отмирать.

Сам Iterable, конечно, "слабее" того же Comparable с точки зрения (математических) законов: формально они не заданы, но 
мы ожидаем, что за один обход каждый элемент будет выдан ровно один раз. Тем не менее этого достаточно, чтобы 
рассматривать его отдельно от какой-либо предметной области и занести в клуб бессрочных.

* из ФП

На основе того же Monoid с изменением какой-то логики (в нашем случае работы с деньгами) могут появляться новые 
реализации:

```kotlin
val sumMoneyMonoid = object : Monoid<Int> { ...
val total = fold(payments, sumMoneyMonoid)
                    ↓
val sumMoneyMonoid = object : Monoid<BigDecimal> { ...
val total = fold(payments, sumMoneyMonoid)
                    ↓
val sumMoneyMonoid = object : Monoid<Money> { ...
val total = fold(payments, sumMoneyMonoid)
```

Сами же законы, заключённые в Monoid, остаются неизменными.

#### используются для идентификации идиом (не буквальный смысл)

Выводим закономерности в разных алгоритмах. Абстракция должна получиться такой, что не будет привязана к конкретному
домену.

* не из ФП

Обход разных коллекций элементов:

```java
...
// обход массива
for (int i = 0; i < array.length; i++) {
    process(array[i]);
}
...
// обход списка
Node current = head;
while (current != null) {
    process(current.value);
    current = current.next;
}
...
```

сводится к переходу от элемента к элементу. Эту идею отражает итератор:

```java
interface Iterator<T> {
    boolean hasNext();
    T next();
}
```

* из ФП

Издалека виден повторяющийся приём преобразования коллекций:

```java
List<User> users = ...;
List<String> names = new ArrayList<>();

for (User user : users) {
    names.add(user.getName());
}

Set<Product> products = ...;
List<String> titles = new ArrayList<>();

for (Product product : products) {
    titles.add(product.getTitle());
}

Queue<Order> orders = ...;
List<Long> ids = new ArrayList<>();

for (Order order : orders) {
    ids.add(order.getId());
}
```

Алгоритмы сводятся к одной идее с map, который ничего не говорит нам и сам ничего не знает о конкретном домене:

```java
List<String> names = users.stream()
    .map(User::getName)
    .toList();

List<String> titles = products.stream()
    .map(Product::getTitle)
    .toList();

List<Long> ids = orders.stream()
    .map(Order::getId)
    .toList();
```

#### статическая типизация

Соблюдение явных требований абстракции проверяется на этапе компиляции.

* не из ФП

Возьмём метод max из примера выше:

```java
record User(...) {}

max(new User(...), new User(...));
```

и в соответствующей строке получим ошибку компиляции из-за использования типа User, который не удовлетворяет ограничению
T extends Comparable<T>.

* из ФП

Возьмём моноид из примера выше:

```kotlin
fold(listOf(1), sumMonoid) // без ошибок компиляции
fold(listOf("a"), sumMonoid) // выдаст ошибку компиляции: Monoid<Int> не подходит для List<String>
```

#### полиморфизм времени компиляции

Какая реализация будет вызвана, определяет компилятор по статически заданным типам, а не класс объекта в рантайме, как
при динамическом полиморфизме.

* не из ФП

Компилятор выбирает перегруженный метод по тому, обладает ли тип свойством Comparable:

```java
void kind(Object o) {
    ...
}

<T extends Comparable<T>> void kind(T c) {
    ...
}

Object x = 1;
kind(x); // в рантайме Integer, но компилятор видит Object, поэтому будет выбран первый метод
kind(1); // Integer подходит под оба метода, но второй будет выбран как более специфичный
```

* из ФП

Выбор моноида по типу элементов списка:

```kotlin
val sumMoneyMonoid = object : Monoid<Money> { ...

fun List<Int>.combineAll(): Int = fold(sumMonoid.empty, sumMonoid::combine)
fun List<Money>.combineAll(): Money = fold(sumMoneyMonoid.empty, sumMoneyMonoid::combine)

listOf(1, 2, 3).combineAll() // List<Int>.combineAll()
listOf(Money(...), Money(...)).combineAll() // List<Money>.combineAll()

emptyList<Int>().combineAll() // List<Int>.combineAll()
emptyList<Money>().combineAll() // List<Money>.combineAll()
```

Компилятор определяет нужный вызов combineAll по типу списка. В рантайме же type erasure не даёт нам в принципе
различить два списка разных типов, а соответственно и выбрать правильный combineAll. Пустые списки -- ещё более сильный 
пример: в рантайме у них нет ни элементов, ни информации о типе, а нужная версия всё равно вызывается (скажем спасибо 
компилятору).

#### механизм генерализации

Позволяет один раз написать код обработки всех типов для заданной абстракции (обладающих нужным свойством). Это 
продолжение идеи выделения идиом. Там мы разный по форме, но не по смыслу код заворачивали в одну 
абстракцию. Здесь же эту абстракцию используем, чтобы обобщённо решать определённую задачу так же на разных типах.

* не из ФП

Теперь решения из блока "используются для идентификации идиом" можно генерализировать:

```java
<T> void processAll(Iterator<T> iterator) {
    while (iterator.hasNext()) {
        process(iterator.next());
    }
}
...
processAll(list.iterator());
processAll(Arrays.asList(new Integer[] { 1, 2, 3 }).iterator());
```

* из ФП

Ранее уже показывали генерализацию при работе с разными моноидами:

```kotlin
fun <T> fold(xs: List<T>, m: Monoid<T>): T = xs.fold(m.empty, m::combine)

val moneyTotal = fold(listOf<Money>(...), sumMoneyMonoid)
val ratio = fold(listOf<Ratio>(...), ratioMultiplierMonoid) // empty = 1, combine = a * b
```

### Интерфейсо-подобные абстракции

#### выражают понятия предметной области

Парное свойство к «выражают абстрактные свойства». Выражают не абстрактные (универсальные математические) свойства, а 
вполне конкретные понятия предметной области.

* не из ФП

Интерфейс выражает вполне конкретное понятие -- правила расчёта кэшбэка для транзакции:

```java
interface CashbackRule {
    long calculate(Transaction tx);
}

class StandardCashback implements CashbackRule {
    public long calculate(Transaction tx) {
        return tx.amountMinors() / 100;
    }
}

class PremiumCashback implements CashbackRule {
    public long calculate(Transaction tx) {
        return tx.amountMinors() * 5 / 100;
    }
}
```

* из ФП

Тот же пример, только вместо интерфейса и реализаций поведение задаётся функциями с алиасом CashbackRule в сигнатуре.
Алиас позволяет лучше показать человеку понятие предметной области. Компилятору же всё равно: что CashbackRule, что
маппинг из Transaction в Long.

```kotlin
typealias CashbackRule = (Transaction) -> Long

val standardCashback: CashbackRule = { tx -> tx.amountMinors / 100 }
val premiumCashback: CashbackRule = { tx -> tx.amountMinors * 5 / 100 }

fun calculate(tx: Transaction, rule: CashbackRule): Long = rule(tx)
```

Как мы передаём CashbackRule в качестве аргумента-правила в calculate, так же мы передавали и Monoid в fold. Но разница 
в том, что они выражают (математическое свойство / закон vs банковский домен / бизнес-правило).

#### реализации имеют срок действия

Парное свойство к «спецификации бессрочны». Жизненный цикл реализаций CashbackRule ограничен временем жизни требований 
бизнеса.

* не из ФП

От:

```java
class StandardCashback implements CashbackRule {
    public long calculate(Transaction tx) {
        return tx.amountMinors() / 100;
    }
}

class PremiumCashback implements CashbackRule {
    public long calculate(Transaction tx) {
        return tx.amountMinors() * 5 / 100;
    }
}
```

при пересмотре тарифов клиентов мы можем прийти, например, к такому изменённому набору:

```java
class StandardCashback implements CashbackRule {
    public long calculate(Transaction tx) {
        return tx.amountMinors() * 2 / 100;
    }
}

class PrivateCashback implements CashbackRule {
    public long calculate(Transaction tx) {
        return tx.amountMinors() * 10 / 100;
    }
}
```

Одни реализации появляются (PrivateCashback), другие -- исчезают (PremiumCashback), третьи -- меняются
(StandardCashback).

* из ФП

Аналогично:

```kotlin
val standardCashback: CashbackRule = { tx -> tx.amountMinors * 2 / 100 }
val privateCashback: CashbackRule = { tx -> tx.amountMinors * 10 / 100 }
```

Тут стоит отметить разницу между меняющимися правилами начисления кэшбэка и разными реализациями суммирования денег при 
помощи моноидов, которые тоже сменяли друг друга.

Реализации PremiumCashback и StandardCashback стали некорректными после изменения бизнес-правил, а вот моноид 
sumMoneyMonoid, например, для Int продолжает в математическом смысле сохранять актуальность (остаётся корректным), 
но был заменён из-за смены типа данных.

#### используются для конструирования паттернов

Парное свойство к «используются для идентификации идиом». Если идиомы распознают в уже написанном коде, то паттерны 
закладывают при проектировании, заранее продумывая решение из строительных блоков. Отсюда следствие: если выделение 
идиомы приводит к множеству безболезненных локальных улучшений в коде, то неиспользование интерфейсо-подобных абстракций 
вовсе или некорректно выбранные паттерны, которые по сути являются фундаментом, могут привести к переработке архитектуры 
сервиса.

* не из ФП

Сам CashbackRule уже представлял собой паттерн Стратегия: мы можем использовать одну из реализаций расчёта кэшбэка в 
зависимости от обстоятельств. Можем поверх этой идеи собрать Декоратор для ограничения суммы начисления по одной 
транзакции:

```java
class BoundedCashback implements CashbackRule {
    private final CashbackRule rule;
    private final long maxMinors;

    BoundedCashback(CashbackRule rule, long maxMinors) {
        this.rule = rule;
        this.maxMinors = maxMinors;
    }

    public long calculate(Transaction tx) {
        return Math.min(rule.calculate(tx), maxMinors);
    }
}

CashbackRule rule = new BoundedCashback(new PremiumCashback(), 5_000_000);
```

BoundedCashback работает не с конкретными реализациями, а с интерфейсом CashbackRule, поэтому декораторы можно
вкладывать друг в друга и комбинировать с любыми реализациями правил.

* из ФП

Те же паттерны собираются функциями высшего порядка: декоратор -- это функция, которая принимает CashbackRule и 
возвращает новый CashbackRule:

```kotlin
fun bounded(rule: CashbackRule, maxMinors: Long): CashbackRule =
    { tx -> minOf(rule(tx), maxMinors) }

fun onlyFor(category: Category, rule: CashbackRule): CashbackRule =
    { tx -> if (tx.category == category) rule(tx) else 0 }

val restaurantPromo: CashbackRule =
    bounded(onlyFor(Category.RESTAURANTS, premiumCashback), maxMinors = 5_000_000)
```

"Ограничение суммы кэшбэка по операции в определённой категории" собираем как композицию функций. Каждая функция знает
только о CashbackRule.

#### динамическая реализация (рантайм)

Парное свойство к «статической типизации». Там требования абстракции проверялись при 
компиляции. Компилятор знал, с каким типом работает. Здесь компилятор знает только интерфейс, а конкретная 
реализация будет выбираться в рантайме в зависимости от приходящих извне данных, например, заголовков запроса, 
конфигурации сервиса, установленного фичатогла в БД и т.д.

* не из ФП

Правило кэшбэка выбирается по пакету услуг клиента:

```java
@Service
class CashbackService {
    private final Map<ServicePackage, CashbackRule> rules;

    CashbackService(Map<ServicePackage, CashbackRule> rules) {
        this.rules = rules;
    }

    long calculate(Headers headers, Transaction tx) {
        CashbackRule rule = rules.get(headers.getServicePackage());

        return rule.calculate(tx);
    }
}
```

На этапе компиляции неизвестно ни какой пакет услуг у клиента, ни какие есть реализации CashbackRule. За счёт перевода 
клиента на новый пакет услуг пересчёт кэшбэка начнёт идти по новым правилам без изменений в коде и перекомпиляции.

* из ФП

```kotlin
val rules: Map<ServicePackage, CashbackRule> = mapOf(
    ServicePackage.STANDARD to standardCashback,
    ServicePackage.PRIVATE to privateCashback,
)

fun calculate(headers: Headers, tx: Transaction): Long {
    val rule = rules.getValue(headers.servicePackage)

    return rule(tx)
}
```

Выбор реализации в ФП -- выбор конкретной функции из набора. Компилятор знает только, что в rule лежит CashbackRule. 
Какая именно функция там окажется, определяется пакетом услуг из заголовков запроса в момент вызова.

#### динамический полиморфизм

Парное свойство к «полиморфизму времени компиляции». Там реализацию выбирал компилятор по статически заданному типу.
Здесь же одна и та же строка выполняет разный код в зависимости от того, какая конкретная реализация пришла в рантайме.

Это перекликается с предыдущим блоком. Но там мы определяли причину, по которой может быть выбрана та или иная 
реализация (откуда она берётся). Динамический полиморфизм скорее про технический механизм, как выбранная реализация 
попадает в конкретное место вызова.

* не из ФП

```java
List<CashbackRule> rules = List.of(
    new StandardCashback(),
    new PrivateCashback()
);

for (CashbackRule rule : rules) {
    rule.calculate(tx);
}
```

Статический тип у всех элементов один и тот же -- CashbackRule. Соответствующий calculate выбирает JVM в момент вызова
по классу объекта.

* из ФП

```kotlin
val rules: List<CashbackRule> = listOf(
    standardCashback,
    privateCashback,
)

rules.forEach { rule -> rule(tx) }
```

В ФП динамический полиморфизм достаётся нам "бесплатно" вместе с функциями как значениями: rule(tx) просто выполняет ту 
функцию, которая лежит в переменной в момент вызова.

Для выбора реализации часто используют sealed-иерархию и when. Это тоже выбор в рантайме, но его минус в том, что 
под каждую новую реализацию требуется расширение условий when. Интерфейсы и функции не задают ограничения на расширение 
новыми реализациями.

#### механизм инкапсуляции

Парное свойство к «механизму генерализации». Генерализация расширяет область применения: fold работает с любым типом, 
для которого есть моноид. Всё его содержимое -- empty и combine, которые являются проводниками законов, поэтому видны 
снаружи, скрывать их не имеет смысла. Инкапсуляция же, наоборот, скрывает детали реализации. Пользователь абстракции 
знает только "интерфейс". Детали реализаций можно менять, а предоставляемый интерфейс при этом остаётся стабильным.

* не из ФП

PartnerCashback, который является таким же правилом CashbackRule, как и остальные, инкапсулирует условия начислений
партнёрам rates:

```java
class PartnerCashback implements CashbackRule {
    private final PartnerRates rates;

    PartnerCashback(PartnerRates rates) {
        this.rates = rates;
    }

    public long calculate(Transaction tx) {
        long percent = rates.percentFor(tx.offerId());

        return tx.amountMinors() * percent / 100;
    }
}
```

CashbackService из блока про динамическую реализацию по-прежнему знает только о calculate(...). Он не знает о 
существовании rates (нет к ним доступа) и откуда они (например, из БД). Если постановка задачи изменится и условия 
начнут приходить, например, из конфига, то это изменение не повлечёт за собой изменение потребителей любых CashbackRule.

* из ФП

```kotlin
fun partnerCashback(rates: PartnerRates): CashbackRule =
    { tx -> tx.amountMinors * rates.percentFor(tx.offerId) / 100 }

val partnerCashbackRule: CashbackRule = partnerCashback(partnerRates)
```

Замыкание в partnerCashback не даёт доступа к rates снаружи, но это не мешает потребителям использовать
partnerCashbackRule, как и любой другой CashbackRule, без этого знания.

# Вывод

Хочется ещё раз кратко зафиксировать особенности генерико-подобных (ГПА) и интерфейсо-подобных абстракций (ИПА) для
наглядного попарного сравнения:

* ГПА: абстрактные свойства (часто математические), генерализация (во избежание дублирования), стабильность, компиляция
* ИПА: бизнес, инкапсуляция при проектировании домена (ради расширяемости), изменчивость (устаревание, изменение,
расширение), рантайм

Из попарного сравнения свойств видна разница, которая определяется не парадигмой и не синтаксисом, а тем, что выражает
абстракция и когда она отрабатывает. Примеры обоих видов абстракций нашлись и в ФП, и за его пределами, так что
парадигма не ограничивает область их применения.

Но в то же время, если бы некоторые примеры не были снабжены комментариями, то их можно было бы с виду отнести не к тому
парному свойству. Например, реализации sumMoneyMonoid сменяли друг друга, что похоже на "реализации имеют срок
действия", но законы моноида при этом не менялись, а версия для Int осталась корректной. Monoid и CashbackRule одинаково
передаются в функцию как аргументы, но первый выражает математическое свойство, а второй -- бизнес-правило. Comparable
является интерфейсом, но по своей сути -- генерико-подобная абстракция.

Как итог можно сказать, что фундаментом сопровождаемой программы должны быть интерфейсо-подобные абстракции и
динамический полиморфизм (именно они отвечают за расширяемость), а генерико-подобные абстракции за счёт
выделения свойств (в том числе и математических) над хорошей системой доменных типов позволяют обобщать алгоритмы.