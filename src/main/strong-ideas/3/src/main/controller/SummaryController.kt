package some.company.loyalty.promoted.cashback.controller

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController
import some.company.contract.header.Headers
import some.company.contract.header.MandatoryHeadersConstraint
import some.company.kotlin.webflux.utils.withTraceContext
import some.company.loyalty.promoted.cashback.model.CategoricalCashbackSummaryResponse
import some.company.loyalty.promoted.cashback.model.ProgramsSummaryResponse
import some.company.loyalty.promoted.cashback.service.CategoricalCashbackSummaryService
import some.company.loyalty.promoted.cashback.service.ProgramService

@RestController
@RequestMapping("/summary")
class SummaryController(
    private val categoricalCashbackSummaryService: CategoricalCashbackSummaryService,
    private val programService: ProgramService,
) {

    @GetMapping("/programs")
    suspend fun getProgramsSummary(
        @MandatoryHeadersConstraint(userId = true) headers: Headers,
        @RequestParam bonusAccountTypeId: String,
    ): ProgramsSummaryResponse = withTraceContext {
        programService.getSummary(headers, bonusAccountTypeId)
    }

    @GetMapping("/categorical-cashback")
    suspend fun getCashbackSummary(
        @MandatoryHeadersConstraint(userId = true) headers: Headers,
        @RequestParam offerDate: String,
    ): CategoricalCashbackSummaryResponse = withTraceContext {
        categoricalCashbackSummaryService.getSummary(headers, offerDate)
    }
}