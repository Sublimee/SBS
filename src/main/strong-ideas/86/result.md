# Пример 1

Есть класс:

```java
class OfferSettingsResponse {
    
    private DealType dealType;
    private OfflineSalesAddressType offlineSalesAddressType;
    private String onlineSalesAddress;
    // другие связанные поля не привожу для простоты
    ...
```

экземпляры которого, очевидно, по-разному заполняются в зависимости от DealType:

```java
enum DealType {

    ONLINE("Онлайн"),
    OFFLINE("Оффлайн"),
    ONLINE_OFFLINE("Онлайн и оффлайн");

    private final String displayName;
}
```

Онлайн-офферу не нужен offlineSalesAddressType. Оффлайн-офферу не нужен onlineSalesAddress.

Что можно сделать? Оставить только нужные поля в зависимости от типа оффера:

```java
sealed interface SalesConfig
permits SalesConfig.Online, SalesConfig.Offline, SalesConfig.OnlineAndOffline {

    @NotNull
    DealType dealType();

    record Online(@NotNull String onlineSalesAddress) implements SalesConfig {
        @Override
        public @NotNull DealType dealType() {return DealType.ONLINE; }
    }

    record Offline(@NotNull OfflineSalesAddressType offlineSalesAddressType) implements SalesConfig {
        @Override
        public @NotNull DealType dealType() {return DealType.OFFLINE; }
    }

    record OnlineAndOffline(@NotNull String onlineSalesAddress,
                            @NotNull OfflineSalesAddressType offlineSalesAddressType) implements SalesConfig {
        @Override
        public @NotNull DealType dealType() {return DealType.ONLINE_OFFLINE; }
    }
}

record OfferSettingsResponse(SalesConfig salesConfig, ...) {

    @JsonProperty("dealType")
    public DealType dealType() {
        return salesConfig.dealType();
    }
    ...
```

Роль ассертов здесь играют аннотации @NotNull.

# Пример 2

```java
class Rate {

    private RateType type;
    private BigDecimal commission;
    private BigDecimal fixedCommission;
    ...
}

enum RateType {

    FIXED("Фиксированный процент"),
    TURNOVER("Процент от оборота");

    private final String displayName;
}
```

Здесь есть проблема в том, что TURNOVER -- не "Процент от оборота", а скорее "Гибкий тариф". В свою очередь FIXED -- это не всегда "Фиксированный процент":
* если используется commission -> фиксированный процент;
* если используется fixedCommission -> фиксированная сумма.

Из-за неоднозначности трактовки FIXED появляются следующие конструкции:

```java
if (rate.getType() == RateType.FIXED) {
    if (rate.getFixedCommission() != null && rate.getFixedCommission().compareTo(ZERO) > 0) {
        ...
    } else {
        ...
    }
}
```

Настраиваем инвариант:

```java
sealed interface RateConfig
        permits RateConfig.FixedPercent, RateConfig.FixedAmount, RateConfig.Turnover {

    @NotNull RateType type();

    record FixedPercent(@NotNull BigDecimal commissionPercent) implements RateConfig {
        @Override
        public @NotNull RateType type() {
            return RateType.FIXED_PERCENT;
        }
    }

    record FixedAmount(@NotNull BigDecimal commissionAmount) implements RateConfig {
        @Override
        public @NotNull RateType type() {
            return RateType.FIXED_AMOUNT;
        }
    }

    record Turnover() implements RateConfig {
        @Override
        public @NotNull RateType type() {
            return RateType.TURNOVER;
        }
    }
}
```

Теперь варианты считываются однозначно. Роль ассертов здесь играют аннотации @NotNull.

# Пример 3

Очевидно, для работы с процентами в прошлом примере плохо подходит BigDecimal. Лучше задать инвариант:

```java
record Percent(BigDecimal value) {

    private static final BigDecimal MIN = new BigDecimal("0.01");
    private static final BigDecimal MAX = new BigDecimal("99.99");

    public Percent {
        if (value == null) {
            throw new IllegalArgumentException("Percent value is null");
        }

        if (value.compareTo(MIN) < 0 || value.compareTo(MAX) > 0) {
            throw new IllegalArgumentException("Percent value must be between %s and %s".formatted(MIN, MAX));
        }
    }

    public BigDecimal asFraction() {
        return value.divide(new BigDecimal("100"), 4, RoundingMode.HALF_UP);
    }
}
```

В таком случае в коде, использующем это значение не придется делать ни лишних if'ов, ни assert'ов.

# Вывод

Приведенные мной примеры удачно уместили корректную логику на уровне самих классов. Собранная в одном месте логика не позволяет появляться разночтениям из-за неправильно заполненных полей. В первых двух примерах я четко задаю иерархии, где экземпляры могут быть настроены однозначно, а в последнем -- избегаю ошибок, связанных с ипользованием сырого, не обремененного теми же assert'ами типа.

assert'ы по моему опыту применяются мало по трем причинам:
1) они находят ошибку только на этапе рантайма, в отличие от, например, тестов (которые в свою очередь тоже используют assert'ы);
2) их нужно ставить в месте использования, коих может быть несколько;
3) если в коде и есть ошибка, то она в рантайме будет сопровождаться исключением и без assert'ов.

В таком случае где assert'ы могут быть полезны? Наверное там, где исключение не выпадет, но код отработает неверно. Такое может произойти, например, при отдаче клиенту ответа для отображения на UI: отрицательная процентная ставка по вкладу отразится тихо, не привлекая внимания разработки).

Но, кажется, что если мы знаем о существовании такой ситуации, то нужно обезопасить себя более продвинутыми техниками, чем assert.