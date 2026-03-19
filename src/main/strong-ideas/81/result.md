# Пример 1

Было:

```java
switch (documentEntity.getStatus()) {
    case NEW -> documentEntity
            .setSum(withDefault(() -> request.getTurnoverSum(), documentEntity.getSum()))
            .setCashback(withDefault(() -> request.getCashback().getSum(), documentEntity.getCashback()))
            .setKbWithVat(withDefault(() -> request.getBankReward().getSum(), documentEntity.getKbWithVat()))
            .setKb(withDefault(() -> request.getBankReward().getSumWithoutVAT(), documentEntity.getKb()))
            .setPartnerOrder(request.getSerialDocNumber())
            .setReportDate(defaultIfNull(request.getDocDate(), documentEntity.getReportDate()))
            .setInvoiceNumber(request.getInvoiceNumber())
            .setInvoiceDate(request.getInvoiceDate());
    case AGREEING -> documentEntity
            .setSum(withDefault(() -> request.getTurnoverSum(), documentEntity.getSum()))
            .setCashback(withDefault(() -> request.getCashback().getSum(), documentEntity.getCashback()))
            .setKbWithVat(withDefault(() -> request.getBankReward().getSum(), documentEntity.getKbWithVat()))
            .setKb(withDefault(() -> request.getBankReward().getSumWithoutVAT(), documentEntity.getKb()))
            .setPartnerOrder(request.getSerialDocNumber())
            .setInvoiceNumber(request.getInvoiceNumber())
            .setInvoiceDate(request.getInvoiceDate())
            .setPartnerSendDate(request.getAgreeingSentDate());
    
    ...
```

Стало:

```java
switch (documentEntity.getStatus()) {
    case NEW -> completeBaseFinancialFields(documentEntity, request)
        .setReportDate(...);

    case AGREEING -> completeBaseFinancialFields(documentEntity, request)
        .setPartnerSendDate(...);

    ...
```

Комментарий: избавляемся от дублирования кода. Один из приемов -- вынести общую логику в отдельный метод. Это позволяет одновременно модифицировать логику во всех местах, где она используется. Такой рефакторинг актуален, и когда код почти похож: мы отделяем общее от различий, что может быть лучше считано глазом разработчика.

# Пример 2

Было:

```java
public ComodClientResponse sendMessage(String token, ComodClientRequest request) {
    var email = request.getContextDto().getMetadataDto().getEventParameterDto()
            .getChannelParameterDto().getEmailDto().getEmail();

    ...
}
```

Стало:

```java
public class ComodClientRequest {
    
    private ContextDto context;

    public String getEmail() {
        return context.getMetadataDto()
                .getEventParameterDto()
                .getChannelParameterDto()
                .getEmailDto()
                .getEmail();
    }
    
    ...
}

...

public ComodClientResponse sendMessage(String token, ComodClientRequest request) {
    var email = request.getEmail();

    ...
}
```

Комментарий: сокращаем знание внешнего кода о внутренней структуре классов за счет того, что избавляемся от MessageChains. Пользователю API (публичных методов класса) не хочется долго с ним разбираться. Под это подпадают, в том числе и длинные цепочки вызовов, которые позволяют достать нужную информацию из недр монструозных объектов. За счёт вынесения отдельных методов, которые закрывают потребность во вполне конкретных бизнес-кейсах, можно сильно сократить и упростить для понимания пользовательский код.

С этим дефектом кода связан принцип Law Of Demeter. В соответствии с ним, если упрощать, объект должен взаимодействовать только с объектами и полями, которые ему доступны и доступны им, т.е. цепочки вида a.getB().getC().getD() недопустимы. Мы не должны запускать свои щупальца через множество объектов, так как код становится сильно связанным. 

# Пример 3

Было:

```java
private static final String NON_DIGIT_REGEX = "\\D";
private static final String RU_COUNTRY_CODE = "7";

public static String toDigitsOnly(String phone) {

    if (isNull(phone)) return null;

    var digits = phone.replaceAll(NON_DIGIT_REGEX, "");

    return digits.isEmpty() ? null : digits;
}

public static String toDigitsOnly11(String phone) {

    if (isNull(phone)) return null;

    var digits = phone.replaceAll(NON_DIGIT_REGEX, "");

    if (digits.length() != 11 || !digits.startsWith(RU_COUNTRY_CODE)) return null;

    return digits;
}

public static String toDigitsOnly10to15(String phone) {

    if (isNull(phone)) return null;

    var digits = phone.replaceAll(NON_DIGIT_REGEX, "");

    if (digits.length() < 10 || digits.length() > 15) return null;

    return digits;
}
```

