# Примеры рефакторинга (в соответствующих папках на уровне с этим файлом)

## Пример 1

* Убрал nullable переменную progress
* Блоки кода, повышающие ЦС, вынес в методы
* Удалил блок else при проверке loyaltyKey

<details>
<summary>Before</summary>

```
@Service
@RequiredArgsConstructor
@Slf4j
public class CardCashbackTariffConverter {

    private static final String NULL_AS_TEXT = "null";

    private final ActivityService activityService;
    private final LoyaltyPromotedCashbackService loyaltyPromotedCashbackService;

    public CashbackConditions getCashbackConditions(Headers headers, CardDTO card, LoyaltyCardInfo loyaltyCardInfo) {
        int rulesId = loyaltyCardInfo.getRulesId() != null ? loyaltyCardInfo.getRulesId() : -1;

        LoyaltyConditionsResponse loyaltyConditionsResponse = getLoyaltyConditions(headers, rulesId);
        List<CardContentDTO> cardCashbackLevels = getCardCashbackLevels(card, loyaltyConditionsResponse);
        List<CardSectionDetailsDTO> cardSectionDetailsDTOList = getCardSectionDetailsDTOList(loyaltyConditionsResponse, card);

        if (CollectionUtils.isEmpty(cardCashbackLevels) && CollectionUtils.isEmpty(cardSectionDetailsDTOList)) {
            throw BusinessException.of(WRONG_SERVICE_PACKAGE);
        }

        BigDecimal progress = null;
        List<CardContentDTO> appliedCardCashbackLevel;
        List<String> loyaltyKeys = loyaltyConditionsResponse.getLoyaltyKeys();
        if (loyaltyKeys == null) {
            appliedCardCashbackLevel = cardCashbackLevels;
        } else {
            List<Activity> activities = activityService.getActivities(headers, loyaltyKeys.get(0));
            if (CollectionUtils.isEmpty(activities)) {
                throw BusinessException.of(ACTIVITIES_NOT_FOUND);
            }
            progress = getProgress(activities);
            Integer levelValue = getLevelValue(activities);
            appliedCardCashbackLevel = getAppliedCardCashbackLevel(levelValue, cardCashbackLevels);
        }

        return CashbackConditions.builder()
                .cardId(card.getId())
                .rulesId(rulesId)
                .loyaltyKey(loyaltyKeys != null ? loyaltyKeys.get(0) : null)
                .servicePackage(card.getServicePackage())
                .appliedCardCashbackLevel(appliedCardCashbackLevel)
                .cardCashbackLevels(cardCashbackLevels)
                .cardDetailsList(cardSectionDetailsDTOList)
                .rulesIdContent(loyaltyConditionsResponse.getRulesIdContentList())
                .progress(progress)
                .maxCategoricalCashbackPercentRate(loyaltyPromotedCashbackService.getMaxCategoricalCashbackPercentRate(headers))
                .customerTitle(
                        loyaltyCardInfo.getDefaultCardName() != null
                                && !loyaltyCardInfo.getDefaultCardName().equals(NULL_AS_TEXT)
                                ? loyaltyCardInfo.getDefaultCardName()
                                : card.getCustomerTitle())
                .build();
    }
}
```

</details>

<details>
<summary>After</summary>

