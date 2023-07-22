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
