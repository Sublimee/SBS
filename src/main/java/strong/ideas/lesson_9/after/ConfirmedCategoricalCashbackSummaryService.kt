package some.company.mobile.loyalty.promoted.cashback.service

import mu.KLogging
import org.springframework.stereotype.Service
import some.company.mobile.contract.header.Headers
import some.company.mobile.exceptions.InternalException
import some.company.mobile.loyalty.promoted.cashback.configuration.SummaryProperties
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.model.CategoricalCashbackSummaryResponse
import some.company.mobile.loyalty.promoted.cashback.model.CategoriesSection
import some.company.mobile.loyalty.promoted.cashback.model.CategoryRepresentation
import some.company.mobile.loyalty.promoted.cashback.service.client.model.Category
import some.company.mobile.loyalty.promoted.cashback.service.client.model.ConfirmedCategories
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CategoriesProviderService
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CommonProviderService
import some.company.mobile.loyalty.promoted.cashback.util.DateTimeUtils.getPrepositionalMonthName
import some.company.mobile.loyalty.promoted.cashback.util.DeclensionUtils.getCategoryDeclensionInNominativeCase

@Service
class ConfirmedCategoricalCashbackSummaryService(
    private val cardsSectionService: CardsSectionService,
    private val categoriesProviderService: CategoriesProviderService,
    private val commonProviderService: CommonProviderService,
    private val summaryProperties: SummaryProperties,
    private val categoryRepresentationService: CategoryRepresentationService,
) : AbstractSummary(categoriesProviderService,
        categoryRepresentationService,
        commonProviderService,
        summaryProperties) {

    suspend fun getConfirmedCategoricalCashbackSummaryResponse(
        headers: Headers,
        offerDate: String,
        confirmedCategories: ConfirmedCategories,
    ): CategoricalCashbackSummaryResponse {
        val cardsSection = cardsSectionService.getCardsSection(headers)
        return CategoricalCashbackSummaryResponse(
            title = getConfirmedCategoriesTitle(
                offerDate = offerDate,
                confirmedCategoriesSize = confirmedCategories.categories.size,
            ),
            categoriesSection = getCategoriesSection(
                headers = headers,
                userCategories = confirmedCategories.categories,
            ),
            cardsSection = cardsSection,
            agreementTerms = agreementTermsButton(headers),
        )
    }

    private fun getConfirmedCategoriesTitle(offerDate: String, confirmedCategoriesSize: Int): String =
        String.format(
            summaryProperties.categoricalCashback.confirmedCategories.titleTemplate,
            confirmedCategoriesSize,
            getCategoryDeclensionInNominativeCase(confirmedCategoriesSize),
            getPrepositionalMonthName(offerDate),
        )

    private companion object : KLogging()
}