```
@Service
@RequiredArgsConstructor
@Slf4j
public class CardCashbackTariffConverter {

    private static final String NULL_AS_TEXT = "null";

    private final ActivityService activityService;
    private final LoyaltyPromotedCashbackService loyaltyPromotedCashbackService;

    public CashbackConditions getCashbackConditions(Headers headers, CardDTO card, LoyaltyCardTerms loyaltyCardTerms) {
        int rulesId = loyaltyCardTerms.getRulesId() != null ? loyaltyCardTerms.getRulesId() : -1;

        LoyaltyConditionsResponse loyaltyConditionsResponse = getLoyaltyConditions(headers, rulesId);
        List<CardContentDTO> cardCashbackLevels = getCardCashbackLevels(card, loyaltyConditionsResponse);
        List<CardSectionDetailsDTO> cardSectionDetailsDTOList = getCardSectionDetailsDTOList(loyaltyConditionsResponse, card);
        checkServicePackage(cardCashbackLevels, cardSectionDetailsDTOList)

        CashbackConditions.CashbackConditionsBuilder cashbackConditionsBuilder = CashbackConditions.builder()
                .cardId(card.getId())
                .rulesId(rulesId)
                .servicePackage(card.getServicePackage())
                .cardCashbackLevels(cardCashbackLevels)
                .cardDetailsList(cardSectionDetailsDTOList)
                .rulesIdContent(loyaltyConditionsResponse.getRulesIdContentList())
                .maxCategoricalCashbackPercentRate(loyaltyPromotedCashbackService.getMaxCategoricalCashbackPercentRate(headers))
                .customerTitle(getCustomerCardTitle(card, loyaltyCardTerms));
        String loyaltyKey = loyaltyConditionsResponse.getLoyaltyKey();

        if (loyaltyKey == null) {
            return cashbackConditionsBuilder
                    .appliedCardCashbackLevel(cardCashbackLevels)
                    .build();
        }

        List<Activity> activities = getActivities(headers, loyaltyKey);
        return cashbackConditionsBuilder
                .loyaltyKey(loyaltyKey)
                .appliedCardCashbackLevel(getAppliedCardCashbackLevel(getLevelValue(activities), cardCashbackLevels))
                .progress(getProgress(activities))
                .build();
    }

    private checkServicePackage(List<CardContentDTO> cardCashbackLevels, List<CardSectionDetailsDTO> cardSectionDetailsDTOList) {
        if (CollectionUtils.isEmpty(cardCashbackLevels) && CollectionUtils.isEmpty(cardSectionDetailsDTOList)) {
            throw BusinessException.of(WRONG_SERVICE_PACKAGE);
        }
    }

    private List<Activity> getActivities(Headers headers, String loyaltyKey) {
        List<Activity> activities = activityService.getActivities(headers, loyaltyKey);
        if (CollectionUtils.isEmpty(activities)) {
            throw BusinessException.of(ACTIVITIES_NOT_FOUND);
        }
        return activities;
    }

    private String getCustomerCardTitle(CardDTO card, LoyaltyCardTerms loyaltyCardTerms) {
        return loyaltyCardTerms.getDefaultCardName() != null
                && !loyaltyCardTerms.getDefaultCardName().equals(NULL_AS_TEXT)
                ? loyaltyCardTerms.getDefaultCardName()
                : card.getCustomerTitle();
    }
}

```

</details>

## Пример 2

* Заменил цикл for на Stream
* Избавился от вложенных if и else

<details>
<summary>Before</summary>

```

@Service
@RequiredArgsConstructor
public class WithdrawalFeeProcessor {

    private final FeeProcessorProperties withdrawalProps;
    private final TariffValueFieldConverter tariffValueFieldConverter;

    public List<ValueField> process(List<ServiceFee> fees, String channelId) {
        ServiceFee withdrawOtherATMFee = null;
        ServiceFee withdrawOurATMFee = null;

        for (ServiceFee fee : fees) {
            if (withdrawalProps.getWithdrawal().getWithdrawalOtherATMFeeName().equals(fee.getCode())) {
                withdrawOtherATMFee = fee;
            } else if (withdrawalProps.getWithdrawal().getWithdrawalOurATMFeeName().equals(fee.getCode())) {
                withdrawOurATMFee = fee;
            }
        }

        if (withdrawOtherATMFee == null || withdrawOurATMFee == null) {
            return Collections.emptyList();
        } else {
            Optional<FeeThreshold> otherATMPaidThreshold = of(withdrawOtherATMFee).flatMap(ServiceFee::getMinimalPaidThreshold);
            Optional<FeeThreshold> ourATMPaidThreshold = of(withdrawOurATMFee).flatMap(ServiceFee::getMinimalPaidThreshold);

            if (otherATMPaidThreshold.isEmpty() && ourATMPaidThreshold.isEmpty()) {
                return Collections.emptyList();
            } else {
                List<ValueField> result = new ArrayList<>();

                result.add(HeaderField.builder()
                        .label(getHeaderLabelByChannelId(withdrawalProps.getWithdrawal().getHeaderLabel(), channelId))
                        .value(createWithdrawalInfo(withdrawOtherATMFee, withdrawOurATMFee))
                        .build());

                ourATMPaidThreshold.ifPresent(feeThreshold ->
                        result.add(tariffValueFieldConverter.toValueField(feeThreshold.getTariff(),
                                withdrawalProps.getWithdrawal().getOwnATMLabel())));

                otherATMPaidThreshold.ifPresent(feeThreshold ->
                        result.add(tariffValueFieldConverter.toValueField(feeThreshold.getTariff(),
                                withdrawalProps.getWithdrawal().getOtherATMLabel())));

                return result;
            }
        }
    }

    private String createWithdrawalInfo(ServiceFee withdrawOtherATMFee, ServiceFee withdrawOurATMFee) {
        BigDecimal otherATMFreeWithdrawal = withdrawOtherATMFee.getFreeThreshold().map(FeeThreshold::getUpperLimit).orElse(null);
        BigDecimal ourATMFreeWithdrawal = withdrawOurATMFee.getFreeThreshold().map(FeeThreshold::getUpperLimit).orElse(null);

        if (otherATMFreeWithdrawal != null && ourATMFreeWithdrawal != null && otherATMFreeWithdrawal.compareTo(ourATMFreeWithdrawal) == 0) {
            String withdrawalInfoPattern = withdrawalProps.getWithdrawal().getFreeWithdrawalTextPattern();
            return String.format(withdrawalInfoPattern, TariffUtils.formatMoneyValue(ourATMFreeWithdrawal));
        }

        return null;
    }
}


```

