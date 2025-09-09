# Пример 1

Рассмотрим процесс логниа пользователя в одном из сервисов:

```java
@RestController
@RequestMapping("v1")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("login")
    public ResponseEntity<TokenResponse> login(
            @RequestHeader(value = "ip", required = false) String ip,
            @RequestHeader(value = "user-agent", required = false) String agent,
            @RequestBody @Valid LoginRequest request
    ) {
        return authService.login(request, ip, agent);
    }
    
    ...
}

@Service
@RequiredArgsConstructor
public class AuthService {
    
    ...
    
    public ResponseEntity<TokenResponse> login(LoginRequest request, String ip, String agent) {

        request.setEmail(request.getEmail().trim().toLowerCase());

        var userEntity = userRepository.findByEmail(request.getEmail())
                .orElseThrow(
                        () -> new AuthException(
                                INVALID_LOGIN,
                                format(WRONG_EMAIL_MESSAGE, request.getEmail())
                        )
                );

        if (isNull(userEntity.getIsActive()) || !userEntity.getIsActive() || nonNull(userEntity.getDeletedAt()))
            throw new AuthException(USER_REMOVED, "user is inactive or deleted");

        checkUserOnDeleteStatus(userEntity);
        checkUserInvitationStatus(userEntity);
        comparePasswords(request.getPassword(), userEntity.getPassword());

        var executionResult = handleRunnableAndReturn(() -> checkPassword(request.getPassword(), TRUE));
        if (!executionResult.getResult() && executionResult.getException() instanceof BadRequestException)
            throw new ForbiddenException(CHANGE_PASSWORD_REQUIRED, "login failed due to weak password");

        var accessTokenKey = generateSecretKey();
        var refreshTokenKey = generateSecretKey();
        var userIdAsString = userEntity.getId().toString();

        var accessToken = generateAccessToken(userIdAsString, accessTokenKey);
        var refreshToken = generateRefreshToken(userIdAsString, refreshTokenKey);

        userEntity.setAccessTokenKey(encodeBase64String(accessTokenKey.getEncoded()));
        userEntity.setRefreshTokenKey(encodeBase64String(refreshTokenKey.getEncoded()));
        userRepository.save(userEntity);

        var cookie = cookieUtil.buildResponseCookie(refreshToken);

        if (allNotNull(ip, agent)) {
            var authorizationLogEntity = buildAuthorizationLog(userEntity.getId(), ip, agent);
            authorizationLogRepository.save(authorizationLogEntity);
        }

        var tokenResponse = TokenResponse.of(userIdAsString, accessToken);

        return ResponseEntity
                .status(OK)
                .header(SET_COOKIE, cookie.toString())
                .body(tokenResponse);
    }
}
```
Какие здесь есть проблемы с точки зрения построения функционального интерфейса?

0) В целом слой контроллера затекает в слой сервиса за счет формирования в нем cookie.

1) Аргумент request изменяется в сервисе. Хуже то, что изменение происходит по причине приходящего, возможно, некорректного состояния, которое приходится корректировать:

```java
    public ResponseEntity<TokenResponse> login(LoginRequest request, String ip, String agent) {
        request.setEmail(request.getEmail().trim().toLowerCase());
```

Что напрашивается? Заменим class на record.

Было:

```java
@Data
public class LoginRequest {

    @NotBlank(message = "EMPTY_EMAIL")
    @Schema(title = "Электронная почта", example = "user@mail.ru")
    private String email;

    @NotBlank(message = "EMPTY_PASSWORD")
    @Schema(title = "Пароль", example = "Pa$$w0rd!")
    private String password;
}

```

Стало:

```java
public record LoginRequest(
        @NotBlank(message = "EMPTY_EMAIL")
        @Schema(title = "Электронная почта", example = "user@mail.ru")
        String email,

        @NotBlank(message = "EMPTY_PASSWORD")
        @Schema(title = "Пароль", example = "Pa$$w0rd!")
        String password) {
    public LoginRequest {
        if (email != null) {
            email = email.trim().toLowerCase();
        }
    }
}
```

Получили неизменяемую структуру без сеттеров, которая уже при конструировании объекта обрабатывает некорректный пользовательский ввод.

2) Также идет работа с БД через репозиторий (side effect):

```java
userRepository.save(userEntity);

...

authorizationLogRepository.save(authorizationLogEntity);
```

===

С учетом выполненного изменения в пункте 1 проведем ряд модификаций исходного кода для разделения контроллера и сервисного слоя:

