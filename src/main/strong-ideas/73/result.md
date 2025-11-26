# Пример 1

```kotlin
interface QuestsClient {

    suspend fun getActiveQuests(headers: Headers): QuestsResponseDto

    suspend fun activateQuest(headers: Headers, questId: Long)

    suspend fun sendAnalyticsEvent(
        headers: Headers,
        event: AnalyticsEvent,
    )
}
```

Выделим независимые активности, которые можно переиспользовать в других сервисах: 

```kotlin
interface Loader<in R, out Z> {
    suspend fun load(request: R): Z
}

interface Activator<in R> {
    suspend fun activate(request: R)
}

interface Auditor<in E> {
    suspend fun audit(event: E)
}
```

И перепишем имплементацию:

```kotlin
typealias QuestsLoader = Loader<QuestsRequest, QuestsResponseDto>
typealias QuestStarter = Activator<ActivateQuestRequest>
typealias QuestsAuditor = Auditor<QuestEvent>

@Service
class QuestsService(
    // ...
) : QuestsLoader,
    QuestStarter,
    QuestsAuditor {

    override suspend fun load(request: QuestsRequest): QuestsResponseDto {
        // ...
    }

    override suspend fun activate(request: ActivateQuestRequest) {
        // ...
    }

    override suspend fun audit(event: QuestEvent) {
        // ...
    }
}
```

Можно расширить идею с получением значений:

```kotlin
interface Loader<in R, out Z> {
    suspend fun load(request: R): Z
}

interface CollectionLoader<in R, out E, out C : Collection<E>> {
    suspend fun loadCollection(request: R): C
}

interface MapLoader<in R, K, out V, out M : Map<K, V>> {
    suspend fun loadMap(request: R): M
}
```

# Пример 2

Интерфейс для работы с фичами. withFeatures обогащает контекст корутины переданными фичами. Остальные два метода выдают информацию о наличии фичи/набора фич у клиента:

```kotlin
interface FeatureToggleService {

    suspend fun hasFeature(headers: Headers, feature: String): Boolean

    suspend fun hasFeatures(headers: Headers, features: List<String>): Map<String, Boolean>
    
    suspend fun <T> withFeatures(
        userId: String,
        vararg features: String,
        body: suspend CoroutineScope.() -> T,
    ): T
}
```

Разделим интерфейс:

```kotlin
interface SingleExistenceChecker<in C, in K> {
    suspend fun exists(context: C, key: K): Boolean
}

interface ManyExistenceChecker<in C, K> {
    suspend fun existsAll(context: C, keys: Collection<K>): Map<K, Boolean>
}

interface Scoped<in C> {
    suspend fun <T> extendedWith(
        context: C,
        body: suspend CoroutineScope.() -> T,
    ): T
}

```

и выполним имплементацию: 

```kotlin
typealias SingleFeatureChecker = SingleExistenceChecker<Headers, String>

typealias ManyFeatureChecker = ManyExistenceChecker<Headers, String>

typealias FeatureScoped = Scoped<FeatureScopeContext>

class FeatureToggleClient(
    // ..
) : SingleFeatureChecker,
    ManyFeatureChecker,
    FeatureScoped {

    override suspend fun exists(header: Headers, feature: String): Boolean {
        // ...
    }

    override suspend fun existsAll(header: Headers, features: Collection<String>): Map<String, Boolean> {
        // ...
    }

    override suspend fun <T> extendedWith(
        params: FeatureScopeParams,
        body: suspend CoroutineScope.() -> T,
    ): T {
        // ...
    }
}
```

# Пример 3

Интерфейс как бы намекает:

```kotlin
interface MultistepServiceInterface {
    suspend fun init(headers: Headers, initParameters: InitParameters, transaction: TransactionEntity?): Tab
    suspend fun next(headers: Headers, nextStepRequest: NextStepRequest, transaction: TransactionEntity): Tab
    suspend fun reload(headers: Headers, reloadRequest: ReloadRequest, transaction: TransactionEntity?): Tab =
        error("notImplemented")
}
```

Разделим на отдельные интерфейсы:

```kotlin
interface MultistepInitializer<in C, in I, in TX, out R : Tab> {
    suspend fun init(context: C, initRequest: I, transaction: TX?): R
}

interface MultistepStepper<in C, in N, in TX, out R : Tab> {
    suspend fun next(context: C, nextStepRequest: N, transaction: TX): R
}

interface MultistepReloader<in C, in RQ, in TX, out R : Tab> {
    suspend fun reload(context: C, reloadRequest: RQ, transaction: TX?): R
}
```

Вообще говоря nullability-типы в сигнатурах предполагают различие поведения. Как вариант разбить такие интерфейсы на 2: с nullability и без него.

# Вывод

ISP -- мощный принцип, который позволяет снизить число зависимостей класса, имплементирующего интерфейс. На фоне снижения сложности интерфейса получаем больше возможностей, чтобы получившиеся маленькие интерфейсы переиспользовать в других сценариях. Это достигается, в том числе за счет максимального обобщения сигнатуры. 

Нужно ли все это делать это заранее или уже после того, как найден потенциальный код-кандидат? С одной стороны у меня нет аргументов против. ISP + обобщение (ну или лучше сказать -- попытку) можно делать на этапе создания интерфейса/интерфейсов. Однако в МС-архитектуре не так часто приходится переиспользовать один и тот же интерфейс для разных целей. Если нужно обобщить поведение каких-то однородных локальных (в рамках одного МС) классов, то интерфейсы выводятся сами собой хотя бы в целях удобства. Выделение каких-то общих идей, которые находят свое отражение в разных МС -- сложнее. Хотя если каждый раз продумывать интерфейсы локально, то в какой-то момент можно заметить их одинаковость в разных МС и впоследствии вынести в библиотеку. А вот на этом этапе уже можно и подумать над удобным обобщением.

Еще, конечно, максимально обобщенный интерфейс хуже ложится с точки зрения используемых названий методов под конкретные домены, в которых они применяются. В этом случае лучше не доводить обобщение до абсурда. Интерфейс все же должен добавлять понимание кода, а не просто вносить дополнительный уровень абстракции.
