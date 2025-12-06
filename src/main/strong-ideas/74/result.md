# Пример 1

BFF. Отдаем разный контент экрана/виджета: 

```kotlin
@Service
class SduiViewService(
    @Qualifier("viewIdToViewServiceMap") private val viewIdToViewServiceMap: Map<String, ViewService>,
    ...
) {

    suspend fun getContent(headers: Headers, viewId: String, requestParams: Map<String, Any>): Map<String, Any> {
        ...
        return mapOf(
            "contentLayout" to (viewIdToViewServiceMap[viewId]?.getContent(headers, requestParams) ?: emptyMap())
        )
    }
}
```

Имеем несколько реализаций ViewService:

```kotlin
interface ViewService {

    suspend fun getContent(headers: Headers, requestParams: Map<String, Any>? = null): Map<String, Any>

    fun getViewId(): String
}
```

Нужная реализация выбирается по соответствующему ему viewId. В результате имеем одну универсальную ручку контроллера, которая не зависит от реализаций:

```kotlin
override suspend fun getContentByViewId(
    @MandatoryHeadersConstraint(userId = true) headers: Headers,
    viewId: String,
    @RequestParam(required = false) requestParams: Map<String, Any>?,
): Map<String, Any> = withTraceContext(headers) {
    sduiViewService.getContent(headers, viewId, requestParams ?: emptyMap())
}
```

# Пример 2

В продолжение предыдущего примера. Дообогащение пришедших "сырых" параметров:

```kotlin
@Service
class RequestParamCollectorManager(
    private val requestParamCollectors: List<RequestParamCollector>
) {

    suspend fun getViewIdToResponse(
        headers: Headers, 
        viewIds: Set<String>
    ): MutableMap<String, Any> = coroutineScope {
        val viewIdToResponse = mutableMapOf<String, Any>()
        requestParamCollectors
            .filter { requestParamCollector ->
                requestParamCollector.getViewIds().any { it in viewIds }
            }
            .map { requestParamCollector ->
                async { requestParamCollector.enrich(headers, viewIdToResponse) }
            }
            .awaitAll()
        viewIdToResponse
    }
}
```

Единственное, конечно, от мутабельности в таком коде надо бы избавиться:

```kotlin
suspend fun getViewIdToResponse(
    headers: Headers,
    viewIds: Set<String>
): Map<String, Any> = coroutineScope {
    requestParamCollectors
        .filter { collector ->
            collector.getViewIds().any { it in viewIds }
        }
        .map { collector ->
            async { collector.enrich(headers) }
        }
        .awaitAll()
        .fold(emptyMap()) { acc, map -> acc + map }
}
```

# Пример 3

С целью унификации подходов при подтверждении программы кэшбэка используем разные реализации одного интерфейса AcceptService:

```kotlin
@Service
class InternalAcceptService(
    private val acceptServices: Map<CashbackType, AcceptService>,
) {

    suspend fun accept(headers: Headers, acceptRequest: AcceptRequest): ResultScreenInfo? =
        requireNotNull(acceptServices[acceptRequest.type]) {
            "Not found AcceptService implementation for type=${acceptRequest.type}"
        }
            .accept(headers, acceptRequest)
}
```

Динамическая диспетчеризация позволяет нам вызвать нужный для данной программы обработчик.

# Пример 4

По той же схеме среди разных реализаций выбираем подходящую:

```kotlin
@Service
class MotivationManager(
    private val sortedStrategies: List<MotivationStrategy>,
) {

    suspend fun getMotivation(
        motivationType: String,
        motivationContentList: List<MotivationContent>?,
        headers: Headers,
    ): Motivation? {
        val motivationContent = motivationContentList?.find { it.name == motivationType }
        val motivationStrategy = sortedStrategies.find { it.isSuitable(headers, motivationContent) }
        return motivationStrategy?.getMotivation(headers, motivationContent)
    }
}
```

# Пример 5

Аналогично. Есть разные виды виджетов, которые соответствуют разным программам:

```kotlin
interface WidgetService {

    fun getProgramId(): Int

    suspend fun getProgramWidget(
        headers: Headers,
        customerLoyalty: CustomerLoyalty,
        bonusAccountType: String,
    ): ProgramWidget
}
```

В каждую реализацию зашит идентификатор программы. По этому идентификатору можно понять, что из всех реализаций выбрана нужная.

# Вывод

Нужно ли в Spring (как впрочем и где бы то ни было еще) всегда использовать абстракции вместо конкретных реализаций? Я не ввожу интерфейсы до тех пор, пока не появятся две реализации. Почему? Добавить интерфейс средствами IDE постфактум очень просто, а второй реализации может никогда и не появиться. Зачем добавлять лишний слой абстракции, если у интерфейса одна реализация? Кажется, что это избыточно.

Несколько лет назад на одном из ревью кода коллеги я оставил комментарий. Смысл его был в моем непонимании, почему для некоторых сервисов добавлялись интерфейсы, а для некоторых -- нет, хотя везде было по одной реализации. Увиденный мной случай был апогеем неправильного использования DIP: читающему код вообще непонятно, нужно ли расценивать наличие интерфейса как значимый для понимания элемент.

Внятного ответа я тогда не получил. Кажется, что сервис можно было вообще освободить от интерфейсов без потери качества его дальнейшего сопровождения.

Удачные примеры DIP совместно с динамической диспетчеризацией выше позволяют разграничить разные реализации, не завязываясь на конкретные их детали. Нужные реализации становится просто добавлять и удалять.