</details>


<details>
<summary>After</summary>

```

@Service
@RequiredArgsConstructor
public class WithdrawalFeeProcessor {

    private final FeeProcessorProperties withdrawalProps;
    private final TariffValueFieldConverter tariffValueFieldConverter;

    public List<ValueField> process(List<ServiceFee> fees, String channelId) {
        Optional<ServiceFee> withdrawOtherATMFee = getWithdrawATMFee(fees, withdrawalProps.getWithdrawal().getWithdrawalOtherATMFeeName());
        Optional<ServiceFee> withdrawOurATMFee = getWithdrawATMFee(fees, withdrawalProps.getWithdrawal().getWithdrawalOurATMFeeName());

        if (withdrawOtherATMFee.isEmpty() || withdrawOurATMFee.isEmpty()) {
            return Collections.emptyList();
        }

        Optional<FeeThreshold> otherATMPaidThreshold = withdrawOtherATMFee.flatMap(ServiceFee::getMinimalPaidThreshold);
        Optional<FeeThreshold> ourATMPaidThreshold = withdrawOurATMFee.flatMap(ServiceFee::getMinimalPaidThreshold);

        if (otherATMPaidThreshold.isEmpty() && ourATMPaidThreshold.isEmpty()) {
            return Collections.emptyList();
        }

        List<ValueField> result = new ArrayList<>();

        result.add(HeaderField.builder()
                .label(getHeaderLabelByChannelId(withdrawalProps.getWithdrawal().getHeaderLabel(), channelId))
                .value(getWithdrawalInfo(withdrawOtherATMFee, withdrawOurATMFee))
                .build());

        ourATMPaidThreshold.ifPresent(feeThreshold ->
                result.add(tariffValueFieldConverter.toValueField(feeThreshold.getTariff(),
                        withdrawalProps.getWithdrawal().getOwnATMLabel())));

        otherATMPaidThreshold.ifPresent(feeThreshold ->
                result.add(tariffValueFieldConverter.toValueField(feeThreshold.getTariff(),
                        withdrawalProps.getWithdrawal().getOtherATMLabel())));

        return result;
    }

    private Optional<ServiceFee> getWithdrawATMFee(List<ServiceFee> fees, String name) {
        return fees.stream()
                .filter(it -> name.equals(it.getCode()))
                .findFirst();
    }

    private String getWithdrawalInfo(Optional<ServiceFee> withdrawOtherATMFee, Optional<ServiceFee> withdrawOurATMFee) {
        Optional<BigDecimal> otherATMFreeWithdrawal = getAtmFreeWithdrawal(withdrawOtherATMFee);
        Optional<BigDecimal> ourATMFreeWithdrawal = getAtmFreeWithdrawal(withdrawOurATMFee);

        if (otherATMFreeWithdrawal.isPresent() && ourATMFreeWithdrawal.isPresent() && otherATMFreeWithdrawal.equals(ourATMFreeWithdrawal)) {
            String withdrawalInfoPattern = withdrawalProps.getWithdrawal().getFreeWithdrawalTextPattern();
            return String.format(withdrawalInfoPattern, TariffUtils.formatMoneyValue(ourATMFreeWithdrawal.get()));
        }

        return null;
    }

    @NotNull
    private Optional<BigDecimal> getAtmFreeWithdrawal(Optional<ServiceFee> withdrawOtherATMFee) {
        return withdrawOtherATMFee.flatMap(serviceFee -> serviceFee.getFreeThreshold().map(FeeThreshold::getUpperLimit));
    }
}


```

</details>


## Пример 3

* Заменил цикл for на Stream
* Избавился от вложенных if и else
* Заменил if на Optional
* Блоки кода, повышающие ЦС, вынес в методы

<details>
<summary>Before</summary>

