package some.company.loyalty.promoted.cashback.service

import mu.KLogging
import org.springframework.stereotype.Service
import some.company.contract.header.Headers
import some.company.exceptions.BusinessException
import some.company.loyalty.promoted.cashback.configuration.ProgramsProperties.Companion.CATEGORICAL_CASHBACK_PROGRAM_ID
import some.company.loyalty.promoted.cashback.configuration.ProgramsProperties.Companion.WHEEL_OF_FORTUNE_PROGRAM_ID
import some.company.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.loyalty.promoted.cashback.model.ProgramWidget
import some.company.loyalty.promoted.cashback.model.ProgramsSummaryResponse
import some.company.loyalty.promoted.cashback.service.client.model.PromotedCashbackCardTerms
import some.company.loyalty.promoted.cashback.service.proxy.CommonProviderService
import some.company.loyalty.promoted.cashback.service.widget.CategoricalCashbackWidgetService
import some.company.loyalty.promoted.cashback.service.widget.WheelOfFortuneWidgetService
import some.company.loyalty.promoted.cashback.util.sortFirstByDateDescendingAndNextById

@Service
class ProgramService(
    private val promotedCashbackAvailabilityService: PromotedCashbackAvailabilityService,
    private val categoricalCashbackWidgetService: CategoricalCashbackWidgetService,
    private val wheelOfFortuneWidgetService: WheelOfFortuneWidgetService,
    private val motivationService: MotivationService,
    private val commonProviderService: CommonProviderService,
) {

    suspend fun getSummary(headers: Headers, bonusAccountType: String): ProgramsSummaryResponse {
        val userPromotedCashbackCardsTerms = try {
            promotedCashbackAvailabilityService.getUserPromotedCashbackCardsTerms(headers)
        } catch (e: Exception) {
            logger.error(e) {
                "Failed getting promoted cashback programs summary for user with id ${headers.userId} due to user " +
                        "cards terms fetch error"
            }
            throw BusinessException.of(LogicErrorCode.PROGRAMS_SUMMARY_FETCH_ERROR)
        }

        if (userPromotedCashbackCardsTerms.isEmpty()) {
            throw BusinessException.of(LogicErrorCode.PROMOTED_CASHBACK_NOT_AVAILABLE)
        }

        try {
            val programs = getPrograms(headers, userPromotedCashbackCardsTerms, bonusAccountType)
            return ProgramsSummaryResponse(
                title = commonProviderService.getUserInterfaceContent(headers = headers).programsSectionTitle,
                programs = programs.sortFirstByDateDescendingAndNextById(),
                motivation = motivationService.getMotivation(headers, programs)
            )
        } catch (e: Exception) {
            logger.error(e) { "Failed getting promoted cashback programs summary for user with id ${headers.userId}" }
            throw BusinessException.of(LogicErrorCode.PROGRAMS_SUMMARY_FETCH_ERROR)
        }
    }

    private suspend fun getPrograms(
        headers: Headers,
        userPromotedCashbackCardsTerms: List<PromotedCashbackCardTerms>,
        bonusAccountType: String,
    ): List<ProgramWidget> {
        val availableProgramsPeriods = promotedCashbackAvailabilityService.getAvailableProgramsPeriods(headers)
        val availableProgramIds = userPromotedCashbackCardsTerms
            .filter { it.bonusAccountTypeId == bonusAccountType }
            .flatMap { it.promotedCashbackProgramIds }.toSet()

        return availableProgramsPeriods
            .filter { programPeriod -> availableProgramIds.contains(programPeriod.programId) }
            .flatMap {
                when (it.programId) {
                    CATEGORICAL_CASHBACK_PROGRAM_ID -> categoricalCashbackWidgetService.getProgramWidgets(
                        headers = headers,
                        periods = it.periods,
                    )

                    WHEEL_OF_FORTUNE_PROGRAM_ID -> wheelOfFortuneWidgetService.getProgramWidgets(
                        headers = headers,
                        periods = it.periods,
                    )

                    else -> emptyList()
                }
            }
    }

    private companion object : KLogging()
}