```java
@RestController
@RequestMapping("v1")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("login")
    public ResponseEntity<TokenResponse> login(
            @RequestHeader(value = "ip", required = false) String ip,
            @RequestHeader(value = "user-agent", required = false) String agent,
            @RequestBody @Valid LoginRequest request
    ) {
        LoginResult loginResult = authService.login(request);
        auditService.audit(loginResult, ip, agent);

        String userId = loginResult.user().getIdAsString();

        String accessToken = generateAccessToken(userId, loginResult.accessToken());
        String refreshToken = generateRefreshToken(userId, loginResult.refreshToken());
        TokenResponse tokenResponse = TokenResponse.of(userId, accessToken);
        String cookie = cookieUtil.buildResponseCookie(refreshToken).toString();

        return ResponseEntity
                .status(OK)
                .header(SET_COOKIE, cookie)
                .body(tokenResponse);
    }
    
    ...
}

@Service
@RequiredArgsConstructor
public class AuthService {
    
    ...

    public LoginResult login(LoginRequest request) {
        UserEntity userEntity = getUserEntity(request);
        validateLoginRequest(request, userEntity);
        SecretKey accessTokenKey = generateSecretKey();
        SecretKey refreshTokenKey = generateSecretKey();

        saveLoggedUser(userEntity, accessTokenKey, refreshTokenKey);

        return new LoginResult(userEntity, accessTokenKey, refreshTokenKey);
    }

    private void saveLoggedUser(UserEntity userEntity, SecretKey accessTokenKey, SecretKey refreshTokenKey) {
        userEntity.setAccessTokenKey(encodeBase64String(accessTokenKey.getEncoded()));
        userEntity.setRefreshTokenKey(encodeBase64String(refreshTokenKey.getEncoded()));
        userRepository.save(userEntity);
    }
    
    ...
}
```

Концептуально теперь прослеживается схема:
получили пользователя (из БД) ->
и провели его валидацию
залогинили пользователя (обновили токены в БД, side effect) ->
выполнили аудит логина (в БД, side effect) ->
вернули аутентификационные данные пользователю

Отразим ее в AuthService:

```java
@Service
@RequiredArgsConstructor
public class AuthService {
    
    ...
    
    public User login(LoginEvent loginEvent) {
        User user = userService.getUser(loginEvent);
        User validatedUser = this.validateUserLogin(user, loginEvent);
        User toLoginUser = this.updateUserKeys(validatedUser);
        User loggedUser = userService.saveUser(toLoginUser);
        return loggedUser;
    }

    ...
}
```

И переложим в AuthController, избавившись от login в AuthService:

```java
@RestController
@RequestMapping("v1")
@RequiredArgsConstructor
public class AuthController {

    private final UserService userService;
    private final AuthService authService;
    private final AuditService auditService;
    
    @PostMapping("login")
    public ResponseEntity<TokenResponse> login(
            @RequestHeader(value = "ip", required = false) String ip,
            @RequestHeader(value = "user-agent", required = false) String agent,
            @RequestBody @Valid LoginRequest loginRequest
    ) {
        // main logic
        User user = userService.getUser(loginEvent.getEmail());
        User validatedUser = authService.validateUserRequest(user, loginRequest);
        User toLoginUser = authService.setUserKeys(validatedUser);
        User loggedUser = userService.saveUser(toLoginUser); // side effect
        
        // crosscutting logic
        auditService.audit(loggedUser, ip, agent); // side effect
        
        // building response (получилось объемно, в дальнейшем лучше скрыть сложность)
        String userId = loggedUser.getIdAsString();
        String accessToken = generateAccessToken(userId, loginResult.accessToken());
        String refreshToken = generateRefreshToken(userId, loginResult.refreshToken());
        TokenResponse tokenResponse = TokenResponse.of(userId, accessToken);
        String cookie = cookieUtil.buildResponseCookie(refreshToken).toString();

        return ResponseEntity
                .status(OK)
                .header(SET_COOKIE, cookie)
                .body(tokenResponse);
    }
    
    ...
}

@Service
@RequiredArgsConstructor
public class AuthService {
    
    ...

    public User setUserKeys(@NotNull User user) {
        var accessTokenKey = generateSecretKey();
        var refreshTokenKey = generateSecretKey();
        return user.withAccessTokenKey(accessTokenKey).withRefreshTokenKey(refreshTokenKey);
    }
}
```

# Пример 2

В том же проекте по проторенной дорожке проведем аналогичную процедуру с разлогиниванием пользователя. Было:

```java
@RestController
@RequestMapping("v1")
@RequiredArgsConstructor
public class AuthController {

    ...

    @PostMapping("logout")
    @ResponseStatus(NO_CONTENT)
    public ResponseEntity<Void> logout(
            @RequestHeader(AUTHORIZATION) String accessToken,
            @RequestHeader(value = USER_ID_HEADER) UUID userId
    ) {
        return authService.logout(accessToken, userId);
    }
    
    ...
}

@Service
@RequiredArgsConstructor
public class AuthService {
    
    ...

    public ResponseEntity<Void> logout(String accessToken, UUID userId) {

        var userEntity = checkAccessTokenAndReturnUser(accessToken, userId);
        userEntity.setAccessTokenKey(null);
        userEntity.setRefreshTokenKey(null);

        userRepository.save(userEntity);

        var cookie = cookieUtil.buildResponseCookie("", 0);

        return ResponseEntity
                .status(OK)
                .header(SET_COOKIE, cookie.toString())
                .build();
    }
}
```

Стало:

