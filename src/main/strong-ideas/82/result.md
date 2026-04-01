# Пример 1

```kotlin
private fun toUnifiedBonusAccount(headers: Headers, account: BonusAccount): UnifiedBonusAccount {
    val loyaltyProgram = unifiedLoyaltyProperties.loyaltyProgramTypes[account.loyaltyType]!!
    val unifiedBonusAccount = UnifiedBonusAccount(
        account = account.toLoyaltyAccount(currencyIcon = loyaltyProgram.currencyIcon),
        balance = getExtendedAmountDto(account, loyaltyProgram),
        title = loyaltyProgram.carouselTitle,
        debit = if (account.totalDebit == null) account.debit else account.totalDebit,
    )

    return if (headers.channelId == WEB_CHANNEL_ID) {
        unifiedBonusAccount.copy(
            faqContent = loyaltyProgram.faqContent,
            faq = loyaltyProgram.faqContent.faq, // TODO убрать после раскатки AO
        )
    } else {
        unifiedBonusAccount.copy(
            faq = loyaltyProgram.faqContent.faq,
        )
    }
}
```

**-- Могу ли я чётко сформулировать, никуда больше не перескакивая, что этот код делает?**

Да. Этот код конвертирует бонусные счета, полученные с бэкенда (BonusAccount), к виду, который отдаем в REST API.

Здесь есть исходная проблема проектирования, когда одновременно используются понятия Bonus и Loyalty. Я это помню), но
терминологию нужно унифицировать, чтобы не вводить в заблуждение читающего код.

**-- Похоже ли это всё на то, что действительно должно занимать "10 строк и 2 условия"?**

В коде есть временный костыль для сохранения обратной совместимости на время раскатки новой версии сервиса. Такое 
разветвление логики встречается в методах для разных платформах. Была идея хранить все разночтения для каждой платформы
в одном месте в коде, но она так и осталась нереализованной из-за большого количества сценариев, на которые влияет
текущая платформа.


# Пример 2

```kotlin
private fun getActionButton(
    headers: Headers,
    loyaltyProgram: LoyaltyProgram,
): SpendButton {
    val button = loyaltyProgram.getSpendButtonByOs(headers)
    // замена необходима в связи с обращением к неправильному полю на IOS
    button.clickLink = if (OperationSystem.IOS == headers.os) {
        button.appLink
    } else {
        button.clickLink
    }
    return button
}
```

**-- Могу ли я чётко сформулировать, никуда больше не перескакивая, что этот код делает?**

Да, частично. Этот код выбирает контент для кнопки действия на экране с балансом бонусного счета. Здесь есть опять же 
смешение двух семантик: Spend и Action. Сейчас из кода непонятно, почему они используются обе.

**-- Похоже ли это всё на то, что действительно должно занимать "10 строк и 2 условия"?**

Исходно для того, чтобы отдавать в ответе ссылки для разных платформ, было введено несколько полей: deepLink, appLink,
clickLink. Это вносит путаницу из-за того, что нужно формировать все три ссылки на каждый ответ даже для тех платформ, 
для которых не предназначен ответ. Эту логику можно было бы разнести по разным интерфейсам, но сейчас мы видим if.


# Пример 3

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
    return this + missingAggregations
}
```

**-- Могу ли я чётко сформулировать, никуда больше не перескакивая, что этот код делает?**

Да, метод заполняет информацию о начисляниях за каждый месяц в цепочке. В цепочке могут отсутствовать начисления по 
некоторым промежуточным месяцам, их нужно отразить в цепочке с нулевым балансом. 

**-- Похоже ли это всё на то, что действительно должно занимать "10 строк и 2 условия"?**

Логика в целом считывается не так сложно, но вариант с рекурсией выглядит более выразительно:

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

# Пример 4

```kotlin
suspend fun toBonuses(
    accounts: List<InternalBonusAccount>,
    headers: Headers,
    version: Int
): List<Bonus> {
    val actualFeatureToggle = featuresProperties.osSpecificUnifiedFeatures[headers.os]
    val isUnifiedLoyaltyWidgetNeeded = actualFeatureToggle != null && accounts.any {
        unifiedLoyaltyProperties.loyaltyProgramTypes.containsKey(it.account.typeId)
                && featureToggleService.hasFeatureIncludeTech(actualFeatureToggle, headers)
    }

    val bonuses = accounts
        .mapNotNull { toBonus(headers, version, isUnifiedLoyaltyWidgetNeeded, it) }
    if (isUnifiedLoyaltyWidgetNeeded) {
        return bonuses + getUnifiedBonus(headers)
    }
    return bonuses
}
```

**-- Могу ли я чётко сформулировать, никуда больше не перескакивая, что этот код делает?**

Да, этот код возвращает контент для виджетов под определенную платформу. Опять же видим несовпадение в имени метода 
toBonuses и Widget.

**-- Похоже ли это всё на то, что действительно должно занимать "10 строк и 2 условия"?**

Думал, как избавиться от краевого случая с getUnifiedBonus(headers), но isUnifiedLoyaltyWidgetNeeded вплетается как в
получение каждого виджета из accounts, так и в получение самого Unified-виджета.

# Пример 5

```kotlin
fun getContract(account: InternalBonusAccount, version: Int): Contract? {
    var result: Contract? = null
    if (version == 1 && isCashBack(account)) {
        result =cashback
    } else if (version == 2 && isCashBackV2(account)) {
        result = cashbackV2
    } else if (isTravel(account)) {
        if (version == 1) {
            result = travel
        } else if (version == 2) {
            result = travelV2
        }
    }
    return result ?: contractMap[ContractId(version, account.account.typeId)]
}
```

**-- Могу ли я чётко сформулировать, никуда больше не перескакивая, что этот код делает?**

Нет, пришлось переходить внутрь Contract, чтобы понять, что речь идет о контракте (варианте наполнения) виджета. Для 
лучшей читаемости лучше было бы добавить везде префикс/суффикс/постфикс Widget.

**-- Похоже ли это всё на то, что действительно должно занимать "10 строк и 2 условия"?**

Нужно переписать работу с условиями в более простом виде:

```kotlin
fun getWidgetContract(account: InternalBonusAccount, version: Int): WidgetContract? =
    when {
        version == 1 && isCashBack(account) -> cashback
        version == 2 && isCashBackV2(account) -> cashbackV2

        isTravel(account) -> when (version) {
            1 -> travel
            2 -> travelV2
            else -> null
        }

        else -> widgetContractMap[WidgetContractId(version, account.account.typeId)]
    }
```