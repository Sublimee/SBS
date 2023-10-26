## Пример № 1

Язык Kotlin предоставляет синтаксический сахар, который очень сильно сокращает конструкции управления. Вот один из примеров: 

```kotlin
val illegalCategoryRepresentation: CategoryRepresentation? = categoriesSection.categories
    .find { it.isSelected == false && it.isEditable == false }

if (illegalCategoryRepresentation != null) {
    logger.error { "Category with id=${illegalCategoryRepresentation.id} can not be selected by user" }
    ...
}
```

В случае, если среди категорий будет найдена некорректно заполненная, то следует залогировать ее идентификатор для внесения правок на стороне справочника. Этот код можно сделать гораздо более компактным:

```kotlin
categoriesSection.categories
    .find { it.isSelected == false && it.isEditable == false }
    ?.let {
        logger.error { "Category with id=${it.id} can not be selected by user" }
        ...
    }
```

Попробуем добавить другие конструкции, которые будут упрощать наши решения и делать их более компактными.

## Пример № 2

У нас в программе была проблема следующего характера: если пользователь на мобильном устройстве прерывал запрос (закрывал экран), то выполняемая корутина выбрасывала CancellationException вверх по иерархии. Если ловить CancellationException напрямую или через catch(e: Exception) в suspend методах, то это приводило к тому, что корутина, которая больше не нужна, выполняла бесполезную работу или выводила бесполезный лог:

```kotlin
suspend fun doSomeSuspendWork(request: Request): List<Response> =
    try {
        client.getMono().awaitSingleOrNull()
    } catch (e: Exception) {
        logger.error(e) { "Something went wrong" }
    }
```

Для того, чтобы решить эту проблему, нужно просто сделать следующее:

```kotlin
suspend fun doSomeSuspendWork(request: Request): List<Response> =
    try {
        client.getMono().awaitSingleOrNull()
    } catch (e: Exception) {
        if (e is CancellationException) {
            throw e
        }
        logger.error(e) { "Something went wrong" }
    }
```

или воспользоваться более читаемым вариантом:

```kotlin
suspend fun doSomeSuspendWork(request: Request): List<Response> =
    try {
        client.getMono().awaitSingleOrNull()
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        logger.error(e) { "Something went wrong" }
    }
```

Но лучшим вариантом будет использование обертки runCatchingCancellable:

```kotlin
suspend fun doSomeSuspendWork(request: Request): List<Response> =
    runCatchingCancellable {
        client.getMono().awaitSingleOrNull()
    }.onFailure {
        logger.error(it) { "Something went wrong" }
    }.getOrDefault(emptyList())
```

runCatchingCancellable реализована следующим образом:

```kotlin
inline fun <R> runCatchingCancellable(block: () -> R): Result<R> {
    return try {
        Result.success(block())
    } catch (e: CancellationException) {
        throw e
    } catch (e: Throwable) {
        Result.failure(e)
    }
}
```

## Пример № 3

В нашей системе есть множество справочников, которые мы не запрашиваем каждый раз из бэкенда, а прихраниваем в кэше. Некоторые кэши в целях оптимизации не протухают, а обновляются соответствующими задачами, выполняющимися по расписанию. Как это выглядит в коде:

```kotlin
@Scheduled(fixedDelayString = "#{@cacheConfiguration.calculateSecondsDelay()}", timeUnit = TimeUnit.SECONDS)
fun updateUserInterfaceContent(): Unit =
    lockRegistry.lockAndExecute(USER_INTERFACE_CONTENT_CACHE_NAME) {
        commonProviderService.updateUserInterfaceContent(TECH_HEADERS)
    }
```

Очень похоже на сквозную функциональность, которую хотелось бы скрыть от глаз пользователя, оставив в теле метода только.
Используя механизм BeanPostProcessor обернем вызов метода в proxy с помощью аннотации:

```kotlin
@Scheduled(fixedDelayString = "#{@cacheConfiguration.calculateSecondsDelay()}", timeUnit = TimeUnit.SECONDS)
@LockAndExecute(lockKey = USER_INTERFACE_CONTENT_CACHE_NAME)
fun updateUserInterfaceContent(): Unit {
    commonProviderService.updateUserInterfaceContent(TECH_HEADERS)
}
```

## Вывод

В первом примере упоминаются scope functions. Это яркий пример попытки заменить развесистые конструкции управления на лаконичные вызовы функций. Что получаем от их использования, для чего они (частый вопрос собеседований)? Это целый комплекс положительных моментов:

* повышение читаемости и структурирование кода

  * избегаем дублирования (если необходимо выполнить несколько операций с одним и тем же объектом, то его имя можно не дублировать)
  
  * уменьшается число промежуточных временных переменных

  * более четкое выражение намерения
  
* null-safety (безопасный вызов ?., перекликается с первым пунктом из вывода)

В явном виде в Java scope functions, как и многих других конструкций нет. По этой причине после написания кода на Kotlin к Java возвращаться совсем не хочется: тяжелее писать выразительный код. Мне это стало понятно только после того, как я получил большой коммерческий опыт, так как написание отдельных небольших участков кода обычно никогда не вызывают проблем.

Если таких встроенных конструкций нет в языке, то их приходится добавлять самостоятельно. В этом смысле комбинация Java/Kotlin + Spring имеют богатые опции. Однако, зачастую не встроенные в язык решения, все же будут не настолько выразительными (пример 2 и 3).