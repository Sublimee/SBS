## Пример 1-2

Повысим полиморфизм функции:

```kotlin
class CategoricalCashbackConfirmationService(
    ...
) {
    
    ...
    
    suspend fun confirmCategories(headers: Headers, idsToConfirm: List<Int>, offerDate: String) {
        val auditOperationReference: String =
            createAuditOperationAndValidateCategories(headers, idsToConfirm, offerDate)

        try {
            auditService.updateCategoriesConfirmationAuditOperationStatus(headers, auditOperationReference, PROGRESS)
            categoriesProviderService.confirmCategories(headers, idsToConfirm, offerDate)
            auditService.updateCategoriesConfirmationAuditOperationStatus(headers, auditOperationReference, SUCCESS)
        } catch (e: CancellationException) {
            throw e
        } catch (e: Exception) {
            logger.error(e) {
                "Categories confirmation failed for user with id ${headers.userId}"
            }
            auditService.updateCategoriesConfirmationAuditOperationStatus(headers, auditOperationReference, FAIL)
            throw BusinessException.of(LogicErrorCode.CATEGORIES_CONFIRMATION_ERROR)
        }
    }
    
    ...
}
```

что позволит работать с разными программами кэшбэка:

```kotlin
abstract class ConfirmationService(
    ...
) {
    abstract val program: Program

    suspend fun confirm(headers: Headers, confirmationRequest: ConfirmationRequest) {
        val auditOperation: AuditOperation = auditService.createAuditOperation(
            headers = headers,
            program = program,
            confirmationRequest = confirmationRequest,
        )

        checkRequirements(headers, confirmationRequest, auditOperation)

        try {
            updateAuditStatus(headers, auditOperation, OperationStatus.PROGRESS)
            performConfirmation(headers, confirmationRequest)
            updateAuditStatus(headers, auditOperation, OperationStatus.SUCCESS)
        } catch (e: Exception) {
            updateAuditStatus(headers, auditOperation, OperationStatus.FAIL)
            handleException(headers, e, auditOperation)
        }
    }

    abstract suspend fun checkRequirements(
        headers: Headers,
        confirmationRequest: ConfirmationRequest,
        auditOperation: AuditOperation,
    )

    abstract suspend fun performConfirmation(headers: Headers, confirmationRequest: ConfirmationRequest)

    abstract suspend fun handleException(headers: Headers, e: Exception, auditOperation: AuditOperation)

    protected suspend fun updateAuditStatus(headers: Headers, auditOperation: AuditOperation, status: OperationStatus) {
        auditService.updateAuditOperationStatus(
            headers = headers,
            program = program,
            auditOperation = auditOperation,
            status = status,
        )
    }
}
```

Что было сделано:

* перешли к более полиморфному неймингу: confirm вместо confirmCategories, createAuditOperation и checkRequirements вместо createAuditOperationAndValidateCategories и др.
* замена idsToConfirm: List<Int> и offerDate: String на confirmationRequest: ConfirmationRequest делают сигнатуру более устойчивой к изменениям и более обобщенной
* замена auditOperationReference: String на auditOperation: AuditOperation позволяет отстраниться от деталей работы с аудитом

Повышение полиморфизма одной функции тянет за собой необходимость внедрения полиморфизма в класс целиком.

## Пример 3

У нас есть множество подобных функций:

```kotlin
private fun isEmptyBalanceMotivationSupported(headers: Headers): Boolean {
    val userOs = headers.os
    val userAppVersion = headers.appVersion
    return headers.channelId == WEB_CHANNEL_ID
            || (headers.channelId == MOBILE_CHANNEL_ID && userOs != null && userAppVersion != null
            && userAppVersion >= unifiedLoyaltyProperties.emptyBalanceMotivationSupportedAppVersionsByOs[userOs])
}
```

которые на основе некоторого набора условий над заголовками определяют, есть ли поддержка определенной функциональности на стороне клиента.


Перейдем в этом методе к проверке поддерживаемости клиентом той или иной стратегии:

