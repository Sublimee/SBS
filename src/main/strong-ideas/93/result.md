# Пример 1

Было:

```kotlin
private fun extractValueWithSymbol(shortTitle: String): String? {
    val match = VALUE_REGEX.find(shortTitle) ?: return null

    val prefix = match.groups[REGEX_PREFIX_NAME]?.value ?: throw InternalException.of(QUEST_VALUE_PARSE_ERROR)
    val number = match.groups[REGEX_NUMBER_NAME]?.value ?: throw InternalException.of(QUEST_VALUE_PARSE_ERROR)
    val rawSpace = match.groups[REGEX_SPACE_NAME]?.value ?: throw InternalException.of(QUEST_VALUE_PARSE_ERROR)
    val rawSeparator = match.groups[REGEX_SEPARATOR_NAME]?.value ?: throw InternalException.of(QUEST_VALUE_PARSE_ERROR)
    
    // форматирование ответа
    ...

    return ...
}
```

Стало:

```kotlin
private fun extractValueWithSymbol(shortTitle: String): String? = QuestValue.from(shortTitle)?.format()

private class QuestValue private constructor(
    private val prefix: String,
    private val number: String,
    private val space: String,
    private val separator: String,
) {

    // форматирование ответа
    fun format(): String {
        ...
    }

    companion object {
        fun from(shortTitle: String): QuestValue? {
            val match = VALUE_REGEX.find(shortTitle) ?: return null

            return QuestValue(
                prefix = match.group(REGEX_PREFIX_NAME) ?: return null,
                number = match.group(REGEX_NUMBER_NAME) ?: return null,
                space = match.group(REGEX_SPACE_NAME) ?: return null,
                separator = match.group(REGEX_SEPARATOR_NAME) ?: return null,
            )
        }

        private fun MatchResult.group(name: String): String? = groups[name]?.value
    }
}
```

# Пример 2

Было:

```kotlin
data class PackageInfo(
    ...
    val conditions: List<Condition>,
    ...
) {
    @JsonIgnore
    fun getConditionWithMaxProgressValue(): Condition? = conditions.maxByOrNull { it.progress }!!
}
```

```kotlin
suspend fun getConditions(...): List<Condition> {
    return ...
}
```

Стало:

```kotlin
// https://quickbirdstudios.com/blog/non-empty-lists-kotlin/
data class NonEmptyList<out T>(
    val head: T,
    val tail: List<T>,
) {
    ...
}
```

```kotlin
fun <T> List<T>.toNonEmptyListOrNull(): NonEmptyList<T>? =
    if (isEmpty()) null else NonEmptyList(head = first(), tail = drop(1))
```

```kotlin
data class PackageInfo(
    ...
    val conditions: NonEmptyList<Condition>,
    ...
) {
    @JsonIgnore
    fun getConditionWithMaxProgressValue(): Condition = conditions.maxBy { it.progress }
}
```

```kotlin
suspend fun getConditions(...): NonEmptyList<Condition> {
    ...
    return conditions.toNonEmptyListOrNull() ?: throw BusinessException.of(ErrorCode.PACKAGE_CONDITIONS_EMPTY_ERROR)
}
```

# Пример 3

Было:

```kotlin
data class CashbackAccrualsRequestDto(
    val accountType: Int,
    val groupIds: List<Int>,
    val month: LocalDate? = null,
    val subGroupId: Long? = null,
    val limit: Int? = null,
    val pointer: String? = null,
)
```

```kotlin
// groupIds содержит > 1 значения только для пар 4,5 и 4,6. В этих парах значения
// трактуются одинаково и нужны только для обратной совместимости на бэк-системе
loyaltyAccrualHistoryService.getGroupContentById(headers, request.groupIds.first())
```

Стало:

```kotlin
data class CashbackAccrualsRequestDto(
    val accountType: Int,
    val groupIds: NonEmptyList<Int>,
    val month: LocalDate? = null,
    val subGroupId: Long? = null,
    val limit: Int? = null,
    val pointer: String? = null,
) {

    /**
     * groupIds содержит > 1 значения только для пар 4,5 и 4,6. В этих парах значения
     * трактуются одинаково и нужны только для обратной совместимости на бэк-системе;
     * если нужен единственный идентификатор группы, то берём первый.
     */
    val primaryGroupId: Int get() = groupIds.head
    
    ...
}
```

# Пример 4

Было:

