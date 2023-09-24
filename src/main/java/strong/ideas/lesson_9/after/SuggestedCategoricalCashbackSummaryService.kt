package some.company.mobile.loyalty.promoted.cashback.service

import mu.KLogging
import org.springframework.stereotype.Service
import some.company.mobile.contract.header.Headers
import some.company.mobile.loyalty.promoted.cashback.configuration.SummaryProperties
import some.company.mobile.loyalty.promoted.cashback.model.Button
import some.company.mobile.loyalty.promoted.cashback.model.CategoricalCashbackSummaryResponse
import some.company.mobile.loyalty.promoted.cashback.service.client.model.SuggestedCategories
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CategoriesProviderService
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CommonProviderService
import some.company.mobile.loyalty.promoted.cashback.util.CategoriesSectionUtils.validateAndFixSuggestedCategoriesSection
import some.company.mobile.loyalty.promoted.cashback.util.DateTimeUtils.getPrepositionalMonthName
import some.company.mobile.loyalty.promoted.cashback.util.DeclensionUtils.getCategoryDeclensionInAccusativeCase
import some.company.mobile.loyalty.promoted.cashback.util.DeclensionUtils.toAccusativeCase

@Service
class SuggestedCategoricalCashbackSummaryService(
    private val cardsSectionService: CardsSectionService,
    private val categoriesProviderService: CategoriesProviderService,
    private val commonProviderService: CommonProviderService,
    private val summaryProperties: SummaryProperties,
    private val categoryRepresentationService: CategoryRepresentationService,
) : AbstractSummary(
    categoriesProviderService,
    categoryRepresentationService,
    commonProviderService,
    summaryProperties
) {

    suspend fun getSuggestedCategoricalCashbackSummaryResponse(
        headers: Headers,
        offerDate: String,
    ): CategoricalCashbackSummaryResponse {
        val suggestedCategories: SuggestedCategories =
            categoriesProviderService.getSuggestedCategories(headers, offerDate)

        return CategoricalCashbackSummaryResponse(
            title = getTitle(
                offerDate = offerDate,
                suggestedCategories = suggestedCategories,
            ),
            categoriesSection = getCategoriesSection(
                headers = headers,
                userCategories = suggestedCategories.categories,
                acceptanceThreshold = suggestedCategories.requiredCount,
            ).let { validateAndFixSuggestedCategoriesSection(it) },
            cardsSection = cardsSectionService.getCardsSection(headers),
            ratePopUp = summaryProperties.categoricalCashback.suggestedCategories.getRatePopUp(headers),
            agreementTerms = agreementTermsButton(headers),
            acceptanceButton = getAcceptanceButton(suggestedCategories.requiredCount),
        )
    }

    private fun getTitle(
        offerDate: String,
        suggestedCategories: SuggestedCategories,
    ): String {
        val suggestedCategoriesProperties = summaryProperties.categoricalCashback.suggestedCategories
        val acceptanceThreshold = suggestedCategories.requiredCount
        val preDefinedCategoriesCount =
            suggestedCategories.categories.count { it.isSelected == true && it.isEditable == false }

        return String.format(
            suggestedCategoriesProperties.titleTemplateByHasResponsePreDefinedCategories[preDefinedCategoriesCount > 0]!!,
            acceptanceThreshold - preDefinedCategoriesCount,
            getCategoryDeclensionInAccusativeCase(acceptanceThreshold - preDefinedCategoriesCount),
            getPrepositionalMonthName(offerDate),
        )
    }

    private fun getAcceptanceButton(acceptanceThreshold: Int): Button {
        val acceptanceButton = summaryProperties.categoricalCashback.suggestedCategories.acceptanceButton
        return Button(
            title = acceptanceButton.title,
            alertMessage = String.format(
                acceptanceButton.alertMessageTemplate,
                acceptanceThreshold.toAccusativeCase(),
                getCategoryDeclensionInAccusativeCase(acceptanceThreshold),
            ),
        )
    }

    private companion object : KLogging()
}