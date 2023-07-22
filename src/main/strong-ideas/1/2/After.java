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
