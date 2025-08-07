# Пример 1

```java
private List<Integer> getQuarterList(int index) {
    var result = new ArrayList<Integer>();
    for (int i = 1; i <= index; i++) result.add(i);
    return result;
}
```

```java
private List<Integer> getQuarterList(int index) {
    return IntStream.rangeClosed(1, index)
                    .boxed()
                    .collect(Collectors.toList());
}
```

# Пример 2

```java
public synchronized int hashCode() {
    if (__hashCodeCalc) {
        return 0;
    }
    __hashCodeCalc = true;
    int _hashCode = 1;
    if (getRequestStatus() != null) {
        for (int i=0;
             i<java.lang.reflect.Array.getLength(getRequestStatus());
             i++) {
            java.lang.Object obj = java.lang.reflect.Array.get(getRequestStatus(), i);
            if (obj != null &&
                !obj.getClass().isArray()) {
                _hashCode += obj.hashCode();
            }
        }
    }
    if (getFolder() != null) {
        for (int i=0;
             i<java.lang.reflect.Array.getLength(getFolder());
             i++) {
            java.lang.Object obj = java.lang.reflect.Array.get(getFolder(), i);
            if (obj != null &&
                !obj.getClass().isArray()) {
                _hashCode += obj.hashCode();
            }
        }
    }
    __hashCodeCalc = false;
    return _hashCode;
}
```

```java
@Override
public synchronized int hashCode() {
    if (__hashCodeCalc) {
        return 0;
    }
    __hashCodeCalc = true;
    try {
        return Stream.of(getRequestStatus(), getFolder())
                .filter(Objects::nonNull)
                .flatMap(array -> Arrays.stream((Object[]) array))
                .filter(Objects::nonNull)
                .filter(obj -> !obj.getClass().isArray())
                .mapToInt(Object::hashCode)
                .reduce(1, Integer::sum);
    } finally {
        __hashCodeCalc = false;
    }
}
```

# Пример 3

```java
public ArrayList<Document> basicDBObjectAppend(String userName, String email) {
    BasicDBObject query = new BasicDBObject();
    query.append("$where", "this.sharedWith == \"CONSTANT\" && this.email == \"CONSTANT\"");

    MongoCursor<Document> cursor = collection.find(query).iterator();

    ArrayList<Document> results = new ArrayList<>();
    while (cursor.hasNext()) {
        Document doc = cursor.next();
        results.add(doc);
    }

    return results;
}
```

```java
public List<Document> basicDBObjectAppend(String userName, String email) {
    BasicDBObject query = new BasicDBObject();
    query.append("$where", "this.sharedWith == \"CONSTANT\" && this.email == \"CONSTANT\"");

    try (MongoCursor<Document> cursor = collection.find(query).iterator()) {
        return StreamSupport.stream(Spliterators.spliteratorUnknownSize(cursor, Spliterator.ORDERED), false)
                            .collect(Collectors.toList());
    }
}
```

# Пример 4

```java
public void compute_pz() {
    double sum = 0.0;
    for (int i = 0; i < numTopics; i++) {
        sum += sumTopicWordCount[i];
    }
    for (int i = 0; i < numTopics; i++) {
        pz[i] = 1.0 * (sumTopicWordCount[i] + alpha) / (sum + alphaSum);
    }
}
```

```java
public void compute_pz() {
    double sum = DoubleStream.of(sumTopicWordCount).sum();

    pz = IntStream.range(0, numTopics)
                  .mapToDouble(i -> (sumTopicWordCount[i] + alpha) / (sum + alphaSum))
                  .toArray();
}
```

# Пример 5

```java
public void compute_phi() {
    for (int i = 0; i < numTopics; i++) {
        double sum = 0.0;
        for (int j = 0; j < vocabularySize; j++) {
            sum += topicWordCount[i][j];
        }
        for (int j = 0; j < vocabularySize; j++) {
            phi[i][j] = (topicWordCount[i][j] + beta) / (sum + betaSum);
        }
    }
}
```