```java
@RestController
@RequestMapping("v1")
@RequiredArgsConstructor
public class AuthController {
    
    private final UserService userService;
    private final AuthService authService;
    private final AuditService auditService;

    @PostMapping("logout")
    @ResponseStatus(NO_CONTENT)
    public ResponseEntity<Void> logout(
            @RequestHeader(AUTHORIZATION) String accessToken,
            @RequestHeader(value = USER_ID_HEADER) UUID userId
    ) {
        // main logic
        User user = userService.getUser(userId);
        User validatedUser = authService.validateUserRequest(user, accessToken);
        User toLogoutUser = authService.clearUserKeys(validatedUser);
        User loggedOutUser = userService.saveUser(toLogoutUser); // side effect

        var cookie = cookieUtil.buildResponseCookie("", 0);

        return ResponseEntity
                .status(OK)
                .header(SET_COOKIE, cookie.toString())
                .build();
    }
    
    ...
}

@Service
@RequiredArgsConstructor
public class AuthService {
    
    ...

    public User clearUserKeys(@NotNull User user) {
        return user.withAccessTokenKey(null).withRefreshTokenKey(null);
    }
}
```

# Пример 3

```java
@RestController
@RequestMapping("v1")
@RequiredArgsConstructor
public class AuthController {

    ...

    @PostMapping("reset-password")
    @ResponseStatus(NO_CONTENT)
    public void resetPassword(
            @RequestBody @Valid ResetPasswordRequest request
    ) {
        authService.resetPassword(request);
    }
    
    ...
}

@Service
@RequiredArgsConstructor
public class AuthService {
    
    ...

    public void resetPassword(ResetPasswordRequest request) {

        request.setEmail(request.getEmail().trim().toLowerCase());

        var userEntityOptional = userRepository.findByEmailAndDeletedAtIsNull(request.getEmail());

        if (userEntityOptional.isEmpty()) return;
        var userEntity = userEntityOptional.get();

        var verificationToken = generateVerificationToken();
        var dateTimePart = encrypt(now().format(ofPattern(DATE_TIME_PATTERN)), verificationToken);
        var emailPart = encrypt(request.getEmail(), verificationToken);

        var finalVerificationToken = verificationToken
                .concat(dateTimePart)
                .concat(DELIMITER)
                .concat(emailPart);

        var encodedVerificationToken = encodeBase64URLSafeString(finalVerificationToken.getBytes(UTF_8));

        var resetPasswordCacheDto = ResetPasswordCacheDto.of(encodedVerificationToken);
        cacheService.save(userEntity.getEmail(), resetPasswordCacheDto, 300);

        notificationService.sendResetPasswordMail(userEntity.getEmail(), encodedVerificationToken);
    }
}

```

request.setEmail(request.getEmail().trim().toLowerCase()); мы уже видели. ResetPasswordRequest нужно перевести в record по аналогии с LoginRequest.

Увидев знакомое userRepository.findByEmailAndDeletedAtIsNull(request.getEmail()); хочется провести рефакторинг метода валидации пользователя, но оставим его за скобками ввиду отсутствия side-effect'ов.

```java
@RestController
@RequestMapping("v1")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;
    ...

    @PostMapping("reset-password")
    @ResponseStatus(NO_CONTENT)
    public void resetPassword(
            @RequestBody @Valid ResetPasswordRequest resetPasswordRequest
    ) {
        User user = userService.getUser(resetPasswordRequest.getEmail());
        User validatedUser = authService.validateUserRequest(user, resetPasswordRequest);
        VerifiationToken verificationToken = authService.generateVerificationToken(validatedUser);
        cacheService.save(validatedUser, verificationToken, 300); // side-effect
        notificationService.sendResetPasswordMail(validatedUser, verificationToken); // side-effect
    }
    
    ...
}

@Service
@RequiredArgsConstructor
public class AuthService {
    
    ...

    public void generateVerificationToken(@NotNull User user) {
        String verificationToken = generateVerificationToken();
        String dateTimePart = encrypt(now().format(ofPattern(DATE_TIME_PATTERN)), verificationToken);
        String emailPart = encrypt(request.getEmail(), verificationToken);

        String finalVerificationToken = verificationToken
                .concat(dateTimePart)
                .concat(DELIMITER)
                .concat(emailPart);

        return encodeBase64URLSafeString(finalVerificationToken.getBytes(UTF_8));
    }
}

```

# Вывод

Что получилось?
1) AuthService получил чисто функциональный интерфейс без side effect'ов;
2) все side effect'ы остались AuditService и UserService, которые работают с БД.

В целом такой рефакторинг произошел преимущественно за счет отказа от тонкого контроллера. Вместо тонкого контроллера мог использоваться какой-то промежуточный сервис, который бы вызывался контроллером. Но зачем?)

Когда-то уже было задание по отказу от тонкого контроллера. Теперь то задание заиграло новыми красками. Если перенести в контроллер логику вызываемого им метода, то появляется больше гибкости в проектировании приложения.

Определенные сервисы, которые наделены сложной логикой, желательно отделить от side-effect'ов. Таким образом каждый из этих двух набороов получившихся сервисов станет проще тестировать и в целом поддерживать.