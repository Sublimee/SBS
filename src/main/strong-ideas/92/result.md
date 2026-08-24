# Пример 1

Было:

```java
private void processTransactionsFromMapl(...) {
    try {
        var downloadLink = extractDownloadLink(registryLinks);
        var fileBytes = downloadMaplFile(downloadLink, token);
        ...
    } catch (NoSuchElementException e) {
        logger.warn("Received empty registry links");
    }
}

private MaplRegistryLink extractDownloadLink(
        List<MaplRegistryLink> registryLinks
) {
    if (registryLinks.isEmpty()) {
        throw new NoSuchElementException("Registry link was not found");
    }

    return registryLinks.getFirst();
}
```

Стало:

```java
private void processTransactionsFromMapl(...) {
    var downloadLink = extractDownloadLink(registryLinks);

    if (downloadLink.isEmpty()) {
        return;
    }

    var fileBytes = downloadMaplFile(downloadLink.get(), token);
    ...
}

private Optional<MaplRegistryLink> extractDownloadLink(
        List<MaplRegistryLink> registryLinks
) {
    if (registryLinks.isEmpty()) {
        logger.warn("Received empty registry links, expected 1");
        return Optional.empty();
    }

    if (registryLinks.size() > 1) {
        logger.warn(
                "Received {} registry links, expected 1; using first one",
                registryLinks.size()
        );
    }

    return Optional.of(registryLinks.getFirst());
}
```

# Пример 2

Было:

```kotlin
private suspend fun buildProgramWidgetOrNull(
    ...
) = runCancellableCatching {
    customerLoyaltyCategories
        .findByBasketOfferIdOrThrow(...)
        .takeIf {
            ...
        }
        ?.let { customerLoyaltyCategory ->
            val widgetSettingsV2 = commonProviderServiceV2.getExternalWidgetSettings(
                ...
            ).findByProgramIdAndBasketOfferIdOrThrow(
                ...
            )
            ...
        }
}.onFailure {
    logger.warn(it) { ... }
}.getOrNull()

fun List<CustomerLoyaltyCategory>.findByBasketOfferIdOrThrow(basketOfferId: Long): CustomerLoyaltyCategory =
    find { ... } ?: throw BusinessException.of(...)

fun List<WidgetSettingsV2>.findByProgramIdAndBasketOfferIdOrThrow(
    programId: Int, basketOfferId: Long, bonusAccountType: String
): WidgetSettingsV2 = find { ... } ?: throw BusinessException.of(...)
```

Стало:

```kotlin
private suspend fun buildProgramWidgetOrNull(
    ...
) = runCancellableCatching {
    customerLoyaltyCategories
        .findByBasketOfferIdOrNull(...)
        .also {
            if (it == null) {
                logger.warn { ... }
            }
        }
        ?.takeIf {
            ...
        }
        ?.let { customerLoyaltyCategory ->
            commonProviderServiceV2.getExternalWidgetSettings(
                ...
            ).findByProgramIdAndBasketOfferIdOrNull(
                ...
            ).also {
                if (it == null) {
                    logger.warn { ... }
                }
            }?.let { ...
        }
}.onFailure {
    logger.warn(it) { ... }
}.getOrNull()

fun List<CustomerLoyaltyCategory>.findByBasketOfferIdOrNull(
    basketOfferId: Long, 
): CustomerLoyaltyCategory? = ...

fun List<WidgetSettingsV2>.findByProgramIdAndBasketOfferIdOrNull(
    programId: Int, 
    basketOfferId: Long,
): WidgetSettingsV2? = ...
```

# Пример 3

Было:

```kotlin
...
    .mapNotNull { customerLoyalty ->
        widgetServices.findByProgramId(customerLoyalty.loyaltySource)
            .runCancellableCatching {
                getProgramWidget(...)
            }
            .onFailure {
                logger.warn(it) { "get widget programId=${customerLoyalty.loyaltySource} run failure!" }
            }
            .getOrNull()
    }
...

private fun List<WidgetServiceV2>.findByProgramId(programId: Int): WidgetServiceV2 =
    checkNotNull(find { it.getProgramId() == programId }) { ... }
```

Стало:

```kotlin
...
    .mapNotNull { customerLoyalty ->
        val widgetService = widgetServices.find {
            it.getProgramId() == customerLoyalty.loyaltySource
        } ?: run {
            logger.warn { ... }
            return@mapNotNull null
        }

        getProgramWidget(...)
    }
...
```

# Пример 4

Было:

```kotlin
...
ProgramsCashbackResponse(
    programs = idToBasket.map {
        val customerLoyaltyCategory = idToCustomer.findByBasketOfferIdOrThrow(it.key)
...    
)
```

Стало:

```kotlin
...

val missingCustomerLoyaltyCategoryIds = idToBasket.keys - idToCustomer.keys
if (missingCustomerLoyaltyCategoryIds.isNotEmpty()) {
    return@coroutineScope CustomerLoyaltyCategoriesMissing(missingCustomerLoyaltyCategoryIds)
}

Success(
    ProgramsCashbackResponse(
        programs = idToBasket.map { (basketOfferId, basket) ->
            val customerLoyaltyCategory = idToCustomer.getValue(basketOfferId)
...    
)
```

# Пример 5

