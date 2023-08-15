package some.company.mobile.loyalty.promoted.cashback.service

import mu.KLogging
import org.springframework.stereotype.Service
import some.company.mobile.contract.header.Headers
import some.company.mobile.entity.operation.OperationStatus
import some.company.mobile.exceptions.BusinessException
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties.Companion.WHEEL_OF_FORTUNE_PROGRAM_ID
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.model.OfferConfirmationRequest
import some.company.mobile.loyalty.promoted.cashback.repository.SuggestedOffersRepository
import some.company.mobile.loyalty.promoted.cashback.service.client.model.SuggestedOffers
import some.company.mobile.loyalty.promoted.cashback.service.proxy.WheelOfFortuneProviderService
import some.company.mobile.loyalty.promoted.cashback.service.ws.WsAccountClickPaymentService

@Service
class WheelOfFortuneConfirmationService(
    private val wheelOfFortuneSummaryService: WheelOfFortuneSummaryService,
    private val promotedCashbackAvailabilityService: PromotedCashbackAvailabilityService,
    private val suggestedOffersRepository: SuggestedOffersRepository,
    private val wheelOfFortuneProviderService: WheelOfFortuneProviderService,
    private val wsAccountClickPaymentService: WsAccountClickPaymentService,
    private val programsProperties: ProgramsProperties,
) {

    suspend fun confirmOffer(headers: Headers, offerConfirmationRequest: OfferConfirmationRequest) {
        val auditOperation = createAuditOperation(headers, offerConfirmationRequest)

        try {
            promotedCashbackAvailabilityService.checkPromotedCashbackProgramAvailable(
                headers = headers,
                programId = WHEEL_OF_FORTUNE_PROGRAM_ID,
                offerDate = offerConfirmationRequest.offerDate,
            )
            wheelOfFortuneSummaryService.checkOfferNotConfirmed(headers, offerConfirmationRequest.offerDate)
            checkWinnerOfferId(headers, offerConfirmationRequest)

            updateAuditOperationStatus(headers, auditOperation, OperationStatus.PROGRESS)
            wheelOfFortuneProviderService.confirmOffer(
                headers = headers,
                offerConfirmationRequest = offerConfirmationRequest
            )
            updateAuditOperationStatus(headers, auditOperation, OperationStatus.SUCCESS)
        } catch (e: Exception) {
            logger.error(e) {
                "Wheel of fortune confirmation failed for user with id ${headers.userId} and request " +
                        "$offerConfirmationRequest due to internal problem"
            }
            updateAuditOperationStatus(headers, auditOperation, OperationStatus.FAIL)
            throw BusinessException.of(LogicErrorCode.WHEEL_OF_FORTUNE_WINNER_CONFIRMATION_ERROR)
        }
    }

    private suspend fun checkWinnerOfferId(
        headers: Headers,
        offerConfirmationRequest: OfferConfirmationRequest,
    ) {
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

    private suspend fun createAuditOperation(
        headers: Headers,
        offerConfirmationRequest: OfferConfirmationRequest,
    ) = wsAccountClickPaymentService.createAuditOperation(
        headers = headers,
        providerData = programsProperties.getWheelOfFortuneProgramProperties().auditRequestParams,
        idsToConfirm = listOf(offerConfirmationRequest.winnerOfferId),
    )?.reference

    private suspend fun updateAuditOperationStatus(
        headers: Headers,
        auditOperationReference: String?,
        status: OperationStatus,
    ) = wsAccountClickPaymentService.changeAuditOperationStatus(
        headers = headers,
        providerData = programsProperties.getWheelOfFortuneProgramProperties().auditRequestParams,
        auditOperationReference = auditOperationReference,
        status = status,
    )

    private companion object : KLogging()
}