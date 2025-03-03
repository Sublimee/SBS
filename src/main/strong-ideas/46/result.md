# Пример 1

Есть эндпоинт в сервисе, отвечающем за бонусные счета пользователей:

```kotlin
@GetMapping
suspend fun getBonusAccounts(
    @MandatoryHeadersConstraint(userId = true) headers: Headers,
    @RequestParam(value = "kids", defaultValue = "false") kids: Boolean,
): List<Bonus> = withTraceContext {
    if (featureToggleService.hasFeatureIncludeTech(kidsProperties.featureKidsWithPersonalAccount, headers)) {
        loyaltyServiceV2.getBonusAccounts(headers, kids)
    } else {
        loyaltyService.getBonusAccounts(headers, kids)
    }
}
```

Видим, что к эндпоинту обращаются и пользователи двух категорий: дети и не дети. Наша задача -- распилить сервис на два, чтобы фронт ходил на разные сервисы за списком бонусных счетов. Домен бонусных счетов так разросся, что требуется провести такой рефакторинг. Текущий сервис продолжит отвечать за все "сырые" счета пользователей, а новый -- будет делать их постобработку для домена "дети".

# Пример 2

Есть такой проблемный код (и ряд аналогичных), по которому сложно понять, какой внешний вид контента будет у пришедшего пользователя:

```kotlin
private suspend fun getBoomerangContentStyle(headers: Headers): BonusContentStyle {
    if (headers.os == null || headers.appVersion == null) {
        return BonusContentStyle.MEDIUM
    }
    val thresholdAppVer =
        cashbackBonusProperties.boomerangBonusProperties.appSpecificHsmallStyleSupport[headers.os]
    return if (thresholdAppVer != null && headers.appVersion >= thresholdAppVer) {
        BonusContentStyle.SMALL
    } else {
        BonusContentStyle.MEDIUM
    }
}
```

Один из вариантов решения -- задавать списком все возможные стратегии отображения, чтобы в них было проще ориентироваться:

```kotlin
class BonusContentStyleStrategy(
    private val os: String?,
    private val appVersionRange: AppVersionRange,
    private val style: BonusContentStyle,
) : ContentStyleStrategy {
    
    override fun appliesTo(headers: Headers): Boolean = headers.os == os && headers.appVersion in appVersionRange
    
    override fun getContentStyle(): BonusContentStyle {
        return style
    }
}
```

```yaml
boomerangBonusProperties:
  defaultContentStyle: MEDIUM
  contentStyleStrategies:
    - os: android
      appVersionRange:
          minAppVersion: 0
          maxAppVersion: 11.0.4
      style: MEDIUM
    - os: android
      appVersionRange:
          minAppVersion: 11.0.5
          maxAppVersion: 999.999.999
      style: SMALL
    - os: ios
      appVersionRange:
          minAppVersion: 0
          maxAppVersion: 13.3.7
      style: MEDIUM
    - os: ios
      appVersionRange:
          minAppVersion: 13.3.8
          maxAppVersion: 999.999.999
      style: SMALL
    - os: null
      appVersionRange:
          minAppVersion: null
          maxAppVersion: null
      style: MEDIUM
```

Бизнес-код будет выглядеть следующим образом:

```kotlin
private suspend fun getBoomerangContentStyle(headers: Headers): BonusContentStyle = boomerangBonusProperties
    .contentStyleStrategies
    .firstOrNull { it.appliesTo(headers) } ?: boomerangBonusProperties.defaultContentStyle
```

Если развивать эту идею, подтягивая в конфигурацию различия между версиями ОС и приложений, можем прийти от локального BonusContentStyleStrategy к некоему подобию ролей для пользователя, где каждая роль будет содержать все особенности отображения на UI. Роль эту соответственно мы можем вычислить уже при входе в наш сервис.

# Пример 3

Следующая проблема происходит на стыке front'а и backend'a. Формируем карусель виджетов:

```kotlin
fun getBonusListView(vararg sourceLists: List<BonusDto?>): List<BonusDto> {
    val composed = sourceLists.toList().flatten().filterNotNull()
    if (composed.size == 1) {
        composed.forEach { it.size = BonusSize.WIDE } // enum class BonusSize { SQUARE, WIDE }
    }
    return composed.sortedBy { it.order }
}
```

