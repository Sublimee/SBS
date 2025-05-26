Мне было достаточно сложно выполнить это задание по одной причине -- кандидатов на применение описанного подхода достаточно сложно найти.

Почему?

У нас много кода, написанного в функциональном стиле. Код выглядит как цепочка вызовов методов:

```kotlin
fun getStatistics(
    aggregations: List<Aggregation>,
): List<Aggregation> = aggregations
        .groupBy { it.date }
        .map { toAggregation(it.value) }
        .sortedBy { it.date }
        .takeLast(STATISTICS_BY_MONTH_LIMIT)
```

Дефункционализировать в таком коде попросту нечего. В дополнение к этому такие цепочки в целях улучшения читаемости кода стараются делать компактными, обычно не скармливая в качестве аргументов блоки кода:

```kotlin
suspend fun getUnifiedBonusAccounts(headers: Headers): List<UnifiedBonusAccount> =
    bonusAccountProxy.getBonusAccounts(headers)
        .filter(supportedProgramWithAppropriateStatus())
        .filter { headers.hasRequiredFeatureTogglePredicate(it) }
        .map { enrichBonusAccount(headers, it) }
        .map { account: BonusAccount -> toUnifiedBonusAccount(headers, account) }
```

В таком коде SRP как будто отходит на второй план, если какой-то одной ответственности не уделено слишком много внимания (тогда ее выносят в отдельный метод). Но что если в одном объемлющем методе в вычислениях используется несколько цепочек?

```kotlin
suspend fun getActions(
    headers: Headers,
    actionsProperties: ActionsProperties,
    bonusAccount: UnifiedBonusAccount,
): Actions? = coroutineScope {
    val featuredLinkFeatures = actionsProperties.buttons
        .mapNotNull { config -> config.featuredLink?.featuresToCheck }
        .flatten()
        .toSet()

    val showConditionsFeatures = actionsProperties.buttons
        .map { config -> config.showConditions.featuresToShow }
        .flatten()
        .toSet()

    val checkedFeatures = featureToggleService.getFeatures(
        features = featuredLinkFeatures + showConditionsFeatures,
        headers = headers,
        includeTech = true
    )

    actionsProperties.buttons
        .filter { config ->
            config.showConditions.featuresToShow.isEmpty()
                    || checkedFeatures.containsAll(config.showConditions.featuresToShow)
        }
        .filter { conditionService.checkAll(headers, it.showConditions.conditionsForCheck) }
        .map { config: ButtonConfig ->
            async {
                builders[config.builder]?.let { btnBuilder ->
                    btnBuilder.buildButton(headers, config, bonusAccount)
                        ?.replaceDeeplinkIfNeeded(config, headers, checkedFeatures)
                }
            }
        }
        .awaitAll()
        .filterNotNull()
        .let {
            Actions(
                title = actionsProperties.title,
                buttonTitle = actionsProperties.buttonTitle,
                buttons = it
            )
        }
        .takeIf { it.buttons.isNotEmpty() }
}
```

Метод getActions достаточно большой, и в нем можно выделить две ответственности: 
1) подготовка фич;
2) формирование набора действий на основе ранее подготовленных фич.

Здесь в некотором роде локальным эквивалентом блоков кода / методов выступают переменные (val), так как они:
1) имеют имена (именуют блок вычислений);
2) вычисляются с помощью неразрывно записанной функциональной цепочки (т.е. оформлены явно).

Тем не менее мы можем выделить вычисление checkedFeatures, включающее промежуточные вычисления, в отдельный блок:

```kotlin
val checkedFeatures = run {
    val featuredLinkFeatures = actionsProperties.buttons
        .mapNotNull { config -> config.featuredLink?.featuresToCheck }
        .flatten()
        .toSet()

    val showConditionsFeatures = actionsProperties.buttons
        .map { config -> config.showConditions.featuresToShow }
        .flatten()
        .toSet()

    featureToggleService.getFeatures(
        features = featuredLinkFeatures + showConditionsFeatures,
        headers = headers,
        includeTech = true
    )
}
```

Вычисления до checkedFeatures включительно достаточно легко считываются, а вот actionsProperties.buttons и далее хотелось бы вынести в отдельный метод, чтобы разгрузить исходный.

Тот же код предварительных вычислений checkedFeatures в императивном стиле, однозначно, нуждается либо в кодовых блоках, либо в разбиении на методы:

