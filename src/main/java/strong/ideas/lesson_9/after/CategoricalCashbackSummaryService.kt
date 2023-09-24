package some.company.mobile.loyalty.promoted.cashback.service

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
    private val categoriesProviderService: CategoriesProviderService,
    private val promotedCashbackAvailabilityService: PromotedCashbackAvailabilityService,
    private val confirmedCategoricalCashbackSummaryService: ConfirmedCategoricalCashbackSummaryService,
    private val suggestedCategoricalCashbackSummaryService: SuggestedCategoricalCashbackSummaryService,
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
            suggestedCategoricalCashbackSummaryService.getSuggestedCategoricalCashbackSummaryResponse(
                headers = headers,
                offerDate = offerDate,
            )
        } else {
            confirmedCategoricalCashbackSummaryService.getConfirmedCategoricalCashbackSummaryResponse(
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

    private companion object : KLogging()
}