```java
public void compute_phi() {
    IntStream.range(0, numTopics).forEach(i -> {
        double sum = IntStream.range(0, vocabularySize)
                              .mapToDouble(j -> topicWordCount[i][j])
                              .sum();
        
        IntStream.range(0, vocabularySize)
                 .forEach(j -> phi[i][j] = (topicWordCount[i][j] + beta) / (sum + betaSum));
    });
}
```

# Вывод

Во-первых, циклы в Java и Kotlin сейчас найти достаточно сложно. Все-таки влияние функциональной парадигмы дает о себе знать. Пришлось посмотреть под сотню репозиториев, чтобы найти примеры выше. Из того, что удалось найти, Пример 2 наиболее остро нуждался в отказе от циклов. В результате, действительно улучшилась читаемость. 

Я нашел много примеров с циклами, которые были просты для чтения и не нуждались в рефакторинге.

Тем не менее в одном из репозиториев нашел следующие методы:

```java
/**
 * Метод изменяет дефолтные названия случайных колонок отчёта
 * @param countForRenaming количество колонок, которым нужно изменить название
 */
private void renameColumns(int countForRenaming) {
    if (countForRenaming != 0) {
        List<Integer> columnOrders = userReportSettings.getUserReportColumns().stream()
                .map(ReportColumn::getOrder)
                .collect(toList());
        for (int i = 0; i < countForRenaming; i++) {
            int columnIdx = getRandomOrder(columnOrders);
            String userTitle = AfinFaker.randomAlphanumeric(columnIdx);
            userReportSettings.getUserReportColumns().get(columnIdx - 1).setUserTitle(userTitle);
        }
    }
}

/**
 * Метод меняет местами пару случайных колонки отчёта
 *
 * @param countForReplacing количество пар колонок, которым нужно изменить порядок
 */
private void replaceColumns(int countForReplacing) {
    if (countForReplacing != 0) {
        List<SwapPair> swapPairs = new ArrayList<>();
        for (int i = 0; i < countForReplacing; i++) {
            List<Integer> columnOrders = userReportSettings.getUserReportColumns().stream()
                    .map(ReportColumn::getOrder)
                    .collect(toList());
            int firstColumnOrder = getRandomOrder(columnOrders);
            int secondColumnOrder = getRandomOrder(columnOrders);
            swapPairs.add(createSwapPair(firstColumnOrder, secondColumnOrder));
        }
        // установка корректных значений columnOrder, после создания пар для перемещений
        int order = 1;
        for (ReportColumn userSetting : userReportSettings.getUserReportColumns()) {
            userSetting.setOrder(order++);
        }
        userReportSettings.getSwappedColumns().addAll(swapPairs);
    }
}
```

Кажется, что они оба написаны некорректно по причине того, что никак не учитывают предысторию генерации случайных чисел, так как могут быть сгенерированы не уникальные значения. Закроем глаза и на то, что они работают с изменяемыми переменными.

В обоих случаях нужно было бы взять первые N (или 2*N для replaceColumns) элементов из списка неповторяющихся индексов:

```java
List<Integer> indices = IntStream.range(0, columns.size())
    .boxed()
    .collect(Collectors.toList());

Collections.shuffle(indices);
```

В дальнейшем прохождение по этим элементам вполне можно делать и в цикле без потери читаемости:     

```java
int actualCount = Math.min(countForRenaming, columns.size());
for (int i = 0; i < actualCount; i++) { ...
```

Я бы не стал ультимативно демонизировать циклы, но всегда бы рассмотрел возможность, как можно было бы обойтись без них, например силами Stream API. Тем не менее, когда речь заходит про обращение к индексам, алгоритм с for обычно считывается очень хорошо.

Для последних двух методов я думал насчет применения каких-то подходов не в лоб, по аналогии с тем, что показал Sean Parent. Ничего стоящего на ум не пришло. Даже если бы пришло, то скорее всего нужно было реализовать аналог функции из STL в Java. Такой аналог нигде бы больше не использовался, кроме как для этого локального рефакторинга (разве кто-то будет выносить это в библиотеку?). Это очень сильно снижает ценность решения, так как STL протестировали вдоль и поперек, а наш алгоритм нужно будет отлаживать и тестировать самостоятельно. Поэтому в большинстве случае максимум, чем мы довольствуемся, это не такой бедный, но все же достаточно ограниченный, но в то же время надежный Stream API.