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
