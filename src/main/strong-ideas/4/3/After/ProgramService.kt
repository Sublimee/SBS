package some.company.mobile.loyalty.promoted.cashback.service

import mu.KLogging
import org.springframework.stereotype.Service
import some.company.mobile.contract.header.Headers
import some.company.mobile.exceptions.BusinessException
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.model.ProgramWidget
import some.company.mobile.loyalty.promoted.cashback.model.ProgramsSummaryResponse
import some.company.mobile.loyalty.promoted.cashback.model.PromotedCashbackAvailability
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CommonProviderService
import some.company.mobile.loyalty.promoted.cashback.service.widget.WidgetService
import some.company.mobile.loyalty.promoted.cashback.util.sortFirstByDateDescendingAndNextById

@Service
class ProgramService(
    private val widgetServiceList: List<WidgetService>,
    private val commonProviderService: CommonProviderService,
    private val motivationService: MotivationService,
    private val promotedCashbackAvailabilityService: PromotedCashbackAvailabilityService,
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
        val availableProgramIds: Set<Int> = promotedCashbackAvailability.userCardsTerms
            .filter { it.bonusAccountTypeId == bonusAccountType }
            .flatMap { it.promotedCashbackProgramIds }.toSet()

        return promotedCashbackAvailabilityService.getAvailableProgramsPeriods(headers)
            .filter { programPeriod -> availableProgramIds.contains(programPeriod.programId) }
            .flatMap {
                widgetServiceList.find { widgetService -> widgetService.getProgramId() == it.programId }
                    ?.getProgramWidgets(headers, it.periods) ?: emptyList()
            }
    }

    private companion object : KLogging()
}