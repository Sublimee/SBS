**Пример 1**

В наших проектах есть старые юнит-тесты, которые представляют собой смесь юнит- и интеграционных тестов:

```kotlin
@Autowired
lateinit var bonusService: BonusService

@Autowired
lateinit var featureToggleApiClient: FeatureToggleApiClient

fun `must return bonus list for unified loyalty client`(): Unit = runBlocking {
    stubForFeatureToggleApi("unified-loyalty-client-features.json")

    val bonuses = bonusService.getBonuses(
        accounts = bonusAccounts(),
        isKids = true,
        headers = ANDROID_HEADERS,
    )

    assertThat(bonuses).isNotEmpty()
}
```

Как мне кажется, они были написаны так по двум причинам:
1) непонимание, что в юнит-тестах в большинстве случаев не требуется поднимать контекст
2) лень, вследствие которой использовался WireMockServer для того, чтобы задать мок (удобнее прописать возвращаемое значение в файле, а не конструктором в коде)

WireMockServer по названию тоже мок, да не тот). Тест выше приводит к тому, что при тестировании BonusService совершался сетевой вызов из экземпляра FeatureToggleApiClient, что не должно быть частью юнит-тестирования BonusService. Тест нужно переписать так:

```kotlin
@MockBean
lateinit var featureToggleApiClient: FeatureToggleApiClient

@InjectMocks
lateinit var bonusService: BonusService

@Test
fun `must return bonus list for unified loyalty client`(): Unit = runBlocking {
    whenever(featureToggleApiClient.get(any(), any(), any()))
        .thenReturn(Mono.just(FeaturesDTO(...))) // объемный конструктор

    val bonuses = bonusService.getBonuses(
        accounts = bonusAccounts(),
        isKids = true,
        headers = ANDROID_HEADERS,
    )

    assertThat(bonuses).isNotEmpty()
}
```

Если ответ мока предполагается большим, то можно либо считать его из файла, либо не задавать его полностью, воспользовавшись возможностями библиотеки, например val featureToggleApiResponse : FeaturesDTO = mock().

**Пример 2**

Пример аналогичный первому:

```kotlin
@Autowired
lateinit var loyaltyPromotedCashbackProxy: LoyaltyPromotedCashbackProxy

@Autowired
lateinit var promotedCashbackService: PromotedCashbackService

@Test
fun `must return null for non kid due to promoted cashback unavailable`(): Unit = runBlocking {
    stubForLoyaltyPromotedCashbackProxy("promoted-cashback-not-available.json")

    val actual = promotedCashbackService.getPrograms(BaseIntegrationTest.HEADERS, BOOMERANG_BONUS_ACCOUNT_TYPE_ID)
    Assertions.assertNull(actual)
}
```

```kotlin
@MockBean
lateinit var loyaltyPromotedCashbackProxy: LoyaltyPromotedCashbackProxy

@InjectMocks
lateinit var promotedCashbackService: PromotedCashbackService

@Test
fun `must return null for non kid due to promoted cashback unavailable`(): Unit = runBlocking {
    whenever(loyaltyPromotedCashbackProxy.getAvailabilityResponse(...))
        .thenReturn(PromotedCashbackAvailabilityResponse.builder().isAvailable(false).build())

    val actual = promotedCashbackService.getPrograms(BaseIntegrationTest.HEADERS, BOOMERANG_BONUS_ACCOUNT_TYPE_ID)
    Assertions.assertNull(actual)
}
```

Стоит отметить, что точно так же, как в юнит-тестах нужно избегать интеграционную составляющую, в интеграционных тестах нужно избегать использования моков.

**Пример 3**

```java
@Test
public void testSmtpSend(String[] args) {
    SmtpClient smtpClient = new SmtpClient("smtp.test.ru", 1025);
    smtpClient.connect();
    smtpClient.sendEmail("from@test.ru", "to@test.ru", "Тема письма", "Текст письма");
    smtpClient.close();
}
```

Этот интеграционный тест в принципе не содержит никаких assert'ов. Ну ок). Что он делает? Проверяет взаимодействие нашей библиотеки с удаленным SMTP-сервером. 

Чем такой тест плох?

* Зависимость от внешнего окружения (его сетевой доступности, корректной работы и особенностей работы конкретной версии)

