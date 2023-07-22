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
