# Пример 1

```kotlin
private suspend fun getAvailableCategoriesByOfferId(
    headers: Headers,
    loyalties: List<CustomerLoyalty>,
): Map<Long, SuggestedCategories> = fetchCategoriesByOfferId(
    loyalties = loyalties.filter { it.isCategoricalCashback() && it.isSuggested() },
) { loyalty ->
    loyaltyBackendApi
        .getCustomerAvailableCategories(headers, loyalty)
        .awaitSingle()
}

private suspend fun getReselectionCategoriesByOfferId(
    headers: Headers,
    loyalties: List<CustomerLoyalty>,
): Map<Long, SuggestedCategories> = fetchCategoriesByOfferId(
    loyalties = loyalties.filter { it.isCategoricalCashback() && it.isReconfirmed() },
) { loyalty ->
    loyaltyBackendApi
        .getReselectionAvailableCategories(headers, loyalty)
        .awaitSingle()
}

private suspend fun fetchCategoriesByOfferId(
    loyalties: List<CustomerLoyalty>,
    fetch: suspend (CustomerLoyalty) -> SuggestedCategories,
): Map<Long, SuggestedCategories> = supervisorScope { ...
```

# Пример 2

```kotlin
    suspend fun confirmCategories(
        headers: Headers,
        categoriesConfirmationRequest: CategoriesConfirmationRequest,
        suggestedCategories: SuggestedCategories,
    ): ConfirmCustomerOffersDrumResponse = confirmCategories(
        headers, categoriesConfirmationRequest, suggestedCategories, loyaltyBackendApi::addCustomerConfirmedCategories
    )

    suspend fun confirmReselectionCategories(
        headers: Headers,
        categoriesConfirmationRequest: CategoriesConfirmationRequest,
        suggestedCategories: SuggestedCategories,
    ): ConfirmCustomerOffersDrumResponse = confirmCategories(
        headers, categoriesConfirmationRequest, suggestedCategories, loyaltyBackendApi::confirmReselectionCategories
    )

    private suspend fun confirmCategories(
        headers: Headers,
        categoriesConfirmationRequest: CategoriesConfirmationRequest,
        suggestedCategories: SuggestedCategories,
        confirmHandler: (Headers, String, String, ConfirmCustomerCategoriesRequest) -> Mono<ConfirmCustomerOffersDrumResponse>,
    ): ConfirmCustomerOffersDrumResponse = runCatchingCancellable { ...
```

# Пример 3

```kotlin
inline fun <T, R> T.runCancellableCatching(block: T.() -> R): Result<R> {
    return try {
        Result.success(block())
    } catch (e: Throwable) {
        if (e is CancellationException) throw e
        Result.failure(e)
    }
}
```

# Пример 4

```kotlin
suspend fun getBonusAccounts(headers: Headers): List<BonusAccount> =
    customerInfoClient.getBonusAccountList(headers.userId, REQUEST_PARAM_INCLUDE_TOTAL_DEBIT_TRUE)
        .awaitSingle()
        .filter(if (clientCheckService.isThirdPartyClient(headers)) onlyKidsTypePredicate() else withoutKidsTypePredicate())
```

# Вывод

Рассматриваем ООП и ФП в частности через призму OCP. Удивительно, что в одной парадигме к нужно целенаправленно стремиться OCP (как и вообще к многим хорошим практикам в ООП), а в другой -- всё есть из коробки.

Все приведённые примеры демонстрируют, как принцип OCP поддерживается функциями высшего порядка. Примеры композиций (функциональных цепочек) здесь не привел, так как не нашел интересных примеров переиспользования одной цепочки в разных сценариях. Тем не менее сами по себе маленькие конвейерные функции являются идеальной предпосылкой для OCP. Почему? Во-первых, не нужно менять старые функции: каждая уже решает свою маленькую законченную задачу. Во-вторых, добавлять новые так же просто: между функциями нет зависимостей, каждая живет сама по себе. В-третьих, эти функции сами принимают функции высшего порядка, что дает им ту самую гибкость.

Если посмотреть на примеры 1 и 2, то видно, что идеи ФП и простота OCP должны и могут совмещаться с наследованием или применением (sealed) интерфейсов: видим, что в разных местах программы над некоторой "иерархией" сущностей (обычные Categories и ReselectionCategories) ожидается свое поведение.