* Увеличенное время исполнения (должны брать в расчет сеть и возможные таймауты)

* Проверка не абстрактного эффекта (сам факт отправки письма), а конкретной физической реализации (работы с конкретным SMTP-клиентом)

Хотя сам по себе тест концептуально хорош, но он не должен быть частью тестов проекта, так как оказывает влияние:

* на время каждого прогона тестов

* на успешность процесса сборки артефакта

Перепишем тест:

```java

@Testcontainers
public class SmtpIntegrationTest {

    public static final String SUBJECT = "Тема письма";
    public static final String CONTENT = "Текст письма";

    @Test
    public void testSmtpSend() throws Exception {
        try (GenericContainer<?> mailhog = new GenericContainer<>(DockerImageName.parse("mailhog/mailhog:v1.0.1"))
                .withExposedPorts(1025, 8025)) {
            mailhog.start();

            SmtpClient smtpClient = new SmtpClient(mailhog.getHost(), mailhog.getMappedPort(1025));
            smtpClient.connect();
            smtpClient.sendEmail("from@test.ru", "to@test.ru", SUBJECT, CONTENT);
            smtpClient.close();

            String mailhogApiUrl = "http://" + mailhog.getHost() + ":" + mailhog.getMappedPort(8025) + "/api/v2/messages";
            String response = new String(new URL(mailhogApiUrl).openStream().readAllBytes());

            assertTrue(isContains(response, SUBJECT), "Письмо не содержит ожидаемую тему");
            assertTrue(isContains(response, CONTENT), "Письмо не содержит ожидаемый текст");
        }
    }

    private static boolean isContains(String testee, String sample) {
        return testee.contains(Base64.getEncoder().encodeToString(sample.getBytes()));
    }
}
```

Мы развязались от внешнего окружения (используем Testcontainers): теперь только мы отвечаем за сетевую доступность, настройку сервера и адаптацию под него клиента. Можно ли было использовать моки? Так как в тесте проверяется работа клиента, то -- нет. Если бы мы писали тест для сервиса, который использует SmtpClient, то мокирование -- подходящий вариант.

**Пример 4**

```java

class LdapServiceTest{
    
    @Test
    public void searchUsersTest(String[] args) {
        Properties env = new Properties();
        env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
        env.put(Context.PROVIDER_URL, ...);
        env.put(Context.PROVIDER_URL, "ldap://ldap.test.ru:389...");
        // и другие настройки тестового сервера ... 
        LdapService ldapService = new LdapService(env);
        List<String> users = ldapService.searchUsers();
        
        assertEquals(2, users.size());
        assertEquals("cn=user1,dc=example,dc=com", users.get(0));
        assertEquals("cn=user2,dc=example,dc=com", users.get(1));
    }
    
    // ...
}

```

К этому тесту те же вопросы, что и в Примере 3. Перепишем его:

```java
@Testcontainers
public class LdapServiceTest {
    
    private LdapService ldapService;

    @Container
    private static final GenericContainer<?> ldapContainer =
            new GenericContainer<>("osixia/openldap:1.5.0")
                    .withExposedPorts(389)
                    .withEnv(...)

    @BeforeAll
    static void setUp() {
        String host = ldapContainer.getHost();
        int port = ldapContainer.getMappedPort(389);
        String ldapUrl = "ldap://" + ldapHost + ":" + ldapPort;

        Properties env = new Properties();
        env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
        env.put(Context.PROVIDER_URL, ...);
        // и другие настройки тестового сервера ...

        ldapService = new LdapService(env);
        ldapService.addUser(// ...);
        ldapService.addUser(// ...);
    }
    
    @Test
    public void searchUsersTest() throws Exception {
        List<String> users = ldapService.searchUsers();

        assertEquals(2, users.size());
        assertEquals(/*...*/, users.get(0));
        assertEquals(/*...*/, users.get(1));
    }
}
```

**Пример 5**

В тесте ниже проверяется работа UnifiedBonusAccountService.

