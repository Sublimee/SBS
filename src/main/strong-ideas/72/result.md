# Пример 1

```kotlin
@DslMarker
annotation class WorkflowDslMarker

@WorkflowDslMarker
data class WorkflowDsl<T : Any, C : WorkflowContext>(
    private val steps: MutableMap<StepName, Step<T, C>> = linkedMapOf(),
    private var errorBehavior: WorkflowErrorBehavior = WorkflowErrorBehavior.Terminate
) {

    @WorkflowDslMarker
    open class StepDsl<T : Any, C : WorkflowContext>(private val step: Step<T, C>) {

        val name by step::name

        init {
            require(step.name.isNotBlank()) { "StepName cannot be empty or blank" }
        }

        constructor(name: StepName) : this(Step(name))

        fun <I : WorkflowInstance<T, C>> action(action: StepAction<I, T, C>) {
            step.action = action
        }

        operator fun invoke(): Step<T, C> = step
    }

    private fun step(name: StepName, block: StepDsl<T, C>.() -> Unit) {
        StepDsl<T, C>(name).apply(block)().also { steps[name] = it }
    }

    fun step(name: Enum<*>, block: StepDsl<T, C>.() -> Unit) {
        step(name.name, block)
    }

    infix fun errorBehavior(errorBehavior: WorkflowErrorBehavior) {
        this.errorBehavior = errorBehavior
    }

    operator fun invoke(): WorkflowDefinition<T, C> = WorkflowDefinition(
        steps = steps.values,
        defaultErrorBehavior = errorBehavior
    )
}

fun <T : Any, C : WorkflowContext> workflow(block: WorkflowDsl<T, C>.() -> Unit): WorkflowDefinition<T, C> =
    WorkflowDsl<T, C>().apply(block)()
```

и пример использования:

```kotlin
override val definition: WorkflowDefinition<AwardProcessData, GameContext> =
    workflow {
        this errorBehavior WorkflowErrorBehavior.RetryOrSuspend(
            maxRetries = workflowProperties.maxRetries,
            retryInterval = workflowProperties.retryInterval
        )

        step(Steps.CREATE_MEMBER_ACHIEVEMENT) {
            action(this@AwardProcess::createMemberAchievement)
        }

        step(Steps.REWARD_MEMBER) {
            action(this@AwardProcess::rewardMember)
        }

        step(Steps.NOTIFY_MEMBER) {
            action(this@AwardProcess::notifyMember)
        }
    }
```

Функция workflow задает сценарий полагаясь на результат шага T : Any (non-nullable) и контекст C : WorkflowContext. Для любых конкретных типов T и C, удовлетворяющих ограничениям, можно построить workflow без изменения кода.

# Пример 2

Пока слабый пример LSP в ФП:

```kotlin
fun MutableMap<String, Any>.putIfNotNull(
    valueGetter: () -> Pair<String, Any?>
): MutableMap<String, Any> {
    val (key, value) = valueGetter()
    if (value != null) {
        this[key] = value
    }
    return this
}
```

Доработаем его, чтобы работать с любыми MutableMap<K, V> и связанными с ними Pair<K, V?>: 

```kotlin
fun <K, V> MutableMap<K, V>.putIfNotNull(
    valueGetter: () -> Pair<K, V?>
): MutableMap<K, V> {
    val (key, value) = valueGetter()
    if (value != null) {
        this[key] = value
    }
    return this
}
```

putIfNotNull можно вызвать на любых реализациях мутабельных мап и получать соответствующий результат, завязанный на переданные типы. 


# Пример 3

```kotlin
fun <OUT_K, K, V, M : Map<K, V>> getInnerContextElement(
    contexts: Map<OUT_K, M>,
    key: OUT_K,
    getter: (M) -> V,
    default: V
): V =
    contexts[key]
        ?.let(getter)
        ?: default
```

Функция может работать с любыми вложенными мапами M, не зависит от конкретных типов.

# Пример 4

```kotlin
fun <T, R> validateAll(
    values: List<T>,
    validator: Validator<in T, out R>
): List<R> =
    values.map(validator::validate)
```

Функция ничего не знает ни о типе данных, с которым работает, ни о результате.


# Вывод

В ФП LSP не про наследование, как в ООП, а про правильное использование полиморфизма и абстракций. Это, конечно, в первую очередь свойственно правильным библиотечным методам, когда нужно правильно и максимально, насколько это возможно, ограничить типы, в то же время не завязываясь на них. 

Для этого, как и в ООП:
* используем дженерики с ограничением типов через in и out;
* не завязываемся на конкретные классы;
* не делаем приведение типов.

Это даст нам максимальную универсализацию метода под разные сценарии использования, но не приведет к ошибкам в рантайме.

Для поиска "правильных" проявлений LSP в ФП нужно фильтровать примеры с обычным параметрическим полиморфизмом. В этом смысле пример 4 можно считать примером "на грани".