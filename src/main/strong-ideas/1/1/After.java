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
