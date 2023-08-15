package some.company.mobile.loyalty.promoted.cashback.service

import mu.KLogging
import org.springframework.stereotype.Service
import some.company.mobile.contract.header.Headers
import some.company.mobile.exceptions.BusinessException
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties.Companion.CATEGORICAL_CASHBACK_PROGRAM_ID
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties.Companion.WHEEL_OF_FORTUNE_PROGRAM_ID
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.model.ProgramWidget
import some.company.mobile.loyalty.promoted.cashback.model.ProgramsSummaryResponse
import some.company.mobile.loyalty.promoted.cashback.model.PromotedCashbackAvailability
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CommonProviderService
import some.company.mobile.loyalty.promoted.cashback.service.widget.CategoricalCashbackWidgetService
import some.company.mobile.loyalty.promoted.cashback.service.widget.WheelOfFortuneWidgetService
import some.company.mobile.loyalty.promoted.cashback.util.sortFirstByDateDescendingAndNextById

@Service
class ProgramService(
    private val categoricalCashbackWidgetService: CategoricalCashbackWidgetService,
    private val commonProviderService: CommonProviderService,
    private val motivationService: MotivationService,
    private val promotedCashbackAvailabilityService: PromotedCashbackAvailabilityService,
    private val wheelOfFortuneWidgetService: WheelOfFortuneWidgetService,
) {

    suspend fun getSummary(headers: Headers, bonusAccountType: String): ProgramsSummaryResponse {
        val promotedCashbackAvailability: PromotedCashbackAvailability = try {
            promotedCashbackAvailabilityService.getPromotedCashbackAvailability(headers)
        } catch (e: Exception) {
            logger.error(e) {
                "Failed getting promoted cashback programs summary for user with id ${headers.userId} due to " +
                        "availability response fetch error"
            }
            throw BusinessException.of(LogicErrorCode.PROGRAMS_SUMMARY_FETCH_ERROR)
        }

        if (!promotedCashbackAvailability.isAvailable) {
            throw BusinessException.of(LogicErrorCode.PROMOTED_CASHBACK_NOT_AVAILABLE)
        }

        try {
            val programs = getPrograms(headers, promotedCashbackAvailability, bonusAccountType)
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
        promotedCashbackAvailability: PromotedCashbackAvailability,
        bonusAccountType: String,
    ): List<ProgramWidget> {
        val availableProgramsPeriods = promotedCashbackAvailabilityService.getAvailableProgramsPeriods(headers)

        var availableProgramIds: Set<Int> = emptySet()
        if (promotedCashbackAvailability.userPromotedCashbackProgramsByBonusAccountTypes != null) {
            availableProgramIds = promotedCashbackAvailability.userPromotedCashbackProgramsByBonusAccountTypes
                .filter { "${it.key}" == bonusAccountType }
                .flatMap { it.value }.toSet()
        } else if (promotedCashbackAvailability.userCardsTerms != null) {
            availableProgramIds = promotedCashbackAvailability.userCardsTerms
                .filter { it.bonusAccountTypeId == bonusAccountType }
                .flatMap { it.promotedCashbackProgramIds }.toSet()
        }

        return availableProgramsPeriods
            .filter { programPeriod -> availableProgramIds.contains(programPeriod.programId) }
            .flatMap {
                var list: List<ProgramWidget> = emptyList()
                if (it.programId == CATEGORICAL_CASHBACK_PROGRAM_ID) {
                    list = categoricalCashbackWidgetService.getProgramWidgets(
                        headers = headers,
                        periods = it.periods,
                    )
                }
                if (it.programId == WHEEL_OF_FORTUNE_PROGRAM_ID) {
                    list = wheelOfFortuneWidgetService.getProgramWidgets(
                        headers = headers,
                        periods = it.periods,
                    )
                }
                list
            }
    }

    private companion object : KLogging()
}