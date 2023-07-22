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
