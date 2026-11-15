# Пример 1. Заголовочный интерфейс + протекающая абстракция + поверхностный интерфейс

Возьмём интерфейс в одном из сервисов:

```kotlin
interface CloseAvailabilityService {
    suspend fun getCloseAvailability(headers: Headers, accountNumber: String): CloseAvailabilityDto
    suspend fun getClosePermission(headers: Headers, accountNumber: String): ClosePermissionDTO
    fun needCloseCreditContract(account: Account): Boolean
    suspend fun isAvailableToClose(headers: Headers,
                                   closeAccountInitialContext: CloseAccountInitialContext): CloseAvailabilityResult
}
```

Какие с ним есть проблемы?

1) у него есть единственная реализация. Интерфейс просто повторяет публичные методы класса. Это не что иное, как 
заголовочный интерфейс.

2) собраны методы разного уровня и назначения: 
* getCloseAvailability(...) вызывается из контроллера и отдаёт DTO наружу;
* needCloseCreditContract(...) однострочная проверка признака счёта;
* getClosePermission(...) является алиасом для вызова Feign‑клиента;
* isAvailableToClose(...) -- проверка для дебетовых счетов.

Как несложно догадаться, CloseAccountController вызывает только getCloseAvailability, а CloseAccountServiceImpl вызывает
остальные три метода, что является нарушением ISP.

3) getCloseAvailability(...) возвращает объявленный на уровне сервиса DTO, а getClosePermission(...) возвращает DTO из 
стартера ...starter.client.feign... . Абстракции протекли. Плюс это очень сильно ограничивает вариативность реализаций.

4) если посмотреть на методы, использующие интерфейс для обработки разных типов счетов, то становится видно, что 
пользователю интерфейса надо досконально знать последовательность и в принципе возможность выполнения вызовов для 
каждого из них, т.е. интерфейс в данном случае абстракцию не предоставляет вовсе, а реализация интерфейса -- это просто 
"класс с набором каких-то методов".

```kotlin
if (closeAvailabilityService.needCloseCreditContract(account)) {
    val permission = closeAvailabilityService.getClosePermission(headers, accountNumber) 
    ...
} else closeAvailabilityService.isAvailableToClose(headers, context) ...
```

# Пример 2. Заголовочный интерфейс + поверхностный интерфейс

Посмотрим на интерфейс для BFF-сервиса:

```kotlin
interface ViewFiller {
    fun fillView(context: ScreenContext, account: AccountDTO): Any?
    fun isSuitable(context: ScreenContext, account: AccountDTO): Boolean
}
```

Реализации fillView(...) отдают совершенно разные типы возвращаемых значений (RectangleWidgetContent, 
RectangleWidgetContent?, DataViewsWrapper, SduiViewsWrapperDto, Map<String, Any>, Any?). Разброс объясняется просто: для 
разных виджетов генерируется подходящий по формату контент, а сервису не важно, какой структуры и содержания ответ уйдёт
наружу. Клиенту же контракт, очевидно, важен, но в интерфейсе он не зафиксирован явно, так как статическая типизация по
сути отключена. Общая сигнатура была вытащена механически из всех реализаций в заголовочный интерфейс, поэтому 
1) не передаёт семантику результата работы (не является абстракцией). А потом догадывайся, как интерпретировать 
emptyMap<String, Any>() и Any?;
2) содержит DTO, завязывая реализации на клиентскую зависимость.

# Пример 3. Нарушение LSP + протекающая абстракция

```kotlin
@JsonTypeInfo(use = NAME, include = EXISTING_PROPERTY, property = "success")
@JsonSubTypes(
    Type(value = FindParticipantSuccessResponse::class, name = "true"),
    Type(value = FindParticipantErrorResponse::class, name = "false"),
)
interface FindParticipantResponse {
    val success: Boolean
}
```

Интерфейс содержит только служебное поле, позволяющее понять, успешно ли прошла операция. От значения success зависит, 
экземпляр какого класса мы получим при десериализации.

Далее в коде выполняется ручной даункаст для определения конкретной реализации:

```kotlin
if (response.success) {
    val participant = response as FindParticipantSuccessResponse
    ...
} else {
    val error = response as FindParticipantErrorResponse
    ...
}
```

Как техническое декларативное решение для избавления от boilerplate кода на границе сервиса пойдёт, но даункаст сводит 
на нет этот плюс. Получилось решение, расширяемое только вручную (оперируем success), с нарушением LSP. В дополнение 
лучше было бы добавить sealed interface ParticipantSearchResult, с которым бы уже работали в бизнес-коде.

# Пример 4. Заголовочный интерфейс

Интерфейс, состоящий целиком из методов с дефолтной реализацией-заглушкой:

```java
public interface Replacer {
    default String replace(String template, TransactionData data,       ReplacerAdditionalData add) { return template; }
    default String replace(String template, CommissionWillBeData data,  ReplacerAdditionalData add) { return template; }
    default String replace(String template, ServiceConnectionData data, ReplacerAdditionalData add) { return template; }
    default String replace(String template, ArbitraryData data,         ReplacerAdditionalData add) { return template; }
}
```

Большинство классов-реализаций переопределяют методы интерфейса лишь частично, например: 

```java
@Component
@Order(NORMAL_PRECEDENCE)
public class AddressReplacer implements Replacer {

    @Override
    public String replace(String template, TransactionData data, ReplacerAdditionalData replacerAdditionalData) {
        ...
    }
}
```

