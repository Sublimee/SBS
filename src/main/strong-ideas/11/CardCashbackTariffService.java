package ru.alfabank.mobile.tariff.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Service;
import ru.alfabank.mobile.contract.header.Headers;
import ru.alfabank.mobile.exceptions.BusinessException;
import ru.alfabank.mobile.starter.client.feign.card.CardDTO;
import ru.alfabank.mobile.tariff.client.bonus.amount.dto.BonusAmountDTO;
import ru.alfabank.mobile.tariff.client.loyalty.card.info.dto.LoyaltyCardInfo;
import ru.alfabank.mobile.tariff.configuration.WidgetCashbackConditionsProperties;
import ru.alfabank.mobile.tariff.configuration.WidgetCashbackConditionsProperties.WidgetCardScreenFeaturesProperties;
import ru.alfabank.mobile.tariff.model.CardStatus;
import ru.alfabank.mobile.tariff.model.CashbackConditions;
import ru.alfabank.mobile.tariff.service.bonus.amount.BonusAmountService;
import ru.alfabank.mobile.tariff.service.card.CardService;
import ru.alfabank.mobile.tariff.service.converter.CardCashbackTariffConverter;
import ru.alfabank.mobile.tariff.service.feature.FeatureService;
import ru.alfabank.mobile.tariff.service.loyalty.card.info.LoyaltyCardInfoService;

import java.time.Clock;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

import static ru.alfabank.mobile.tariff.exception.ErrorCode.LOYALTY_KEY_IS_NULL;
import static ru.alfabank.mobile.tariff.exception.ErrorCode.UNABLE_TO_MATCH_LOYALTY_CARD_INFO;
import static ru.alfabank.mobile.tariff.model.BonusAmountStatus.NOT_ACCRUED_TO_BONUS_ACCOUNT;
import static ru.alfabank.mobile.tariff.util.WidgetUtils.ALFA_ONLINE_CHANNEL_ID;
import static ru.alfabank.mobile.tariff.util.WidgetUtils.ONE;
import static ru.alfabank.mobile.tariff.util.WidgetUtils.isRulesIdGroupNeeded;

@Service
@RequiredArgsConstructor
@Slf4j
public class CardCashbackTariffService {

    private final CardService cardService;
    private final CardCashbackTariffConverter cardCashbackTariffConverter;
    private final LoyaltyCardInfoService loyaltyCardInfoService;
    private final BonusAmountService bonusAmountService;
    private final WidgetCashbackConditionsProperties widgetProperties;
    private final FeatureService featureService;
    private final Clock clock;

    public List<CashbackConditions> getCardsCashbackConditions(Headers headers) {
        List<CardDTO> cards = cardService.getMaskedCards(headers);
        List<LoyaltyCardInfo> loyaltyCardsInfo = loyaltyCardInfoService.getLoyaltyCardsInfo(headers);
        List<CardStatus> cardStatuses = new ArrayList<>();

        boolean widgetCardScreenOpenForCustomer = isWidgetCardScreenOpenForCustomer(headers);

        List<CashbackConditions> cashbackConditions = cards.stream()
                .map(card -> {
                    try {
                        CashbackConditions conditions = widgetCardScreenOpenForCustomer
                                ? getWidgetCashbackConditions(headers, card, loyaltyCardsInfo)
                                : getCardCashbackConditions(headers, card, loyaltyCardsInfo);
                        addCardStatusPassed(cardStatuses, card, conditions, widgetCardScreenOpenForCustomer);
                        return conditions;
                    } catch (Exception e) {
                        addCardStatusExcluded(cardStatuses, card, e, widgetCardScreenOpenForCustomer);
                        return null;
                    }
                })
                .filter(Objects::nonNull)
                .collect(Collectors.toList());

        log.info("Card cashback screen statuses for user {}: {}", headers.getUserId(), cardStatuses);
        return cashbackConditions;
    }

    public CashbackConditions getCardCashbackConditions(Headers headers, String cardId) {
        CardDTO card = cardService.getMaskedCard(headers, cardId);
        List<LoyaltyCardInfo> loyaltyCardsInfo = loyaltyCardInfoService.getLoyaltyCardsInfo(headers);

        return getCardCashbackConditions(headers, card, loyaltyCardsInfo);
    }