Стало:

Сначала хотел нормализацию во втором и третьем методах вынести в отдельный метод, но тогда бы в них оставалась двойная ответственность. Пришлось создавать отдельный класс:

```java
public final class Phone {

    private static final String NON_DIGIT_REGEX = "\\D+";
    private static final String RU_COUNTRY_CODE = "7";
    private static final int RU_PHONE_LENGTH = 11;
    private static final int MIN_INTERNATIONAL_PHONE_LENGTH = 10;
    private static final int MAX_INTERNATIONAL_PHONE_LENGTH = 15;

    private final String digits;

    public Phone(String rawPhone) {
        if (rawPhone == null) {
            this.digits = null;
            return;
        }

        String normalized = rawPhone.replaceAll(NON_DIGIT_REGEX, "");
        this.digits = normalized.isEmpty() ? null : normalized;
    }

    public String getDigits() {
        return digits;
    }

    public boolean isEmpty() {
        return digits == null;
    }

    public boolean isNotEmpty() {
        return !isEmpty();
    }

    public boolean isRussian() {
        return isNotEmpty()
                && digits.length() == RU_PHONE_LENGTH
                && digits.startsWith(RU_COUNTRY_CODE);
    }

    public boolean isInternational() {
        return isNotEmpty()
                && digits.length() >= MIN_INTERNATIONAL_PHONE_LENGTH
                && digits.length() <= MAX_INTERNATIONAL_PHONE_LENGTH;
    }

    ...
}

```

Комментарий: добиваемся соблюдения One Responsibility Rule в коде. Даже короткие методы могут брать на себя много ответственности (что уж говорить о длинных). SRP прекрасен тем, что позволяет упрощать логику строительных блоков кода. Это благоприятно влияет на их переиспользование. В примере выше пришлось полностью перестроить код, хотя, если приглядеться, то используются практически те же, но распутанные конструкции.

# Пример 4

Было:

Один класс используется в двух сценариях (экранах), поэтому одно из полей всегда null:

```java
TfaStatusResponse.builder()
    .phone(phoneNumber)
    .maskedPhone(maskedPhone)
    ...
```

Стало:

Разделяем классы для поддержания двух разных сценариев:

```java
InitPhoneResponse.builder()
    .phone(phoneNumber)
    ...    
    
...
        
TfaStatusResponse.builder()
    .maskedPhone(maskedPhone)
    ...
```

Комментарий: опять One Responsibility Rule. Две ответственности могут быть представлены двумя сценариями работы, которые мы хотим покрыть одним и тем же кодом. У нас появляются ветвления, различные флаги и разная логика, чтобы одновременно поддержать каждый из них. Но зачем усложнять код, если можно сделать два простых сценария? Надо будет только аккуратно проработать дублирование логики в каждом схожем сценарии.

# Пример 5

Было:

```java
public abstract class PageTurnerService {

    ...

    public abstract void turnToNextPage(UserEntity userEntity);

    public void turnToPrevious(UserEntity userEntity) {
    }
}
```

и много реализаций, где turnToPrevious оставался с пустой реализацией, так как не поддерживал фичу. Это пример Refused Bequest.

Стало:

Изначально предполагаем, что вернуться к предыдущему шагу в процессе не получится. При необходимости реализуем логику.

```java
public abstract class PageTurnerService {

    ...

    public abstract void turnToNextPage(UserEntity userEntity);
    
    public abstract void turnToPrevious(UserEntity userEntity);
}

```

Комментарий: при организации наследования часто допускаются ошибки. То, о чем нужно помнить -- это соблюдение LSP. Его нарушение можно найти даже в стандартной библиотеке Java в иммутабельных коллекциях. Поведение наследника должно быть предсказуемым: если оно предполагалось в родители или же было в каком-то виде реализовано, то странно его не наблюдать при спуске вниз по иерархии.