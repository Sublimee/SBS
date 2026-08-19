# Статья 1

## Примеры 1 и 2

```java
public class Main {
    public static void main(String[] args) {
        // Пример 1
        var results = List.of(
                new GameResult("Alice", 120),
                new GameResult("Bob", 350),
                new GameResult("Charlie", 210),
                new GameResult("Dave", 290)
        );

        var best = Extension.fold(
                results,
                new Max<>(GameResult::new)
        );
        System.out.println(best);

        // Пример 2
        var bonusAccountTransactions = List.of(
                new BonusAccountTransaction(180, 120),
                new BonusAccountTransaction(104, 350),
                new BonusAccountTransaction(180, 210),
                new BonusAccountTransaction(104, 290)
        );

        var stats = Extension.fold(
                bonusAccountTransactions.stream()
                        .map(BonusAccountStatsMapper::from)
                        .toList(),
                new Stats()
        );
        System.out.println(stats);
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

interface Monoid<T> {
    T zero();

    T plus(T left, T right);
}

class Extension {

    public static <T> T fold(
            Collection<T> collection,
            Monoid<T> monoid
    ) {
        return collection.stream()
                .reduce(monoid.zero(), monoid::plus);
    }

}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Пример 1
record GameResult(String player, int score) implements Comparable<GameResult> {

    GameResult() {
        this("", Integer.MIN_VALUE);
    }

    @Override
    public int compareTo(GameResult o) {
        return Integer.compare(score, o.score);
    }
}

class Max<T extends Comparable<T>> implements Monoid<T> {

    private final Supplier<T> zeroSupplier;

    public Max(Supplier<T> zeroSupplier) {
        this.zeroSupplier = zeroSupplier;
    }

    @Override
    public T zero() {
        return zeroSupplier.get();
    }

    @Override
    public T plus(T left, T right) {
        return left.compareTo(right) > 0
                ? left
                : right;
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Пример 2
record BonusAccountTransaction(
        long accountId,
        long bonus) {
}

record BonusAccountStats(
        Map<Long, Long> bonusByAccountId,
        long totalBonus,
        long maxBonus
) {

    BonusAccountStats() {
        this(new HashMap<>(), 0, 0);
    }

    public BonusAccountStats plus(BonusAccountStats other) {
        HashMap<Long, Long> bonusByAccountId = new HashMap<>(this.bonusByAccountId);

        other.bonusByAccountId.forEach(
                (accountId, bonus) -> bonusByAccountId.merge(accountId, bonus, Long::sum)
        );

        return new BonusAccountStats(bonusByAccountId, this.totalBonus + other.totalBonus, Long.max(this.maxBonus, other.maxBonus));
    }
}

class BonusAccountStatsMapper {

    public static BonusAccountStats from(
            BonusAccountTransaction transaction
    ) {
        return new BonusAccountStats(
                Map.of(
                        transaction.accountId(),
                        transaction.bonus()
                ),
                transaction.bonus(),
                transaction.bonus()
        );
    }
}

class Stats implements Monoid<BonusAccountStats> {

    @Override
    public BonusAccountStats zero() {
        return new BonusAccountStats();
    }

    @Override
    public BonusAccountStats plus(BonusAccountStats left, BonusAccountStats right) {
        return left.plus(right);
    }
}
```

# Статья 2

## Пример 3 (доработанный пример 2)