    private CashbackConditions getCardCashbackConditions(Headers headers,
                                                         CardDTO card,
                                                         List<LoyaltyCardInfo> loyaltyCardsInfo) {
        LoyaltyCardInfo loyaltyCardInfo = getLoyaltyCardInfo(card, loyaltyCardsInfo)
                .orElseThrow(() -> BusinessException.of(UNABLE_TO_MATCH_LOYALTY_CARD_INFO));

        CashbackConditions conditions = cardCashbackTariffConverter.getCashbackConditions(headers, card, loyaltyCardInfo);

        if (conditions.getLoyaltyKey() == null
                && !isRulesIdGroupNeeded(conditions.getRulesId(),
                widgetProperties.getRulesIdGroup().getCategoricalCashback())) {
            throw BusinessException.of(LOYALTY_KEY_IS_NULL);
        }
        return conditions;
    }

    private void addCardStatusPassed(List<CardStatus> cardStatuses,
                                     CardDTO card,
                                     CashbackConditions conditions,
                                     boolean widgetCardScreenOpenForCustomer) {
        cardStatuses.add(CardStatus.builder()
                .cardId(card.getId())
                .rulesId(conditions.getRulesId())
                .loyaltyKey(conditions.getLoyaltyKey())
                .excluded(false)
                .widgetCardScreenOpenForCustomer(widgetCardScreenOpenForCustomer)
                .build());
    }

    private void addCardStatusExcluded(List<CardStatus> cardStatuses,
                                       CardDTO card,
                                       Exception e,
                                       boolean isWidgetScreen) {
        cardStatuses.add(CardStatus.builder()
                .cardId(card.getId())
                .excluded(true)
                .widgetCardScreenOpenForCustomer(isWidgetScreen)
                .errorCode(e.getMessage())
                .build());
    }

    public CashbackConditions getWidgetCashbackConditions(Headers headers, String cardId) {
        CardDTO card = cardService.getMaskedCard(headers, cardId);

        List<LoyaltyCardInfo> loyaltyCardsInfo = loyaltyCardInfoService.getLoyaltyCardsInfo(headers);
        return getWidgetCashbackConditions(headers, card, loyaltyCardsInfo);
    }

    public CashbackConditions getWidgetCashbackConditions(Headers headers,
                                                          CardDTO card,
                                                          List<LoyaltyCardInfo> loyaltyCardsInfo) {
        LoyaltyCardInfo loyaltyCardInfo = getLoyaltyCardInfo(card, loyaltyCardsInfo)
                .orElseThrow(() -> BusinessException.of(UNABLE_TO_MATCH_LOYALTY_CARD_INFO));
        log.debug("loyaltyCardInfo - {}, headers - {}", loyaltyCardInfo, headers);

        List<BonusAmountDTO> bonusAmounts = getBonusAmounts(headers, card, loyaltyCardInfo);

        return cardCashbackTariffConverter.fetchWidgetCashbackConditions(
                headers,
                loyaltyCardInfo,
                card,
                bonusAmounts
        );
    }

    @NotNull
    private List<BonusAmountDTO> getBonusAmounts(Headers headers, CardDTO card, LoyaltyCardInfo loyaltyCardInfo) {
        return bonusAmountService.getBonusSumByCard(
                        headers,
                        LocalDate.now(clock).minusMonths(ONE).withDayOfMonth(ONE),
                        card.getId())
                .stream()
                .filter(bonusAmountDTO -> bonusAmountDTO.getBonusSumAccrualStatus() == NOT_ACCRUED_TO_BONUS_ACCOUNT.getCode())
                .filter(bonusAmountDTO -> bonusAmountDTO.getBonusAccountNumber().startsWith(loyaltyCardInfo.getAccountType()))
                .filter(bonusAmountDTO ->
                        bonusAmountDTO.getAccrualDate().isAfter(LocalDate.now(clock).minusDays(ONE)))
                .sorted(Comparator.comparing(BonusAmountDTO::getAccrualDate))
                .collect(Collectors.toList());
    }

