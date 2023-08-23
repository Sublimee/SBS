import kotlinx.coroutines.async
import kotlinx.coroutines.coroutineScope
import org.springframework.stereotype.Service
import some.company.mobile.contract.header.Headers
import some.company.mobile.loyalty.promoted.cashback.configuration.SummaryProperties
import some.company.mobile.loyalty.promoted.cashback.model.CardSection
import some.company.mobile.loyalty.promoted.cashback.model.CardsSection
import some.company.mobile.loyalty.promoted.cashback.service.client.model.matches
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CommonProviderService

@Service
class CardsSectionService(
    private val commonProviderService: CommonProviderService,
    private val cardsService: CardsService,
    private val summaryProperties: SummaryProperties,
) {

    suspend fun getCardsSection(headers: Headers): CardsSection = CardsSection(
        title = summaryProperties.categoricalCashback.cardsSection.title,
        cards = getCardsSectionItems(headers),
        subtitle = summaryProperties.categoricalCashback.cardsSection.getSubtitle(headers),
    )

    /**
     * При формировании секции требуется "схлопнуть" карты пользователя для лаконичности отображения на UI. Это действие
     * выполняется при наличии у пользователей карт одного типа: несколько карт пользователя будут представлены в UI одним
     * элементом.
     *
     * "Схлопывание" карт не должно использоваться в бизнес-логике при определении доступности ПК.
     */
    private suspend fun getCardsSectionItems(headers: Headers): List<CardSection> = coroutineScope {
        val promotedCashbackCardsTermsDeferred =
            async { commonProviderService.getPromotedCashbackCardsTerms(headers) }
        val cardsWithPromotedCashbackDeferred =
            async { cardsService.getCardsWithPromotedCashback(headers) }

        val promotedCashbackCardsTerms = promotedCashbackCardsTermsDeferred.await()
        val cardsWithPromotedCashback = cardsWithPromotedCashbackDeferred.await()

        promotedCashbackCardsTerms
            .asSequence()
            .filter { terms -> cardsWithPromotedCashback.any { card -> card.matches(terms) } }
            .groupBy({ it.defaultCardType }, { it })
            .map { entry -> entry.value.maxBy { it.priority } }
            .map { terms ->
                if (terms.cardType == terms.defaultCardType) {
                    val (title, imageURL) = cardsWithPromotedCashback.first { card -> card.matches(terms) }
                    CardSection(
                        title = title,
                        cardType = terms.cardType,
                        imageURL = extractURLWithoutParameters(imageURL),
                    )
                } else {
                    CardSection(
                        title = terms.defaultCardName!!,
                        cardType = terms.defaultCardType,
                        imageURL = terms.defaultImageURL!!,
                    )
                }
            }
    }

    private fun extractURLWithoutParameters(url: String): String = url.substring(0, url.lastIndexOf('?'))
}