```java
interface Monoid<T> {
    T zero();

    T plus(T left, T right);
}

interface Group<T> extends Monoid<T> {
    T inverse(T item);
}

record BonusAccountTransaction(
        long originalTransactionId,
        long bonusAccountId,
        long bonus
) {
}

record BonusAccountStats(
        Map<Long, Long> bonusByAccountId,
        long totalBonus
) {

    BonusAccountStats {
        bonusByAccountId = Map.copyOf(bonusByAccountId);
    }

    BonusAccountStats() {
        this(Map.of(), 0);
    }

    public BonusAccountStats plus(BonusAccountStats other) {
        var merged = new HashMap<>(bonusByAccountId);

        other.bonusByAccountId.forEach(
                (accountId, bonus) -> merged.merge(accountId, bonus, Long::sum)
        );

        return new BonusAccountStats(
                merged,
                totalBonus + other.totalBonus
        );
    }

    public BonusAccountStats inverse() {
        var inverted = bonusByAccountId.entrySet().stream()
                .collect(Collectors.toMap(
                        Map.Entry::getKey,
                        entry -> -entry.getValue()
                ));

        return new BonusAccountStats(
                inverted,
                -totalBonus
        );
    }
}

class BonusAccountStatsMapper {

    public static BonusAccountStats from(
            BonusAccountTransaction transaction
    ) {
        return new BonusAccountStats(
                Map.of(
                        transaction.bonusAccountId(),
                        transaction.bonus()
                ),
                transaction.bonus()
        );
    }
}

class Stats implements Group<BonusAccountStats> {

    @Override
    public BonusAccountStats zero() {
        return new BonusAccountStats();
    }

    @Override
    public BonusAccountStats plus(
            BonusAccountStats left,
            BonusAccountStats right
    ) {
        return left.plus(right);
    }

    @Override
    public BonusAccountStats inverse(BonusAccountStats item) {
        return item.inverse();
    }
}

sealed interface Event<T>
        permits Add, Remove, Nothing {
}

record Add<T>(T data) implements Event<T> {
}

record Remove<T>(T data) implements Event<T> {
}

record Nothing<T>() implements Event<T> {
}

class History<T> {

    private final List<Event<T>> events = new ArrayList<>();

    public History<T> add(T item) {
        events.add(new Add<>(item));
        return this;
    }

    public History<T> remove(T item) {
        events.add(new Remove<>(item));
        return this;
    }

    public History<T> nothing() {
        events.add(new Nothing<>());
        return this;
    }

    public <S> S reduce(
            Function<T, S> mapper,
            Group<S> group
    ) {
        return events.stream()
                .map(event -> {
                    if (event instanceof Add<?> add) {
                        return mapper.apply((T) add.data());
                    }

                    if (event instanceof Remove<?> remove) {
                        return group.inverse(
                                mapper.apply((T) remove.data())
                        );
                    }

                    if (event instanceof Nothing<?>) {
                        return group.zero();
                    }

                    throw new IllegalStateException("Unknown event: " + event);
                })
                .reduce(
                        group.zero(),
                        group::plus
                );
    }

}

public class GroupExample {

    public static void main(String[] args) {

        var history = new History<BonusAccountTransaction>()
                .add(new BonusAccountTransaction(1, 1, 100))
                .add(new BonusAccountTransaction(2,2, 300))
                .add(new BonusAccountTransaction(3, 1, 50))
                .add(new BonusAccountTransaction(4,3, 200))
                .remove(new BonusAccountTransaction(2, 2, 300));

        var stats = history.reduce(
                BonusAccountStatsMapper::from,
                new Stats()
        );

        System.out.println(stats);
    }
}
```

## Пример 4

```java
interface Monoid<T> {
    T zero();

    T plus(T left, T right);
}

interface Group<T> extends Monoid<T> {
    T inverse(T item);
}

record Move(
        int dx,
        int dy
) {
    Move() {
        this(0, 0);
    }

    public Move plus(Move other) {
        return new Move(this.dx + other.dx, this.dy + other.dy);
    }

    public Move inverse() {
        return new Move(-this.dx, -this.dy);
    }
}

class MoveGroup implements Group<Move> {

    @Override
    public Move zero() {
        return new Move();
    }

    @Override
    public Move plus(
            Move left,
            Move right
    ) {
        return left.plus(right);
    }

    @Override
    public Move inverse(Move move) {
        return move.inverse();
    }
}

class Extension {

    public static <T> T fold(
            List<T> collection,
            Monoid<T> monoid
    ) {
        return collection.stream()
                .reduce(monoid.zero(), monoid::plus);
    }

    public static <T> List<T> getReverseRoute(
            List<T> collection,
            Group<T> group
    ) {
        return collection.stream()
                .map(group::inverse).toList().reversed();
    }

}

public class RobotExample {

    public static void main(String[] args) {

        var route = new ArrayList<>(List.of(
                new Move(5, 0),
                new Move(0, 3),
                new Move(-2, 0),
                new Move(0, -1)
        ));

        var destination = Extension.fold(
                route,
                new MoveGroup()
        );

        System.out.println(destination);

        route.addAll(Extension.getReverseRoute(route, new MoveGroup()));

        var roundtrip = Extension.fold(
                route,
                new MoveGroup()
        );

        System.out.println(roundtrip);
    }
}
```


# Вывод

Для первой статьи сделал два примера:
1) поиск максимума, но на Java, чтобы посмотреть, как будет выглядеть моноид в языке; 
2) сбор статистики по бонусным счетам.

Показательно, что для обоих примеров переиспользуется один и тот же метод класса Extension без внесения изменений.

Вообще если не знать математических терминов, то в коде с моноидами это просто fold + стратегия. То же в принципе можно сказать и о группе. Что группа, что моноид -- способы задекларировать контракт при работе с сущностями для быстрой коммуникации с коллегами.

В примере 2 задал имплементацию класса статистики BonusAccountStats с реализацией plus, чего делать, конечно не надо было, так как:
1) теряется гибкость задания Stats (по сравнению с Max);
2) BonusAccountStats начинает знать про plus.

Это противоречит идее универсальности использования моноида. Оставил как напоминание себе.

В примере 3 доработал пример 2, чтобы довести моноид до группы. Пришлось избавиться от вычисления максимума в статистике, так как при откате для него нет обратимой операции.

В примере 4 моделировал движение робота как мы это делали в одном из курсов через задание смещения относительно текущего положения. Группа получилась абелевой, так как в исходную точку можно вернуться с помощью инвертированного набора исходных шагов вне зависимости от их порядка. Как развитие идеи можно было бы предложить начать работать с поворотами на угол и движением вперед.