```
@Component
@RequiredArgsConstructor
public class CardServiceFeeExtractor {

    private final ConditionsProperties conditionsProperties;

    public CardServiceFee getCardServiceFee(CardDTO cardDTO, List<TariffEntity> tariffs) {
        var codesFromProperties = conditionsProperties.getCommissionCodes();

        Set<String> commissionCodes = new HashSet<>();
        for (TariffEntity tariff : tariffs) {
            String code = tariff.getCommissionCode();
            if (codesFromProperties.getServiceMonthly().equals(code) || codesFromProperties.getServiceYearly().equals(code)) {
                commissionCodes.add(code);
            }
        }

        if (commissionCodes.size() != 1) {
            throw BusinessException.of(TARIFF_NOT_FOUND);
        }

        String commissionCode = commissionCodes.iterator().next();

        List<TariffEntity> filteredByCommissionCodes = filterCommissionCodes(tariffs, commissionCode);

        boolean isComboCard = false;
        if (cardDTO.getComboData() != null) {
            isComboCard = cardDTO.getComboData().getComboMode() != null;
        }
        TariffValue tariffValue;
        if (isComboCard) {
            tariffValue = getSalaryCardFee(cardDTO, filteredByCommissionCodes);
        } else {
            tariffValue = getRegularCardFee(cardDTO, filteredByCommissionCodes);
        }

        return new CardServiceFee(new BigDecimal(tariffValue.getValue()));
    }
}

```

</details>


<details>
<summary>After</summary>

```

@Component
@RequiredArgsConstructor
public class CardServiceFeeExtractor {

    private final ConditionsProperties conditionsProperties;

    public CardServiceFee getCardServiceFee(CardDTO cardDTO, List<TariffEntity> tariffs) {
        String commissionCode = getCommissionCode(tariffs);
        List<TariffEntity> filteredByCommissionCodes = filterCommissionCodes(tariffs, commissionCode);

        boolean isComboCard = isComboCard(cardDTO);
        TariffValue tariffValue = isComboCard
                ? getSalaryCardFee(cardDTO, filteredByCommissionCodes)
                : getRegularCardFee(cardDTO, filteredByCommissionCodes);

        return new CardServiceFee(new BigDecimal(tariffValue.getValue()));
    }

    private String getCommissionCode(List<TariffEntity> tariffs) {
        var codesFromProperties = conditionsProperties.getCommissionCodes();

        Set<String> commissionCodes = tariffs.stream()
                .map(TariffEntity::getCommissionCode)
                .filter(code ->
                        codesFromProperties.getServiceMonthly().equals(code) || codesFromProperties.getServiceYearly().equals(code)
                )
                .collect(Collectors.toSet());

        if (commissionCodes.size() != 1) {
            throw BusinessException.of(TARIFF_NOT_FOUND);
        }

        return commissionCodes.iterator().next();
    }

    @NotNull
    private boolean isComboCard(CardDTO cardDTO) {
        return ofNullable(cardDTO.getComboData())
                .map(it -> it.getComboMode() != null)
                .orElse(false);
    }
}

```

</details>

# Резюме

Цикломатическая сложность показывает сложность программы на основе количества возможных путей ее выполнения. Чем выше ЦС, тем больше тестов потребуется для обеспечения полного покрытия. Таким образом, высокая ЦС усложняет процесс тестирования, а именно требует больше усилий для поддержания актуальности и работоспособности тестовых сценариев. Вот яркий пример из кодовой базы:
```
@ParameterizedTest
@CsvSource(
    "C3,ANDROID,11,58,",
    "M2,ANDROID,11,58,''",
    "M2,ANDROID,11,59,",
    "M2,ANDROID,11,60,",
    "M2,IOS,11,58,",
    "M2,IOS,11,59,",
    "M2,IOS,11,60,",
)
fun `must return correct subtitle due to vary headers`(
```
Очевидно, в тестируемом методе присутствует большое число ветвлений, которое порождает большое число тестов. Какие здесь могут быть проблемы? При добавлении очередного ветвления в коде число тестов, необходимых для обеспечения покрытия метода будет увеличиваться. Также потребуется внести изменения в список аргументов всех ранее написанных тестов. При этом достаточно просто можно пропустить (не добавить) интересующий кейс. При изменении значений (порогов, констант и т.д.) потребуется доработка всех тестов.

Такой код требует рефакторинга, так как является тяжело поддерживаемым. Обычно, уже на этапе написания тестов появляется непреодолимое желание уменьшить его ЦС, чтобы облегчить свои страдания.  

Как добиться снижения ЦС?
1) Использовать синтаксические конструкции и стандартные библиотеки языка: элвис-оператор, non-nullable типы, регекспы и т.д.
2) Разделить код на более мелкие методы.
3) Выносить повторяющиеся блоки кода в отдельные методы.
4) Использовать полиморфизм.
5) Писать код в декларативном стиле.
6) По возможности делать состояние объекта неизменяемым.
7) Применять паттерны проектирования.