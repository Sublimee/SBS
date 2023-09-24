package strong.ideas.lesson_9.before

import kotlinx.coroutines.CancellationException
import mu.KLogging
import org.springframework.stereotype.Service
import some.company.mobile.contract.header.Headers
import some.company.mobile.exceptions.BusinessException
import some.company.mobile.exceptions.InternalException
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties.Companion.CATEGORICAL_CASHBACK_PROGRAM_ID
import some.company.mobile.loyalty.promoted.cashback.configuration.SummaryProperties
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.model.Button
import some.company.mobile.loyalty.promoted.cashback.model.CategoricalCashbackSummaryResponse
import some.company.mobile.loyalty.promoted.cashback.model.CategoriesSection
import some.company.mobile.loyalty.promoted.cashback.model.CategoryRepresentation
import some.company.mobile.loyalty.promoted.cashback.service.client.model.Category
import some.company.mobile.loyalty.promoted.cashback.service.client.model.ConfirmedCategories
import some.company.mobile.loyalty.promoted.cashback.service.client.model.SuggestedCategories
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CategoriesProviderService
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CommonProviderService
import some.company.mobile.loyalty.promoted.cashback.util.CategoriesSectionUtils.validateAndFixSuggestedCategoriesSection
import some.company.mobile.loyalty.promoted.cashback.util.DateTimeUtils.getPrepositionalMonthName
import some.company.mobile.loyalty.promoted.cashback.util.DeclensionUtils.getCategoryDeclensionInAccusativeCase
import some.company.mobile.loyalty.promoted.cashback.util.DeclensionUtils.getCategoryDeclensionInNominativeCase
import some.company.mobile.loyalty.promoted.cashback.util.DeclensionUtils.toAccusativeCase

@Service
class CategoricalCashbackSummaryService(
    private val cardsSectionService: CardsSectionService,
    private val categoriesProviderService: CategoriesProviderService,
    private val commonProviderService: CommonProviderService,
    private val promotedCashbackAvailabilityService: PromotedCashbackAvailabilityService,
    private val summaryProperties: SummaryProperties,
    private val categoryRepresentationService: CategoryRepresentationService,
) {

    suspend fun getSummary(headers: Headers, offerDate: String): CategoricalCashbackSummaryResponse = try {
        promotedCashbackAvailabilityService.checkPromotedCashbackProgramAvailable(
            headers = headers,
            programId = CATEGORICAL_CASHBACK_PROGRAM_ID,
            offerDate = offerDate,
        )

        val confirmedCategories: ConfirmedCategories? =
            categoriesProviderService.getConfirmedCategories(headers, offerDate)
        if (confirmedCategories == null) {
            getSuggestedCategoricalCashbackSummaryResponse(
                headers = headers,
                offerDate = offerDate,
            )
        } else {
            getConfirmedCategoricalCashbackSummaryResponse(
                headers = headers,
                offerDate = offerDate,
                confirmedCategories = confirmedCategories,
            )
        }
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        logger.error(e) { "Failed getting categorical cashback summary for user with id ${headers.userId} and offer date $offerDate" }
        throw BusinessException.of(LogicErrorCode.CATEGORICAL_CASHBACK_SUMMARY_FETCH_ERROR)
    }

    private suspend fun getSuggestedCategoricalCashbackSummaryResponse(
        headers: Headers,
        offerDate: String,
    ): CategoricalCashbackSummaryResponse {
        val suggestedCategories: SuggestedCategories =
            categoriesProviderService.getSuggestedCategories(headers, offerDate)

        return CategoricalCashbackSummaryResponse(
            title = getSuggestedCategoriesTitle(
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

    private suspend fun getConfirmedCategoricalCashbackSummaryResponse(
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

    private suspend fun getCategoriesSection(
        headers: Headers,
        userCategories: List<Category>,
        acceptanceThreshold: Int? = null,
    ) = CategoriesSection(
        categories = getUserCategoriesRepresentation(headers, userCategories),
        acceptanceThreshold = acceptanceThreshold,
    )

    private suspend fun getUserCategoriesRepresentation(
        headers: Headers,
        userCategories: List<Category>,
    ): List<CategoryRepresentation> {
        val categoriesDirectory = categoriesProviderService.getCategoriesDirectory(headers)
        return userCategories
            .sortedByDescending { it.priority }
            .map {
                it to (categoriesDirectory[it.id]
                    ?: throw InternalException.of(LogicErrorCode.CATEGORIES_DIRECTORY_ITEM_NOT_FOUND))
            }
            .map { (category, categoryDirectoryItem) ->
                categoryRepresentationService.toRepresentation(headers, category, categoryDirectoryItem)
            }
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

    private suspend fun agreementTermsButton(headers: Headers) = Button(
        title = summaryProperties.categoricalCashback.agreementTermsTitle,
        documentUrl = commonProviderService.getUserInterfaceContent(headers).categoricalCashbackTermsDocumentURL,
    )

    private fun getConfirmedCategoriesTitle(offerDate: String, confirmedCategoriesSize: Int): String =
        String.format(
            summaryProperties.categoricalCashback.confirmedCategories.titleTemplate,
            confirmedCategoriesSize,
            getCategoryDeclensionInNominativeCase(confirmedCategoriesSize),
            getPrepositionalMonthName(offerDate),
        )

    private fun getSuggestedCategoriesTitle(
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

    private companion object : KLogging()
}