## Пример 1

Было:

```kotlin
fun List<Program>.sortByDateDescThenById(): List<Program> =
    this.sortedWith(compareByDescending<Program> { it.date }.thenBy { it.id })
```

Метод применяется к списку программ для их сортировки сначала по дате, а затем по идентификатору в рамках одной даты.
Проанализируем выходные данные в качестве подготовки к реализации по ко-рекурсивной схеме:

1. Когда выход будет пуст? Когда вход пуст.
2. Если выход не пуст, то какова его голова? Значение с максимальной датой и в то же время с минимальным значением идентификатора программы из входного списка.
3. Из каких данных рекурсивно строится хвост выхода? Входной список без значения, найденного на предыдущем шаге.

Шаблон:

```
если список пуст, то выдаём [ ] иначе
sortByDateDescThenById x = let a = maxByDateThenMinById x in a : sortByDateDescThenById(x \\ [a])
```

Стало:

```kotlin
tailrec fun sortByDateDescThenById(
    programs: List<Program>,
    sortedPrograms: List<Program> = emptyList(),
): List<Program> {
    return if (programs.isEmpty()) {
        sortedPrograms
    } else {
        val minElement = 
            programs.minWithOrNull(compareByDescending<Program> { it.date.toDate() }.thenBy { it.id })!!
        sortByDateDescThenById(
            programs - minElement,
            sortedPrograms + minElement,
        )
    }
}
```

На каждом шаге получаем отсортированный по заданным правилам список.

## Пример 2

Было:

```kotlin
private fun List<Aggregation>.fillGaps(): List<Aggregation> {
    val size = this.size
    val missingAggregations: MutableList<Aggregation> = ArrayList()
    if (size > 1) {
        var date = this[0].date
        var index = 1
        while (index < size) {
            if (ChronoUnit.MONTHS.between(
                    YearMonth.from(date), YearMonth.from(
                        this[index].date
                    )
                ) >= 2
            ) {
                val missingMaplAggregation = AggregationUtils.toZeroAccruedAggregation(date.plusMonths(1))
                missingAggregations.add(missingMaplAggregation)
                date = missingMaplAggregation.date
            } else {
                date = this[index].date
                index++
            }
        }
    }
    return (this + missingAggregations).sortedBy { it.date }
}
```

Метод заполняет пробелы в отсортированном списке начислений.

Проанализируем выходные данные в качестве подготовки к реализации по ко-рекурсивной схеме:

1. Когда выход будет пуст? Когда пуст вход необработанных элементов.
2. Если выход не пуст, то какова его голова? Элемент входного списка или сгенерированный нами для этого списка элемент, закрывающий пробел.
3. Из каких данных рекурсивно строится хвост выхода? Оставшиеся элементы списка без значения, взятого на предыдущем шаге.

Шаблон:

```
если список пуст, то выдаём [ ] иначе
fillGaps x y = 
                let a = findMissingAggregation(x, y)
                fillGaps(x \\ [a], a : y)
```

Стало:

```kotlin
fun List<Aggregation>.fillGaps(acc: List<Aggregation> = emptyList()): List<Aggregation> {
    return when {
        this.isEmpty() -> acc
        acc.isNotEmpty() && ChronoUnit.MONTHS.between(
            YearMonth.from(acc.last().date),
            YearMonth.from(this.first().date)
        ) >= 2 -> {
            val nextDate = acc.last().date.plusMonths(1)
            val missingAggregation = AggregationUtils.toZeroAccruedAggregation(nextDate)
            this.fillGaps(acc + missingAggregation)
        }

        else -> this.drop(1).fillGaps(acc + this.first())
    }
}
```

Получаем на каждом шаге отсортированный список начислений без промежутков.

## Пример 3

Было:

```kotlin
fun List<Aggregation>.aggregateByDate(): List<Aggregation> {
    return this
        .groupBy { it.date }
        .map { (date, aggregations) ->
            Aggregation(
                date = date,
                amount = aggregations.sumOf { it.amount }
            )
        }
        .sortedBy { it.date }
}
```

Метод агрегирует начисления в неотсортированном списке по возрастанию даты.

Проанализируем выходные данные в качестве подготовки к реализации по ко-рекурсивной схеме:

1. Когда выход будет пуст? Когда пуст вход.
2. Если выход не пуст, то какова его голова? Элемент с наименьшей датой и суммой всех начислений с той же датой.
3. Из каких данных рекурсивно строится хвост выхода? Оставшиеся элементы списка без значений, взятых на предыдущем шаге.

Шаблон:

```
если список пуст, то выдаём [ ] иначе
aggregateByDate x y = 
                        let a = getCurrentAggregations(x, y) 
                        aggregateByDate(x \\ [a], a : y)
```

Стало:

```kotlin
    fun List<Aggregation>.aggregateByDate(
    acc: List<Aggregation>,
): List<Aggregation> {
    if (this.isEmpty()) return acc

    val currentDate = this.first().date
    val (currentAggregations, rest) = this.partition { it.date == currentDate }

    return rest.aggregateByDate(acc + Aggregation(
            date = date,
            amount = currentAggregations.sumOf { it.amount.value }),
    )
}
```

Получаем на каждом шаге отсортированный список агрегированных начислений.

# Вывод

Посмотрим на получившиеся методы в ко-рекурсивном стиле, где программа следует за выходными данными. 

Что имеем в примерах 1 и 3? Соперничать с декларативным подходом, если метод можно записать целиком в функциональном стиле на основе входных данных достаточно сложно. Абсолютно точно обратиться к структуре выходных данных нужно, когда простое решение на основе входных данных не материализовалось в голове само собой.

Наибольшую выгоду мы смогли извлечь во втором примере. Почему? Придерживаясь схемы получения на каждом шаге последовательности по заданному контракту для выходных данных (отсутствие промежутков и сортировка) мы решили сразу две задачи:

1) ясно перевели требования в код программы (повысили читаемость), так как был понятен каждый очередной шаг
2) на выходе имеем сразу отсортированный список (выигрыш в производительности)

Метод изначально был написан плохо по той причине, что входная последовательность не отвечает на вопрос, как должен быть реализован алгоритм. 

Все три примера имели на выходе коллекцию. Насколько применим ко-рекурсивный формат к единичным экземплярам, у которых меняется состояние нескольких полей объекта. Мне показалось, что для написанных в классическом стиле методов, реализацию которых я уже знал, это сделать было практически нереально, так как мозг просто раскручивал клубок от выхода до входа по той же классической схеме просто восстанавливая из памяти последовательность действий. Однако если раскручивание алгоритма может быть вполне успешным, как это было в примере 2.

Также я попробовал написать в ко-рекурсивном стиле алгоритм, который выдаст все перестановки переданных элементов (до того, как прочитал о том же примере в оригинале статьи), и не смог сделать это хоть сколь-нибудь адекватно, оставив в итоге исходную рекурсивную реализацию.

В любом случае, если в арсенале есть два инструмента, каждый из которых может иметь преимущества в своих ситуациях, то стоит пользоваться обоими инструментами. 