Было:

```kotlin
private fun CategoriesConfirmationRequest.checkRequiredCategoriesAreContains(
    suggestedCategories: SuggestedCategories,
) = suggestedCategories.categories
    .filter { ... }
    .map { ... }
    .takeIf { categoriesIdsToConfirm.containsAll(it) }
    ?: throw BusinessException.of(LogicErrorCode.CATEGORIES_REQUIRED_CONFIRMATION_ERROR)
```

Стало:

```kotlin
private fun CategoriesConfirmationRequest.containsRequiredCategories(
    suggestedCategories: SuggestedCategories,
): Boolean {
    val requiredCategoryIds = suggestedCategories.categories
        .filter { it.isConfirmed() || it.isSelectedAndNotEditable() }
        .map { it.id }

    return categoriesIdsToConfirm.containsAll(requiredCategoryIds)
}

sealed interface CategoriesConfirmationResult {
    data object Success : CategoriesConfirmationResult
    data object RequiredCategoriesMissing : CategoriesConfirmationResult
    data object ConfirmationFailed : CategoriesConfirmationResult
}

@Service
class CategoricalCashbackConfirmationServiceV2( ...

    suspend fun confirmCategories(...)
    ): CategoriesConfirmationResult {
        ...
    
        if (!request.containsRequiredCategories(suggestedCategories)) {
            auditServiceV2.updateAuditOperationStatus(headers, auditOperationReference, VALIDATION_FAIL)
            return CategoriesConfirmationResult.RequiredCategoriesMissing
        }
    
        return runCatchingCancellable {
            ...
        }.fold(
            onSuccess = { CategoriesConfirmationResult.Success },
            onFailure = {
                logger.error(it) { "Categories confirmation failed" }
                auditServiceV2.updateAuditOperationStatus(headers, auditOperationReference, FAIL)
                CategoriesConfirmationResult.ConfirmationFailed
            }
        )
    }
    ...
}

@RestController
class CategoriesController(
    private val categoricalCashbackConfirmationServiceV2: CategoricalCashbackConfirmationServiceV2,
) : CategoriesControllerApi {

    override suspend fun confirmCategories(
        @MandatoryHeadersConstraint(userId = true) headers: Headers,
        categoriesConfirmationRequestDto: CategoriesConfirmationRequestDto,
    ) = withTraceContext(headers) {
        when (
            categoricalCashbackConfirmationServiceV2.confirmCategories(...)
        ) {
            Success -> Unit
            RequiredCategoriesMissing -> throw BusinessException.of(
                LogicErrorCode.CATEGORIES_REQUIRED_CONFIRMATION_ERROR
            )
            ConfirmationFailed -> throw BusinessException.of(
                LogicErrorCode.CATEGORIES_CONFIRMATION_ERROR
            )
        }
    }
}
```

# Вывод

Второй пример получился показательным. В buildProgramWidgetOrNull сразу два метода выкидывают исключения. При этом методы используются много где. Ну в целом "удобно": везде в "низкоуровневых" методах выбрасываем исключение, и если happy path не произошёл, то оптом ловим все исключения снаружи (один обработчик runCancellableCatching на всё). С одной стороны в таком случае удобно выстраиваются функциональные цепочки: не нужно думать о побочном эффекте в виде исключительных ситуаций, и тот самый happy path, действительно, считывается из кода просто. В то же время все отклонения от happy path теперь вообще не считываются из кода "верхнего уровня": всегда придется проваливаться внутрь методов.

В то же время я вижу, что в ряде случаев использования можно:
1) работать с более точными исключениями (в том числе message) + гораздо ближе к "выходам" из контроллеров, где изменение потока управления уже не так критично;
2) вообще отказаться от исключений.

Получился перекос: низкая стоимость написания кода против высокой стоимости его сопровождения.

В этом примере исключение вообще не нужно генерировать, так как результат его обработка -- сообщение уровня warn (показываем, что возникшая ситуация -- не ошибка) и возвращение наружу null.

Что получилось в результате внесённых изменений?
1) Низкоуровневые методы стали более переиспользуемыми, так как для всех случаев мы теперь не кидаем одно универсальное исключение, а их сигнатуру уточнилась за счет введения nullable возвращаемого значения.
2) Добавились специализированные под каждый вызов логи с уровнем WARN + бывший logger.warn(it) { ... } теперь не логирует наше псевдоисключение. 

Чтобы читать happy path, теперь нужно чуть больше усилий, но неявного поведения стало гораздо меньше.

Почему остался logger.warn(it) в конце исходного метода? Чтобы ловить исключения от вызовов клиентов для сторонних сервисов. По сравнению с предыдущими исключениями это не так больно, потому что обращение к сторонним сервисам идет единообразно: если получили ошибку, то сразу её логируем и прокидываем исключение выше.

Также, чтобы работать с исключениями дальше от "низкоуровневого" кода, можно пробовать работать с, например, Result из стандартной библиотеки или собственными его интерпретациями для более точного отражения состояний (начиная с примера 3). Само исключение можно даже в это состояние подложить чтобы не сопоставлять через when, как в примере. В чём может быть минус? Такая иерархия состояний должна возникать на уровне перед выходом из контроллера, иначе метод невозможно будет переиспользовать для других сценариев.