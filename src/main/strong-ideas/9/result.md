**Методы, которые используются только в тестах**

В моем проекте такие методы можно отнести к трем категориям:

1. Избавляемся от дублирования, чтобы соблюсти предусловие в серии тестов. 

Прежде чем поучаствовать в розыгрыше пользователь должен запросить о нем информацию. Так как в серии "интеграционных" тестов проверяем работу фиксации победителя, то предусловие должно быть соблюдено. Метод используется для снижения дублирования и не требует рефакторинга.

```
private fun preserveWinnerOfferId() {
    wireMockServer.stubForOffersSuggestionClient(...)
    wireMockServer.stubForOffersDirectoryClient(...)

    val exchange = webTestClient.get()
        .uri("/wheel-of-fortune?offerDate=$APRIL")
        .androidMobileHeaders()
        .exchange()
        .expectStatus().isOk
        .expectBody()
        .json(getExpectedResponse("wheel-of-fortune/get/ok.json"))
}
```

2. Компактная запись конструктора

Если в тесте не нужны все подробности заполнения экземпляра класса, то для лучшей концентрации на тестируемой функциональности выношу конструктор в отдельный метод. Метод используется для снижения дублирования и улучшения читаемости и не требует рефакторинга.

```
private fun getLoyaltyCardTerms(cardContractId: String?, servicePackage: String?) =
    LoyaltyCardTerms(
    defaultCardType = "ANY",
    defaultImageURL = "ANY",
    defaultCardName = "ANY",
    cashbackPercentRate = "ANY",
    cardType = "ANY",
    cardContractId = cardContractId,
    servicePackage = servicePackage,
    bonusAccountTypeId = "ANY",
    loyaltyProgramIds = emptyList(),
    cardCashbackTermsId = 0,
)
```

3. Генерация тестовых данных

В программе есть алгоритм, который должен производить сортировку последовательности из 4 элементов. Для того чтобы протестировать эту функциональность, я добавил в тесты метод, который формирует все возможные входные последовательности для заданного набора. Т.о. тестирование проходит на всех возможных входных данных. Вероятно, такой способ является избыточным, т.е. требуется ограничиться некоторой выборкой из всего множества входных данных. Выбор определенных входных последовательностей показался мне неочевидным, а в сочетании с малым количеством различных входных вариаций и возможностью протестировать все комбинации мой подход к реализации теста выглядит разумным. При значительно бОльшем числе входных последовательностей потребуется ограничение числа тестов, но в данный момент не вижу необходимости в рефакторинге. 

**Цепочки методов. Метод вызывает другой метод, который вызывает другой метод, который вызывает другой метод, который вызывает другой метод... и далее и далее.**

Если цепочки вызовов слишком длинные, то зачастую это говорит о том, что в класс берет на себя слишком много ответственности, которую можно делегировать. В представленном примере не самая длинная цепочка, но все же мы ее укоротим и упростим понимание работы класса. Разделим подтвержденные и предложенные для выбора категории по разным классам:

[Код "до"](..%2F..%2Fjava%2Fstrong%2Fideas%2Flesson_9%2Fbefore)

[Код "после":](..%2F..%2Fjava%2Fstrong%2Fideas%2Flesson_9%2Fafter)

**У метода слишком большой список параметров.**

Метод с большим списком параметров найти достаточно проблематично, так как это слишком явный признак кода с душком. Такой метод рефакторится до попадания в удаленный репозиторий. Разрастанию числа аргументов также препятствует статический анализатор, который не дает передавать более 5 аргументов. Однако даже в методах с маленьким числом аргументов встречаются возможности оптимизации. 

Код "до":

```
    public CashbackConditions getWidgetCashbackConditions(Headers headers, String cardId) {
        CardDTO card = cardService.getMaskedCard(headers, cardId);

        List<LoyaltyCardInfo> loyaltyCardsInfo = loyaltyCardInfoService.getLoyaltyCardsInfo(headers);
        return getWidgetCashbackConditions(headers, card, loyaltyCardsInfo);
    }

    public CashbackConditions getWidgetCashbackConditions(Headers headers,
                                                          CardDTO card,
                                                          List<LoyaltyCardInfo> loyaltyCardsInfo) {
```

Любой вызов извне всегда сводится к вызову второго метода. Зачем получать в таком случае loyaltyCardsInfo в первом методе и передавать его во второй, если можно обойтись без передачи лишнего аргумента? В данном случае это можно делать безболезненно. Бывают же случаи, когда приходится вычислять аргумент заранее и передавать его в независимые участки кода, а не вычислять на месте при необходимости, так как это вычисление обходится слишком дорого.

Код "после":

```
    public CashbackConditions getWidgetCashbackConditions(Headers headers, String cardId) {
        CardDTO card = cardService.getMaskedCard(headers, cardId);
        return getWidgetCashbackConditions(headers, card);
    }

    public CashbackConditions getWidgetCashbackConditions(Headers headers,
                                                          CardDTO card) {
        List<LoyaltyCardInfo> loyaltyCardsInfo = loyaltyCardInfoService.getLoyaltyCardsInfo(headers);
```

**Странные решения. Когда несколько методов используются для решения одной и той же проблемы, создавая несогласованность.**

В разных микросервисах, а иногда и в рамках одного микросервиса в тестах можно увидеть разные способы получения контента json-файла для дальнейшего сравнения с результатом выполнения метода. Отсутствие единого подхода рассеивает внимание, создавая проблему на ровном месте. Вот лишь некоторые варианты, которые удалось найти:

```
fun getExpectedResponse(filePath: String): String =
    readFile("/__files/expected-response/$filePath")

fun getExpectedResponse(filePath: String): String =
    StringLoader.fromClasspath(this::class, "/__files/expected-response/$filePath")
    
fun expectedResponsePath(fileName: String): String =
    StringLoader.fromClasspath("/__files/expected-response/$fileName.json")
    
...
```

**Чрезмерный результат. Метод возвращает больше данных, чем нужно вызывающему его компоненту.**

В коде одного из микросервисов есть два метода в контроллере, от которых каждый раз у меня идет кровь из глаз:

```
@GetMapping
suspend fun getCustomerBaseInfo(
        @MandatoryHeadersConstraint(userId = true) headers: Headers,
): CustomerInfoWithAdditionalData = withTraceContext {
    customerInfoService.getInfoWithAdditionalData(headers, additionalData)
}

@GetMapping(path = "/extended")
suspend fun getCustomerExtInfo(
        @MandatoryHeadersConstraint(userId = true) headers: Headers,
): CustomerExtendedInfoResponse = withTraceContext {
    customerInfoService.getExtendedInfoWithProvider(headers, additionalData)
}
```

Начиналось все с выбранных названий методов, аргументов и классов (InfoWithAdditionalData и ExtendedInfo), которые не дают никакого понимания, что вообще происходит под капотом. Такой дизайн развязывает руки: каждый разработчик считает своим долгом дополнить возвращаемое значение очередным полем. Так же просто любое поле из ответа можно убрать. К чему это приводит?
1) новому пользователю сложно разобраться с API
2) получаемый объем данных избыточен для большинства запросов извне и как следствие избыточная паразитная нагрузка на зависимые сервисы

Что в этому случае требуется сделать? Разбить получение информации на независимые доменные модели, что позволит большинству пользователей API получать необходимую информацию за ограниченное число запросов:

```
@GetMapping(path = "/package")
suspend fun getCustomerPackage(
    @MandatoryHeadersConstraint(userId = true) headers: Headers
): CustomerPackage = withTraceContext { 
    customerService.getPackage(headers) 
}
```