```java
class UnifiedBonusAccountServiceTest {

    // ...

    @MockBean
    lateinit var uwsCustomerInfoClient: CustomerInfoClient
    
    @MockBean
    lateinit var featureToggleApiClient: FeatureToggleApiClient

    @Autowired
    lateinit var applicationVersionConverter: ApplicationVersionConverter

    @Autowired
    lateinit var unifiedBonusAccountService: UnifiedBonusAccountService
    
    @ParameterizedTest(...)
    @CsvSource(
         "bank://longread?endpoint=/v1/travel/|IOS|12.9",
            ...
    )
    suspend fun `must successfully build spend button due to vary clients`(deeplink: String?, os: OperationSystem?, appVersion: String?) {
        whenever(featureToggleApiClient.get(...)
            .thenReturn(...)
        whenever(uwsCustomerInfoClient.getBonusAccountList(...))
            .thenReturn(...)

        val response = unifiedBonusAccountService.getUnifiedBonusAccountResponse(
            Headers.builder()
                .userId(USER_ID)
                .channelId(MOBILE_CHANNEL)
                .os(os)
                .appVersion(version?.let { applicationVersionConverter.convert(it) })
                .build()
        )

        Assertions.assertEquals(
            SpendButton(
                deepLink = deeplink,
            ),
            response.spendButton
        )
    }

    // ...
}
```

Мы видим, что не все бины помечены аннотацией @MockBean. ApplicationVersionConverter выбивается из общей массы. Почему так было сделано? Автор теста решил, что будет удобно заинжектить конвертер, который будет использоваться для конвертации версии приложения из строки в экземпляр AppVersion. Выглядит логично: нам не придется переизобретать свою логику, она уже написана и лежит в библиотеке. Однако тест пополнился дополнительной зависимостью и мы стали завязаны на его реализацию. Лучше было использовать аннотацию @MethodSource, чтобы избавиться от зависимости от реализации ApplicationVersionConverter:

```java
class UnifiedBonusAccountServiceTest {

    // ...

    @MockBean
    lateinit var uwsCustomerInfoClient: CustomerInfoClient

    @MockBean
    lateinit var featureToggleApiClient: FeatureToggleApiClient

    @Autowired
    lateinit var unifiedBonusAccountService: UnifiedBonusAccountService

    @ParameterizedTest
    @MethodSource("spendButtonTestData")
    fun `must successfully build spend button due to vary clients`(deeplink: String?, os: OperationSystem?, appVersion: AppVersion?) = runBlocking {
        whenever(featureToggleApiClient.get(...))
            .thenReturn(...)
        whenever(uwsCustomerInfoClient.getBonusAccountList(...))
            .thenReturn(...)

        val response = unifiedBonusAccountService.getUnifiedBonusAccountResponse(
            Headers.builder()
                .userId(USER_ID)
                .channelId(MOBILE_CHANNEL)
                .os(os)
                .appVersion(appVersion)
                .build()
        )

        assertEquals(
            SpendButton(     
                deepLink = deeplink,
            ),
            response.spendButton
        )
    }

    // ...

    companion object {
        @JvmStatic
        fun spendButtonTestData(): Stream<Array<Any?>> {
            return Stream.of(
                    arrayOf("bank://longread?endpoint=/v1/travel/", OperationSystem.IOS, AppVersion.builder().major(12).minor(9).build()),
                    ...
                    )
            )
        }
    }
}
```


**Вывод**

Моки очень хороши для юнит-тестов. Хотим проверить работу определенного класса? Мокируем его зависимости и проверяем изолированно от остальной кодовой базы. Таких юнит-тестов можно написать много, они просто поддерживаются и быстро выполняются. Понятное дело, что контроллеры, например, тестировать таким образом нецелесообразно:

```kotlin
@GetMapping
suspend fun getInternalBonusAccounts(
    @MandatoryHeadersConstraint(userId = true) headers: Headers,
): List<InternalBonusAccount> = internalBonusAccountService.getInternalBonusAccounts(headers)
```

Для этого лучше подойдут интеграционные тесты: как раз проверим пользовательские сценарии и сериализацию/десериализацию. Исправленные примеры 3 и 4 показывают их уместность. Их исходные варианты, как я уже упоминал, тоже имеют место, но должны запускаться в рамках автотестов за пределами кодовой базы приложения.

Вообще тема тестирования абстрактных эффектов для джависта -- норма и, как мне кажется, не вызывает вопросов. На это указывает, в том числе, и устоявшиеся стандарты используемых библиотек в Java и Kotlin, которые не отличаются большим разнообразием.