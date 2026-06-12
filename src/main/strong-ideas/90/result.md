# Пример 1

Посмотрел исходники WireMock и ответил на давно интересовавший меня вопрос. Чем для меня как для пользователя библиотеки отличаются следующие вызовы?

```kotlin
wireMock.stubFor(post(...
```

```kotlin
stubFor(post(...
```

В первом случае мы работаем с конкретным экземпляром, который поднимается на случайном порту. Во втором случае работа идёт со статически заданным экземпляром, который дефолтно поднимается на порту 8080, что не очень хорошо для целей тестирования, так как этот порт обычно может быть занят.


# Пример 2

Какой пул потоков используется под капотом @Scheduled в Spring? Тут нет никакой магии: это класс, который под капотом содержит ScheduledExecutorService:

```java
public class ThreadPoolTaskScheduler extends ExecutorConfigurationSupport
implements AsyncListenableTaskExecutor, SchedulingTaskExecutor, TaskScheduler {

    ...

	@Nullable
	private ScheduledExecutorService scheduledExecutor;

```

Но интересно другое. С одной стороны, логично, а с другой -- странно увидеть такой его размер:

```java
private volatile int poolSize = 1;
```

Это на практике означает, что задачи выстроятся в очередь и будут выполняться последовательно. Не самое очевидное поведение по умолчанию. Конечно, есть возможность переопределить это значение через конфигурацию. Правда, я ни разу не видел, чтобы это делали. Возможно, потому что нечасто можно встретить более одного @Scheduled в проекте.

# Пример 3

В последнее время ревьюил много PR'ов. Но этот код прошёл мимо меня:

```java
@Override
public void saveWithKeepTtl(String key, Object value) {

    var prefix = KEY_PREFIX_BY_CLASS_NAME.get(value.getClass().getSimpleName());
    var fullKey = BASIC_CACHE_KEY_PREFIX + prefix + key;

    cache.policy().expireAfterWrite().ifPresent(expiration ->
            expiration.ageOf(fullKey).ifPresent(remaining -> {
                cache.put(fullKey, map(value));
                expiration.setExpiresAfter(remaining);
            }));
}
```

Если ключ уже есть в кэше, то не обновляем время его жизни. Здесь смущают сразу две вещи, в которых нужно разобраться:
* работа с policy происходит как будто на глобальном уровне всего кэша;
* ageOf, судя по названию, должен возвращать время, которое запись живёт в кэше, а мы используем его для установления оставшегося времени жизни.

Начинаем разбираться. Предположения по поводу ageOf подтверждаются:

```
Returns the age of the entry based on the expiration policy. The entry's age is the cache's estimate of the amount of time since the entry's expiration was last reset
```

Если посмотреть доку по policy(), то станет очевидно, что мы меняем policy для всего кэша:

```
Returns access to inspect and perform low-level operations on this cache based on its runtime characteristics.
```

А как тогда управлять TTL конкретных ключей? По иронии судьбы на соседней строчке был нужный метод:

![img.png](img.png)

Однако переписывать решение я не стал, потому что понял, что Caffeine не используется в сервисе в принципе, только висит как зависимость в дополнение к Redis. Была надежда на near-cache, но нет :)

В процессе наткнулся на неизвестную ранее мне политику удаления элементов в Caffeine:

```
public Caffeine<K, V> softValues() {
```

со следующим описанием:

```
Specifies that each value (not key) stored in the cache should be wrapped in a SoftReference (by default, strong references are used). Softly-referenced objects will be garbage-collected in a globally least-recently-used manner, in response to memory demand.
...
```

Вообще выглядит логично пытаться защититься от OOM путём оборачивания каждого значения в мягкую ссылку. Как будто надо такое поведение применять чуть ли не по умолчанию?

Но далее читаем предупреждение:

```
...
Warning: in most circumstances it is better to set a per-cache maximum size instead of using soft references. You should only use this method if you are very familiar with the practical consequences of soft references.
...
```

Действительно, защита от OOM достигается обычно за счёт более классического механизма: задаются максимальное количество объектов и объём памяти, который может занимать мапа Caffeine.

Но какой элемент будет удалён при превышении порога? Используется политика Window TinyLfu, которая ориентируется на частоту и давность обращений.

```
   * Eviction:
   * ---------
   * Maximum size is implemented using the Window TinyLfu policy [2] due to its high hit rate, O(1)
   * time complexity, and small footprint. A new entry starts in the admission window and remains
   * there as long as it has high temporal locality (recency). ... If the main space is already 
   * full, then a historic frequency filter determines whether to evict the newly admitted entry or
   * the victim entry chosen by the eviction policy. ...
```

Она, к сожалению или к счастью, не настраивается.

Если мы говорим об очистке с помощью GC, то порядок удаления будет непредсказуем. Если удалять свежие ключи, то мы можем наблюдать потерю, а не рост производительности. Caffeine выставляет CacheStats, поэтому можно провести НТ на разных режимах, чтобы понять, какой из них лучше подходит при заданном профиле нагрузки.

# Вывод

К сожалению, досконально знать все зависимости в развивающемся проекте невозможно сразу по нескольким причинам:
1) набор зависимостей в проекте меняется;
2) сами зависимости обновляются.

Изучение всего объёма получаемых в таком случае изменений неоправданно трудоёмко. Можно хотя бы ознакомиться с теми классами, которые используются в проекте, и читать changelog при поднятии версии, чтобы понять, не зацепило ли нас обновление.

Правда, такое частичное ознакомление не гарантирует, что зависимость используется правильно. Тут стоит погуглить и/или узнать мнение AI, чтобы опять же не скатиться в бесконечный ресёрч. Кругозор AI в этом вопросе сыграет нам на руку: могут быть предложены другие способы работы с зависимостью или альтернативные подходы в других зависимостях.

Изучить классические, прошедшие проверку временем решения по типу Caffeine -- хорошая идея. Долго разрабатываемый коммьюнити продукт часто имеет по крайней мере интересные идеи и подходы, а его распространённость позволит применить знания конкретной зависимости в очередном проекте.