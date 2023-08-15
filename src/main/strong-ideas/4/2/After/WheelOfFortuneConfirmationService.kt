package some.company.mobile.loyalty.promoted.cashback.service

import mu.KLogging
import org.springframework.stereotype.Service
import some.company.mobile.contract.header.Headers
import some.company.mobile.entity.operation.OperationStatus
import some.company.mobile.exceptions.BusinessException
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties.Companion.WHEEL_OF_FORTUNE_PROGRAM_ID
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.model.OfferConfirmationRequest
import some.company.mobile.loyalty.promoted.cashback.repository.SuggestedOffersRepository
import some.company.mobile.loyalty.promoted.cashback.service.audit.AuditService
import some.company.mobile.loyalty.promoted.cashback.service.client.model.SuggestedOffers
import some.company.mobile.loyalty.promoted.cashback.service.proxy.WheelOfFortuneProviderService

@Service
class WheelOfFortuneConfirmationService (
    private val wheelOfFortuneSummaryService: WheelOfFortuneSummaryService,
    private val promotedCashbackAvailabilityService: PromotedCashbackAvailabilityService,
    private val suggestedOffersRepository: SuggestedOffersRepository,
    private val wheelOfFortuneProviderService: WheelOfFortuneProviderService,
    private val auditService: AuditService,
) {

    suspend fun confirmOffer(headers: Headers, offerConfirmationRequest: OfferConfirmationRequest) {
        val auditOperationReference = auditService.createAuditOperation(
            headers = headers,
            programId = WHEEL_OF_FORTUNE_PROGRAM_ID,
            idsToConfirm = listOf(offerConfirmationRequest.winnerOfferId),
        )

        checkConfirmationRequirements(headers, offerConfirmationRequest, auditOperationReference)

        try {
            auditService.updateAuditOperationStatus(
                headers = headers,
                programId = WHEEL_OF_FORTUNE_PROGRAM_ID,
                auditOperationReference = auditOperationReference,
                status = OperationStatus.PROGRESS,
            )
            auditService.updateAuditOperationStatus(
                headers = headers,
                programId = WHEEL_OF_FORTUNE_PROGRAM_ID,
                auditOperationReference = auditOperationReference,
                status = OperationStatus.SUCCESS,
            )
            wheelOfFortuneProviderService.confirmOffer(
                headers = headers,
                offerConfirmationRequest = offerConfirmationRequest,
            )
        } catch (e: Exception) {
            logger.error(e) {
                "Wheel of fortune confirmation failed for user with id ${headers.userId} and request " +
                        "$offerConfirmationRequest due to internal problem"
            }
            auditService.updateAuditOperationStatus(
                headers = headers,
                programId = WHEEL_OF_FORTUNE_PROGRAM_ID,
                auditOperationReference = auditOperationReference,
                status = OperationStatus.FAIL,
            )
            throw BusinessException.of(LogicErrorCode.WHEEL_OF_FORTUNE_WINNER_CONFIRMATION_ERROR)
        }
    }

    private suspend fun checkConfirmationRequirements(
        headers: Headers,
        offerConfirmationRequest: OfferConfirmationRequest,
        auditOperationReference: String,
    ) {
        try {
            promotedCashbackAvailabilityService.checkPromotedCashbackProgramAvailable(
                headers,
                WHEEL_OF_FORTUNE_PROGRAM_ID,
                offerConfirmationRequest.offerDate,
            )
            wheelOfFortuneSummaryService.checkOfferNotConfirmed(headers, offerConfirmationRequest.offerDate)
            checkProvidedWinnerOffer(headers, offerConfirmationRequest)
        } catch (e: Exception) {
            auditService.updateAuditOperationStatus(
                headers = headers,
                programId = WHEEL_OF_FORTUNE_PROGRAM_ID,
                auditOperationReference = auditOperationReference,
                status = OperationStatus.VALIDATION_FAIL,
            )
            throw e
        }

    }

    private suspend fun checkProvidedWinnerOffer(headers: Headers, offerConfirmationRequest: OfferConfirmationRequest) {
        val suggestedOffersByKey: SuggestedOffers? = suggestedOffersRepository.getSuggestedOffersByKey(
            "${CacheConfiguration.SUGGESTED_OFFERS_CACHE_NAME}::${headers.userId},${offerConfirmationRequest.offerDate}"
        )
        if (suggestedOffersByKey == null) {
            logger.warn {
                "Wheel of fortune winner id not found for user with id ${headers.userId}, request: $offerConfirmationRequest"
            }
            throw BusinessException.of(LogicErrorCode.WHEEL_OF_FORTUNE_WINNER_NOT_FOUND)
        }
        if (offerConfirmationRequest.winnerOfferId != suggestedOffersByKey.winnerOffer.id) {
            logger.error {
                "Provided winner offer id $offerConfirmationRequest does not match with cached one $suggestedOffersByKey"
            }
            throw BusinessException.of(LogicErrorCode.WHEEL_OF_FORTUNE_WINNER_MISMATCH)
        }
    }

    private companion object : KLogging()
}

abstract class ConfirmationService(
    private val auditService: AuditService
) {
    abstract val programId: Int

    suspend fun confirm(headers: Headers, idsToConfirm: List<Int>) {
        val auditOperationReference = auditService.createAuditOperation(
            headers = headers,
            programId = programId,
            idsToConfirm = idsToConfirm
        )

        checkConfirmationRequirements(headers, idsToConfirm, auditOperationReference)

        try {
            updateAuditStatus(headers, auditOperationReference, OperationStatus.PROGRESS)
            performConfirmation(headers, idsToConfirm)
            updateAuditStatus(headers, auditOperationReference, OperationStatus.SUCCESS)
        } catch (e: Exception) {
            handleException(headers, e, auditOperationReference)
        }
    }

    abstract suspend fun checkConfirmationRequirements(
        headers: Headers,
        idsToConfirm: List<Int>,
        auditOperationReference: String
    )

    abstract suspend fun performConfirmation(headers: Headers, idsToConfirm: List<Int>)

    protected suspend fun updateAuditStatus(headers: Headers, auditOperationReference: String, status: OperationStatus) {
        auditService.updateAuditOperationStatus(
            headers = headers,
            programId = programId,
            auditOperationReference = auditOperationReference,
            status = status
        )
    }

    abstract fun handleException(headers: Headers, e: Exception, auditOperationReference: String)
}