```kotlin
@Validated
@ConfigurationProperties("cashback-v2")
data class CashbackPropertiesV2(
    val accrualsDeeplinkByPlatformFromGroups: Map<String, String> = emptyMap(),
    ...
) {

    fun getAccrualsDeeplink(headers: Headers): String {
        val platform = headers.platform.toString()
        return accrualsDeeplinkByPlatformFromGroups[platform] ?: accrualsDeeplinkByPlatformFromGroups[DEFAULT]!!
    }

    ...
```

Стало:

```yaml
accruals-deepLink-by-platform-from-groups:
  default: '...'
  by-platform:
    WEB_DESKTOP: '...'
```

```kotlin
data class DeeplinkByPlatform(
    val default: String,
    val byPlatform: Map<String, String> = emptyMap(),
) {

    fun forPlatform(platform: String): String = byPlatform[platform] ?: default
}
```

# Пример 5

Было:

```kotlin
fun buildCategoryInfo(
    headers: Headers,
    segment: SegmentDto?,
    content: ContentDto,
    category: CashbackCategoryDto,
    subContent: SubContentDto?,
): CashbackCategoryInfoDto? {
    if (segment?.hint.isNullOrBlank() && content.description.isNullOrBlank()) return null
    if (segment?.buttonText.isNullOrBlank() && subContent?.title.isNullOrBlank()) return null

    return CashbackCategoryInfoDto(
        iconUrl = content.iconName,
        title = categoryTitle(content.name, category.percentRate),
        text = content.description ?: segment?.hint!!,
        infoDeeplink = categoryDeeplink(headers, segment?.deeplink ?: subContent?.deeplink),
        buttonText = segment?.buttonText ?: subContent?.title!!,
    )
}
```

Стало:

```kotlin
value class NonBlankString private constructor(val value: String) {

    override fun toString(): String = value

    companion object {
        fun of(value: String?): NonBlankString? =
            if (value.isNullOrBlank()) null else NonBlankString(value)
    }
}

fun String?.toNonBlankOrNull(): NonBlankString? = NonBlankString.of(this)
```

```kotlin
    fun buildCategoryInfo(
        headers: Headers,
        segment: SegmentDto?,
        content: ContentDto,
        category: CashbackCategoryDto,
        subContent: SubContentDto?,
    ): CashbackCategoryInfoDto? {
        val text = content.description.toNonBlankOrNull()
            ?: segment?.hint.toNonBlankOrNull()
            ?: return null
        val buttonText = segment?.buttonText.toNonBlankOrNull()
            ?: subContent?.title.toNonBlankOrNull()
            ?: return null

        return CashbackCategoryInfoDto(
            iconUrl = content.iconName,
            title = categoryTitle(content.name, category.percentRate),
            text = text.value,
            infoDeeplink = categoryDeeplink(headers, segment?.deeplink ?: subContent?.deeplink),
            buttonText = buttonText.value,
        )
    }
```

# Вывод

goto ругали за изменение потока выполнения, но исключения тоже его меняют. Ругают же их значительно реже. Действительно, проще в случайном месте Spring (в нашем случае) программы выбросить исключение, которое будет единообразно обработано прежде чем отдать ответ клиенту на выходе из контроллера. А в чём проблема? Написанное в одном месте исключение условный jacoco заставит нас проверить локально, а во всех бизнес-сценариях уже нет). Как повлияет это исключение на работу программы каждый раз надо проверять заново. Это особенно тяжело, если добавлятся код, который использует где-то под капотом метод с исключением.

Что делать? Попробую сформировать правила:

1) исключение, если и должно быть выброшено, то в идеале как можно ближе к точке входа в приложение / выхода из приложения:
* при старте приложения, а не в процессе работы;
* в контроллерах (или, что уже хуже в публичных методах сервисов), чтобы код был максимально переиспользуем и сопровождаем.

2) выкидываем как можно более специфические исключения, если это возможно;

3) пытаемся делать невозможным некорректное состояние (снижаем неопределённость) в первую очередь за счёт введения более специфичных типов:
* меньше проверок в коде;
* лучше считывается семантика (как сама по себе, так и с учётом предыдущего подпункта);
* проще модифицировать код (как результат предыдущих двух).

4) используем Result (в том числе иерархии на его основе) / Optional, чтобы не нарушать поток выполнения в случайном месте (примеры есть в предыдущем решении задания HW).