что, очевидно, является нарушением ISP: реализации зависят от методов, которые им не нужны. 

Как вызывается конкретная реализация?

```java
    @Override
    public void visit(TransactionData data) {
        replace(data,
                (replacer, template, transactionData, replacerAdditionalData) ->
                        replacer.replace(template, (TransactionData) transactionData, replacerAdditionalData));
    }

    @Override
    public void visit(ServiceConnectionData data) {
        replace(data,
                (replacer, template, serviceConnectionData, replacerAdditionalData) ->
                        replacer.replace(template, (ServiceConnectionData) serviceConnectionData, replacerAdditionalData));
    }

    @Override
    public void visit(CommissionWillBeData data) {
        replace(data,
                (replacer, template, commissionWillBeChargedData, replacerAdditionalData) ->
                        replacer.replace(template, (CommissionWillBeData) commissionWillBeChargedData, replacerAdditionalData));
    }

    @Override
    public void visit(ArbitraryData data) {
        replace(data,
                (replacer, template, arbitraryData, replacerAdditionalData) ->
                        replacer.replace(template, (ArbitraryData) arbitraryData, replacerAdditionalData));
    }

    private void replace(MessageData data,
                         QuaternaryFunction<Replacer, String, MessageData, ReplacerAdditionalData, String> replaceFunction) {
    
        for (Replacer replacer : replacers) {
            template = replaceFunction.apply(replacer, template, data, replacerAdditionalData);
        }
    }
    
    private interface QuaternaryFunction<T, U, V, W, R> {
        R apply(T t, U u, V v, W w);
    }
```

Сначала тип data определяется через выбор перегрузки visit. Затем data с уже известным типом апкастится до MessageData, 
а затем используется приведение типа, чтобы выбрать нужную перегрузку replace. Вау! Новый тип данных при случае нужно 
будет добавлять вручную. В итоге получившийся интерфейс -- это просто набор методов под каждый тип. Абстракции здесь 
нет.

# Пример 5. Поддержка DI

Нашёлся хороший пример, как подтверждение для выводов из статьи:

```kotlin
interface RouteStrategy {
    fun isSupported(headers: Headers, transactionDefinition: TransactionDefinition): Boolean
    suspend fun routeName(headers: Headers, transactionDefinition: TransactionDefinition): RouteName
}

interface AccountRouteStrategy : RouteStrategy

interface DeeplinkStrategy {
    fun isSupported(context: TransactionContext): Boolean
    fun deeplink(): String
}

interface AccountDeeplinkStrategy : DeeplinkStrategy
```

"Пустые" интерфейсы AccountRouteStrategy и AccountDeeplinkStrategy используются в качестве маркеров для Spring, чтобы 
удобно инжектить соответствующие бины списком. Такие интерфейсы используются не как абстракция, а как синтаксический 
сахар для DI.

# Вывод

В статье зафиксировано общепринятое понимание интерфейса ("коллекция абстрактных методов, которые задают некоторый 
"контракт" для класса, который он должен реализовать"), которым чаще всего и пользуются при создании оного. Но задаёт ли 
интерфейс "контракт" для класса? Или это просто удобная формулировка, которая снимает с нас ответственность за 
скрупулёзное выделение абстракций? Нарушается причинно-следственная связь: "выделил интерфейс" -> "получил абстракцию", 
вместо "выделил абстракцию" -> "спроектировал интерфейс". Удобная иллюзия, в которую верят разработчики.

И тогда речь про контракты и абстракции в интерфейсе уже вообще не идёт. Он представляет собой просто коллекцию 
абстрактных методов для класса, которые он должен реализовать. Те самые заголовочные интерфейсы, когда к самому 
интерфейсу не предъявляется никаких требований и он сам ничего не требует. Интерфейс просто существует, становится 
набором методов, который еще и реализуется одним классом. Формально перестали работать с конкретными классами, 
фактически -- добавили новый уровень "абстракции", который ничем не помогает, а лишь затрудняет изучение кода.

Даже если несколько классов содержат одни и те же или близкие по сигнатуре методы, то опять же получается заголовочный 
интерфейс, который возникает механически из автоматического выделения в него одинаковых частей без продумывания смысловой 
нагрузки. Поверхностный (в прямом смысле) подход к выделению интерфейса приводит к более тяжелым последствиям в 
дальнейшем.

Как мы уже видели, в интерфейс в таком случае попадают детали конкретных реализаций, что создаёт сильную связанность 
реализаций и интерфейса. Абстракции протекают, и с этими внесёнными нами собственноручно зависимостями в дальнейшем
приходится считаться. Как итог мы вообще не можем пользоваться преимуществами интерфейсов, кроме объединения нескольких 
реализаций под общим именем. Полиморфизм формально есть, но он сопровождается ручным вычислением типа (нарушение LSP).

Интерфейсы преимущественно "проектируются" (получаются) как одноразовые: очередное бизнес-требование ломает их, и 
требуется масштабный рефакторинг. В рамках микросервиса это делается относительно безболезненно для разработчика (а 
теперь еще проще с LLM), но стоит времени для тестирования и TTM, так как обычно требует серьёзных переделок и 
соответствующего регресса. 

Интерфейс стоит выводить из потребностей клиента, а не из реализации постфактум, что исходно требует этапа 
проектирования до написания самого кода. Это как раз попытка начать с абстракции, которая будет вложена в интерфейс, а 
не наоборот.