```kotlin
val featuredLinkFeatures = mutableSetOf<String>()
for (button in actionsProperties.buttons) {
    val features = button.featuredLink?.featuresToCheck
    if (features != null) {
        featuredLinkFeatures.addAll(features)
    }
}

val showConditionsFeatures = mutableSetOf<String>()
for (button in actionsProperties.buttons) {
    showConditionsFeatures.addAll(button.showConditions.featuresToShow)
}

val allFeatures = mutableSetOf<String>()
allFeatures.addAll(featuredLinkFeatures)
allFeatures.addAll(showConditionsFeatures)
```

Вот еще пример:

```kotlin
override suspend fun buildButton(
    headers: Headers,
    buttonConfig: ButtonConfig,
    bonusAccount: UnifiedBonusAccount,
): Button? {
    val loyaltyTypeId = bonusAccount.account.typeId
    val operations = loyaltyOperationsProxy.getOperations(headers, loyaltyTypeId)
    if (operations.isEmpty()) {
        return null
    }

    val operationsCount = operations.count { it.writeoffAmount.value <= bonusAccount.balance.amount.value }
    val configWithValue = buttonConfig.copy(value = operationsCount.toString())
    return defaultActionButtonBuilder.buildButton(headers, configWithValue, bonusAccount)
}
```

Здесь опят же можно выделить две ответственности:
1) формирование конфигурации;
2) конструирование кнопки.

Вообще наличие return null (кнопки) в середине метода как бы намекает на то, что ответственности смешались. 

На ум приходит следующий вариант разбиения:

```kotlin
    override suspend fun buildButton(
    headers: Headers,
    buttonConfig: ButtonConfig,
    bonusAccount: UnifiedBonusAccount,
): Button? {
    val loyaltyTypeId = bonusAccount.account.typeId

    val configWithValue = loyaltyOperationsProxy.getOperations(headers, loyaltyTypeId)
        .takeIf { it.isNotEmpty() }
        ?.count { it.writeoffAmount.value <= bonusAccount.balance.amount.value }
        ?.let { count -> buttonConfig.copy(value = count.toString()) }

    return if (configWithValue!= null) {
        defaultActionButtonBuilder.buildButton(headers, configWithValue, bonusAccount)
    } else {
        null
    }
}
```

И если перейти к Kotlin-style:

```kotlin
override suspend fun buildButton(
    headers: Headers,
    buttonConfig: ButtonConfig,
    bonusAccount: UnifiedBonusAccount,
): Button? {
    val loyaltyTypeId = bonusAccount.account.typeId
    return loyaltyOperationsProxy.getOperations(headers, loyaltyTypeId)
        .takeIf { it.isNotEmpty() }
        ?.let { operations ->
            val operationsCount = operations.count { it.writeoffAmount.value <= bonusAccount.balance.amount.value }
            val configWithValue = buttonConfig.copy(value = operationsCount.toString())
            defaultActionButtonBuilder.buildButton(headers, configWithValue, bonusAccount)
        }
}
```

С помощью scope-функции let формирование кнопки выделено в отдельный блок. Однако нужно помнить, что вложенные let (которыми грешат увлекающиеся разработчики) значительно ухудшают читаемость.

Если бы в коде не встречались внезапные if'ы, то очень хорошо смотрятся такие выделенные блоки:


```kotlin
val configWithValue = run {
    val operationsCount = operations.count { it.writeoffAmount.value <= bonusAccount.balance.amount.value }
    buttonConfig.copy(value = operationsCount.toString())
}
```

Идея использования встраиваемого проектирования может встречаться в утильных классах / конвертерах, когда, пока они маленькие, проще не дробить, чтобы дополнительно не увеличивать когнитивную нагрузку на разработчика. То же по моему опыту относится и к классам с небольшим количеством (1-2) методов. Код таких классов обычно лучше поддерживается, если мы не допускаем его разрастания за счет boilerplate кода приватных методов.

Подобный подход с использованием комментариев для разделения независимых блоков кода можно встретить в тестах, как описано, например, здесь https://davidvlijmincx.com/posts/junit-given-when-then/. Предполагается, что такие комментарии помогут в считывании теста. Хотя, как по мне, они избыточны и не выполняют свою роль, только засоряя код. Чего, однако, нельзя сказать о given-when-then структурах в BDD-фреймворках для тестов, например Kotest.

Часто для логического разбиения блоков кода также используются две пустые строки. Это неформальная, но в то же время очень понятная и простая техника форматирования кода.

В статье упоминалось, что при использовании встраиваемого проектирования мы ясно видим, "какие локальные переменные будут "жить" во всём теле функции, а какие используются только локально внутри своих блоков кода." Я часто пользуюсь таким приемом при рефакторинге: исследуемый метод, разбитый на множество мелких методов, я собираю путем инлайнинга выделенных методов, после чего перекраиваю более ясным образом.