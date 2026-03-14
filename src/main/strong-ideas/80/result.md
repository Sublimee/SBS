# Пример 1

Пример аналогичный тому, что было в статье:

```kotlin
val categories = userCategoriesRepresentation.filter {
    it.id < yandexCategoriesProperties.from || it.id > yandexCategoriesProperties.to
}
val yandexCategories = userCategoriesRepresentation.filter {
    it.id >= yandexCategoriesProperties.from && it.id <= yandexCategoriesProperties.to
}
```

Имеются два взаимоисключающих условия в соответствии с которыми категории попадают либо в один, либо в другой диапазон.

Повысим надежность за счет того, что укажем диапазон один раз:

```kotlin
fun List<UserCategoryRepresentation>.splitYandexCategories(): CategoriesSplit {
    val (yandexCategories, otherCategories) = partition { it.id in yandexCategoriesProperties.from .. yandexCategoriesProperties.to }
    return SplitCategories(
        yandexCategories = yandexCategories,
        otherCategories = otherCategories,
    )
}
```

Чтобы избежать путаницы в том, какой список за что отвечает, введем CategoriesSplit, где дадим им имена явно.

Таким образом рефакторинг позволил избежать сразу двух проблем, указанных в статье. 


# Пример 2

Еще один пример:

```kotlin
@CacheableAsync(
    cacheName = NOT_PAID_OUT_AGGREGATIONS,
    key = "{#headers.userId}"
)
suspend fun getNotPaidOutAggregations(
    headers: Headers,
): List<Aggregation> = runCatchingCancellable {
    getPayPeriodSumDto(headers = headers)
        .toAggregationList(filterNotPaidOut)
}.getOrElse { e: Throwable ->
    logger.error(e) { "Error occurred while fetching not paid out aggregations" }
    throw InternalException.builder()
        .errorCode(LogicErrorCode.UNABLE_TO_FETCH_BONUS_AGGREGATIONS)
        .cause(e)
        .build()
}

@CacheableAsync(
    cacheName = PAID_OUT_AGGREGATIONS,
    key = "{#headers.userId}"
)
suspend fun getPaidOutAggregations(
    headers: Headers,
): List<Aggregation> = runCatchingCancellable {
    getPayPeriodSumDto(headers = headers)
        .toAggregationList(filterPaidOut)
}.getOrElse { e: Throwable ->
    logger.error(e) { "Error occurred while fetching paid out aggregations" }
    throw InternalException.builder()
        .errorCode(LogicErrorCode.UNABLE_TO_FETCH_BONUS_AGGREGATIONS)
        .cause(e)
        .build()
}
```

2 разных метода ходят в один и тот же сервис бэкенда по взаимоисключающим условиям. Кажется, что раз уж мы используем 
одинаковые вызовы к бэкенду и навешиваем кэш над каждым из методов, то лучше сделать это универсально:

```kotlin
@CacheableAsync(
    cacheName = ALL_AGGREGATIONS,
    key = "{#headers.userId}"
)
suspend fun getAggregationsByPayStatus(
    headers: Headers,
): AggregationsByPayStatus = runCatchingCancellable {
    getPayPeriodSumDto(headers = headers).splitByPaidOut()
}.getOrElse { e ->
    logger.error(e) { "Error occurred while fetching aggregations" }
    throw InternalException.builder()
        .errorCode(LogicErrorCode.UNABLE_TO_FETCH_BONUS_AGGREGATIONS)
        .cause(e)
        .build()
}

private fun PayPeriodSumDto.splitByPaidOut(): AggregationsByPayStatus {
    val (paid, notPaid) = aggregations.partition { it.payStatus == PayStatus.PAID_OUT }

    return AggregationsByPayStatus(
        paidOut = paid.map { it.toAggregation() },
        notPaidOut = notPaid.map { it.toAggregation() },
    )
}
```

Убили сразу нескольких зайцев:
1) не пойдем лишний раз в бэкенд;
2) в ответах не просто списки, они именованы (paidOut и notPaidOut);
3) взаимоисключающие условия из двух мест схлопнулись в одно.

# Пример 3

У нас есть метод, который возвращает контент для переданных идентификаторов viewId виджетов:

```kotlin
@RestController
class SduiViewController(
    private val sduiViewService: SduiViewService,
) : SduiViewControllerApi {

    override suspend fun getContentByViewIds(
        @MandatoryHeadersConstraint(userId = true) headers: Headers,
        @RequestBody paramsByViewId: Map<String, Map<String, Any>?>,
    ): Map<String, Map<String, Any>> = withTraceContext(headers) {
        sduiViewService.getContent(headers, paramsByViewId)
    }
}
```

Контент будет возвращен по viewId, если:
1) наш сервис знает о переданном viewId;
2) в ходе формирования контента не произошло ошибок.

Иначе будет возвращено "пустое" значение по этому ключу viewId. Разделить 2 состояния выше в таком случае не представляется возможным. Лучше избавиться от неопределенности, добавив в ответ соответствующие поля со списками:
- unknown;
- error.

# Вывод

Еще раз обращаемся к идее, что нужно максимально избегать двусмысленности, недосказанности и вариативности (в плохом смысле) при разработке. Для этого лучше всего задавать себе вопрос: как этот метод / код может использоваться некорректно?

Для себя по результатам этого (и прошлых заданий) могу выделить следующие правила:

* не должно быть неявных зависимостей между двумя частями кода, чтобы изменение одной части кода требовало изменения другой части кода, но не отражалось на процессе компиляции (по мотивам примеров 1 и 2);
* взаимоисключающие или наоборот взаимосвязанные действия на уровне API нужно предоставлять таким образом, чтобы не было возможности вызвать их неправильно (примеры 1 и 2);
* нужно избегать сырых типов, создавая собственные обертки с полями, имеющими понятные имена (пример 3);
* в ответе нужно отдавать максимально полную информацию о результатх работы метода (примера 3).