В случае, если виджет один, то он должен быть широким. Можно, конечно, рассматривать решение установки ширины виджета, как фичу с заделом на будущее, однако ситуаций, когда в списке есть и широкий и квадратный виджет, не было и нет сейчас. Можно избавиться от этой проверки на backend'е, предоставив возможность определять размер на front'е:

```kotlin
fun getBonusListView(vararg sourceLists: List<BonusDto?>): List<BonusDto> = sourceLists
    .toList()
    .flatten()
    .filterNotNull()
    .sortedBy { it.order }
}
```

# Пример 4

Избавимся от when, используя полиморфизм:

```kotlin
@RestController
class BonusController(
    private val premiumBonusService: PremiumBonusService,
    private val composedBonusService: ComposedBonusService,
    private val cashbackBonusService: CashbackBonusService,
    private val nonFinancialBonusService: NonFinancialBonusService,
    private val kidsBonusService: KidsBonusService,
) : BonusControllerApi {
    
    override fun getBonus(
        @PathVariable("type") type: BonusType,
        @RequestParam(name = "version", defaultValue = "2") version: Int,
    ): List<BonusDto> = when (type) {
        PREMIUM -> premiumBonusService.getBonuses(headers, version)
        CASHBACK -> cashbackBonusService.getBonuses(headers, version)
        NON_FINANCIAL -> nonFinancialBonusService.getBonuses(headers, version)
        KIDS -> kidsBonusService.getBonuses(headers, version)
        ALL -> composedBonusService.getAllBonuses(headers, version)
    }

    ...
```

Перечисленные сервисы и так уже реализуют один интерфейс, осталось только внести их все в коллекцию и сделать выборку по ключу, который зашьем в самих сервисах:

```kotlin
@Configuration
class BonusServices {

    @Bean
    fun bonusTypeToBonusServiceMap(bonusServices: List<BonusService>): Map<BonusType, BonusService> =
        bonusServices.associateBy { it.getBonusType() }
}
```

```kotlin
@RestController
class BonusController(
    private val bonusServiceMap: Map<BonusType, BonusService>,
    ...
) : BonusControllerApi {

    override fun getBonus(
        @PathVariable("type") type: BonusType,
        @RequestParam(name = "version", defaultValue = "2") version: Int,
    ): List<BonusDto> = bonusServiceMap[type].getBonuses(headers, version)

    ...
```

# Пример 5

Рассмотрим Пример 4 с еще одной стороны. У каждого пользователя в системе есть роль. В одном из сервисов роль то ли не приходит, то ли теряется в контексте, поэтому разработчик решил добавить проверку:

```kotlin
private fun createFeignHeaders(headers: Headers): FeignHeaders {
    return FeignHeaders.of(
        Headers.of(
            headers.asMap()
                .also {
                    it.putIfAbsent(HeaderNames.USER_ROLE, CLIENT)
                }
        )
    )
}
```

С причинами нужно разбираться, но правильным решением будет явно указать в контракте сервиса, что заголовок userRole является обязательным:

```kotlin
@RestController
class BonusController(
    ...
) : BonusControllerApi {

    override fun getBonus(
        @MandatoryHeadersConstraint(userId = true, userRole = true) headers: Headers,
        ...
```

# Вывод

Как просто поставить if в коде, так же просто if из кода бывает убрать. Это своего рода красная тряпка, которую достаточно легко найти поиском по проекту, как и другие потенциально уязвимые места с ключевыми словами (for, when и т.п.).

В наших примерах мы избавляемся от условной проверки за счет:
1 -- внедрения нового сервиса, где роль потребителя нам заранее известна (мета-правило 1);
2 -- явного указания списка возможных вариантов потребителей (мета-правило 1);
3 -- упрощения логики на стороне backend'a (мета-правило 2);
4 -- использования полиморфизма (мета-правило 1);
5 -- перемещения условия непосредственно в контракт эндпоинта (мета-правило 1);

Как видим, мета-правило 1 превалирует в нашем списке. Это происходит по двум причинам:
1) оно проще считывается, чем мета-правило 2, так как больше привязано к уровню реализации. Мета-правило 2 зачастую требует размышления о программе на уровне аналитики/спецификации;
2) мета-правило 1 покрывает большее количество сценариев некорректного применения if (по крайней мере в моих проектах), так как эти сценарии чаще генерируются разработчиками.