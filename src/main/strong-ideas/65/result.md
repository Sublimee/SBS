# Пример 1

Пройдемся по методу получения пользователя, который остался нетронутым с прошлого раза:

```java
@NotNull
private UserEntity getUserEntity(LoginRequest request) {
    UserEntity userEntity = userRepository.findByEmail(request.email())
            .orElseThrow(
                    () -> new AuthException(
                            INVALID_LOGIN,
                            format(WRONG_EMAIL_MESSAGE, request.email())
                    )
            );

    if (isNull(userEntity.getIsActive()) || !userEntity.getIsActive() || nonNull(userEntity.getDeletedAt()))
        throw new AuthException(PARTNER_REMOVED, "user is inactive or deleted");

    checkUserOnDeleteStatus(userEntity);
    checkUserInvitationStatus(userEntity);
    comparePasswords(request.password(), userEntity.getPassword());

    ExecutionResult<Boolean> executionResult = handleRunnableAndReturn(() -> checkPassword(request.password(), TRUE));
    if (!executionResult.getResult() && executionResult.getException() instanceof BadRequestException)
        throw new ForbiddenException(HAVE_TO_CHANGE_PASSWORD, "login failed due to weak password");
    return userEntity;
}
```

В handleRunnableAndReturn даже есть попытка залифтить логику:

```java
public static <T> ExecutionResult<Boolean> handleRunnableAndReturn(Runnable runnable) {

    try {
        runnable.run();
        return ExecutionResult.of(true, null);
    } catch (RuntimeException e) {
        return ExecutionResult.of(false, e);
    } catch (Exception e) {
        return ExecutionResult.of(false, new IllegalStateException(e.getMessage()));
    }
}
```

Только почему-то это происходит очень локально.

Как бы можно было выразительно переписать этот код на Kolin:

```kotlin
fun getUser(request: LoginRequest): Result<User> = getUser(request)
    .andThen(::ensureActiveStatus)
    .andThen(::ensureOnDeleteStatus)
    .andThen(::ensureInvitationStatus)
    .andThen { user -> ensurePasswordMatches(request.password, user) }

private fun getUser(request: LoginRequest): Result<User> = userRepository.findByEmail(request.email).toResult {
    AuthException(INVALID_LOGIN, format(WRONG_EMAIL_MESSAGE, request.email))
}

fun ensureActiveStatus(user: User): User = if (user.isActive) user else throw AuthException(...)
...
```

Вспомогательные методы:

```kotlin
fun <T> Optional<T>.toResult(orElse: () -> Throwable): Result<T> =
    if (isPresent) Result.success(get()) else Result.failure(orElse())

inline fun <A> Result<A>.andThen(f: (A) -> (A)): Result<A> =
    map { f(it) }
```

В вызывающем коде переход от Result к User будет выглядеть так:

```kotlin
val user: User = getUserEntity(request).getOrThrow()
```

# Пример 2

В коде выше используется строковое поле request.email. Лучше привести приходящий адрес к обертке Email и далее использовать:

```kotlin
data class Email(val value: String) { // lift
    companion object {
        fun of(raw: String): Result<Email> =
            runCatching {
                val s = raw.trim().lowercase()
                require(Regex("^[\\w.+-]+@[\\w.-]+$").matches(s)) { "Invalid email" }
                Email(s)
            }
    }
}

val email: String = Email.of("  User@domain.org  ").map { it.value }.getOrThrow() // lower
```

# Пример 3

В одном из участков кода нашел работу с "сырыми" объемами памяти:

```java
public BigDecimal defineTotalKb(RateEntity rateEntity, BigDecimal totalSum, BigDecimal overAll, BigDecimal paymentsCount,
                                int index) {
    var totalKb = ZERO;

    if (rateEntity == null || paymentsCount == null || paymentsCount.compareTo(BigDecimal.ZERO) <= 0) {
        return totalKb.setScale(2, RoundingMode.HALF_UP);
    }
    ...
```

Кажется, что лучше перейти к абстракции File. Приведу упрощенную версию реализации:

```java
final class File {

    static final File EMPTY = new File(0);
    private static final int OUT_SCALE = 2;
    private static final long KIB = 1024L;

    private final byte[] content;
    private final BigDecimal size;
    
    static File ofBytes(@NotNull byte[] content) {
        ...
    }

    public BigDecimal bytes() {
        return size;
    }

    public File plus(File other) {
        return new File(...);
    }

    public List<File> split(@Positive @NotNull Integer parts) {
        ...
    }

    ...
}
```

# Вывод

Что можно сказать по приведенным примерам?

В примерах 1 и 2 получилось больше инкапсулирование логики в рамках пользовательских классов и отказ от использования примитивных типов, чем глубокая проработка абстракции. 

В примере 1 был выделен ряд операций над сущностью, но они достаточно однобоки. Многопланового взаимодействия с сущностью не происходит, что снижает репрезентативность этого примера.

Пример 2 тоже достаточно скромен по причине отсутствия действий над сущностью, но на мой взгял достаточно точен для представления электронной почты и может служить базой для дальнейших расширений.

Тем не менее получить хорошую абстракцию в коде, которая будет отражением реального мира без приведенных выше операций, вряд ли получится.

Пример 3 наиболее близок к идее статьи: мы начинаем оперировать не сырыми байтами, а контентом, заключенным в "файл", который имеет определенный размер.

Поиск возможности внедрения таких абстракций -- важный шаг для того, чтобы строить понятный публичный API.