```kotlin
interface SupportStrategy {
    fun isSupported(headers: Headers): Boolean
}

class WebSupportStrategy : SupportStrategy {
    override fun isSupported(headers: Headers): Boolean = headers.channelId == WEB_CHANNEL_ID
}

class MobileSupportStrategy(
    private val supportedVersions: Map<OperationSystem, ApplicationVersion>
) : SupportStrategy {
    override fun isSupported(headers: Headers): Boolean {
        headers.os?.let { os ->
            headers.appVersion?.let { appVersion ->
                supportedVersions[os]?.let { minVersion ->
                    return appVersion >= minVersion
                }
            }
        }
        return false
    }
}

class EmptyBalanceMotivationService(
    ...
) {
    fun isFeatureSupported(headers: Headers, strategies: List<SupportStrategy>): Boolean {
        return strategies.any { strategy -> strategy.isSupported(headers) }
    }
}
```

Теперь это решение можно тиражировать за пределы одного класса.

## Пример 4

Важным моментом при проектировании REST API является недопущение появления таких низкополимормных типов результатов в ответах контроллеров:

```kotlin
@GetMapping("/programs")
suspend fun getPrograms(
    @MandatoryHeadersConstraint(userId = true) headers: Headers,
): List<Program> = ...
```

В случае, если потребуется видоизменить тип результата (например, на Map), то это повлечет цепочку измений типа List<Program> во всей цепочке до контроллера. Это произойдет и в полиморфном варианте (который опишу далее), но все же будет скрыто под капотом объемлющего типа, что потребует доработок в меньшем числе мест (меньше раскрываем реализацию). Также такая доработка повлечет нарушение обратной совместимости клиентов с нашим сервисом. Хорошим решением видится введение нового типа ProgramsResponse:


```kotlin
@GetMapping("/programs")
suspend fun getPrograms(
    @MandatoryHeadersConstraint(userId = true) headers: Headers,
): ProgramsResponse = ...

data class ProgramsResponse(
    val programs: List<Program>,
)
```

## Пример 5

Следующий интерфейс используется для того, чтобы для всех переданных периодов получить виджеты программ.

```kotlin
interface WidgetService {

    suspend fun getProgramWidgets(headers: Headers, periods: List<String>): List<ProgramWidget> = coroutineScope {
        periods
            .map { period ->
                async {
                    getProgramWidget(headers, period)
                }
            }
            .awaitAll()
    }

    suspend fun getProgramWidget(headers: Headers, period: String): ProgramWidget

    suspend fun getProgramId(): Int

    companion object {
        const val SUGGESTED_WIDGET_PROPERTIES_ID = 1
        const val CONFIRMED_WIDGET_PROPERTIES_ID = 2
    }
}
```
Что хочется сделать? Отделить бизнес-составляющую от технической, которые сейчас слеплены воедино. 
Повысим полиморфизм следующим образом:

```kotlin
interface ParallelizedService<N, T> {

    suspend fun getParallelized(requests: List<N>): List<T> = coroutineScope {
        requests
            .map { request ->
                async {
                    get(request)
                }
            }
            .awaitAll()
    }

    suspend fun get(request: N): T
}
```

У нас получился чисто технический метод получения некоторых результатов по исходному списку объектов. С помощью дженериков получили возможность распараллелить получение любых объектов, а не только виджетов программ.

## Вывод

В большинстве случаев очень простым и быстрым решением повышение полиморфизма некоторого кода является избавление от примитивных типов и параметризованных коллекций. Действительно, если спрятать конкретные детали внутрь объемлющего класса, то взаимодействие с его кишками в коде будет сконцентрировано только в местах непосредственного применения бизнес-логики (оболочка в виде класса скроет детали реализации в случае, когда данные используются для транспортировки к бизнес-логике). Таких примеров по коду мной было найдено очень много.

Более интересным является пример №5, отличающийся от предыдущих примеров более сильной идеей. Повышение полморфизма здесь привело к необходимости разделения большого интерфейса, содержащего техническую и бизнесовую составляющие на 2 независимых интерфейса. Техническая часть будучи отделенной от бизнесовой теперь может переиспользоваться в других частях программы и вполне может быть вынесена в библиотеку. Вероятно, не в каждом проекте может быть найден такой участок кода, требующий глубокого повшения полиморфизма, так как целью должно быть все-таки увеличение переиспользования такого метода.