    private Optional<LoyaltyCardInfo> getLoyaltyCardInfo(CardDTO card, List<LoyaltyCardInfo> loyaltyCardsInfo) {
        List<LoyaltyCardInfo> loyaltyCardsInfoWithType = loyaltyCardsInfo
                .stream()
                .filter(loyaltyCardInfo -> card.getType().equals(loyaltyCardInfo.getCardType()))
                .collect(Collectors.toList());

        if (!loyaltyCardsInfoWithType.isEmpty()) {
            return getLoyaltyCardsInfoByServicePackage(card, loyaltyCardsInfoWithType);
        } else {
            List<LoyaltyCardInfo> loyaltyCardsInfoWithNullType = loyaltyCardsInfo
                    .stream()
                    .filter(loyaltyCardInfo -> loyaltyCardInfo.getCardType() == null)
                    .collect(Collectors.toList());

            return getLoyaltyCardsInfoByServicePackage(card, loyaltyCardsInfoWithNullType);
        }
    }

    private Optional<LoyaltyCardInfo> getLoyaltyCardsInfoByServicePackage(
            CardDTO card,
            List<LoyaltyCardInfo> loyaltyCardsInfoWithType) {
        List<LoyaltyCardInfo> loyaltyCardsInfoWithTypeAndServicePackage = loyaltyCardsInfoWithType
                .stream()
                .filter(loyaltyCardInfo -> card.getServicePackage().equals(loyaltyCardInfo.getServicePackage()))
                .collect(Collectors.toList());

        if (!loyaltyCardsInfoWithTypeAndServicePackage.isEmpty()) {
            return getLoyaltyCardInfoByCardContractId(card, loyaltyCardsInfoWithTypeAndServicePackage);
        } else {
            List<LoyaltyCardInfo> loyaltyCardsInfoWithTypeAndNullServicePackage = loyaltyCardsInfoWithType
                    .stream()
                    .filter(loyaltyCardsInfo -> loyaltyCardsInfo.getServicePackage() == null)
                    .collect(Collectors.toList());

            return getLoyaltyCardInfoByCardContractId(card, loyaltyCardsInfoWithTypeAndNullServicePackage);
        }
    }

    private Optional<LoyaltyCardInfo> getLoyaltyCardInfoByCardContractId(
            CardDTO card,
            List<LoyaltyCardInfo> loyaltyCardsInfoWithTypeAndServicePackage) {
        List<LoyaltyCardInfo> loyaltyCardsInfoWithTypeAndServicePackageAndCardContractId =
                loyaltyCardsInfoWithTypeAndServicePackage
                        .stream()
                        .filter(
                                loyaltyCardInfo -> card.getCardContractId().equals(loyaltyCardInfo.getCardContractId())
                        )
                        .toList();

        if (!loyaltyCardsInfoWithTypeAndServicePackageAndCardContractId.isEmpty()) {
            return loyaltyCardsInfoWithTypeAndServicePackageAndCardContractId
                    .stream()
                    .filter(Objects::nonNull)
                    .findAny();
        } else {
            return loyaltyCardsInfoWithTypeAndServicePackage
                    .stream()
                    .filter(loyaltyCardInfo -> loyaltyCardInfo.getCardContractId() == null)
                    .findAny();
        }
    }

    private boolean isWidgetCardScreenOpenForCustomer(Headers headers) {
        if (headers.getChannelId().equals(ALFA_ONLINE_CHANNEL_ID)) {
            return true;
        }

        WidgetCardScreenFeaturesProperties cardScreenFeatures = widgetProperties.getWidgetCardScreenFeatures();

        Set<String> featuresForCheck = new HashSet<>();
        featuresForCheck.addAll(cardScreenFeatures.getAndroid());
        featuresForCheck.addAll(cardScreenFeatures.getIos());

        Collection<String> providedFeatures = featureService.getFeatures(headers, featuresForCheck);

        return providedFeatures.containsAll(cardScreenFeatures.getAndroid())
                || providedFeatures.containsAll(cardScreenFeatures.getIos());
    }
}