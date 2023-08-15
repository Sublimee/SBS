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
import some.company.mobile.loyalty.promoted.cashback.service.audit.AuditService
import some.company.mobile.loyalty.promoted.cashback.service.client.model.SuggestedOffers
import some.company.mobile.loyalty.promoted.cashback.service.proxy.WheelOfFortuneProviderService

@Service
class WheelOfFortuneConfirmationService(
    private val wheelOfFortuneSummaryService: WheelOfFortuneSummaryService,
    private val promotedCashbackAvailabilityService: PromotedCashbackAvailabilityService,
    private val suggestedOffersRepository: SuggestedOffersRepository,
    private val wheelOfFortuneProviderService: WheelOfFortuneProviderService,
    auditService: AuditService
) : ConfirmationService(auditService) {

    override val programId: Int = WHEEL_OF_FORTUNE_PROGRAM_ID

    override suspend fun checkConfirmationRequirements(
        headers: Headers,
        idsToConfirm: List<Int>,
        offerDate: String,
        auditOperationReference: String
    ) {
        try {
            promotedCashbackAvailabilityService.checkPromotedCashbackProgramAvailable(
                headers = headers,
                programId = programId,
                offerDate = offerDate,
            )
            wheelOfFortuneSummaryService.checkOfferNotConfirmed(headers, offerDate)
            checkProvidedWinnerOffer(headers, offerDate, idsToConfirm.first())
        } catch (e: Exception) {
            updateAuditStatus(headers, auditOperationReference, OperationStatus.VALIDATION_FAIL)
            throw e
        }
    }

    override suspend fun performConfirmation(headers: Headers, idsToConfirm: List<Int>, offerDate: String) {
        wheelOfFortuneProviderService.confirmOffer(
            headers = headers,
            offerConfirmationRequest = OfferConfirmationRequest(
                winnerOfferId = idsToConfirm.first(),
                offerDate = offerDate,
            )
        )
    }

    override suspend fun handleException(headers: Headers, e: Exception, auditOperationReference: String) {
        logger.error(e) {
            "Wheel of fortune confirmation failed for user with id ${headers.userId} due to internal problem"
        }
        updateAuditStatus(headers, auditOperationReference, OperationStatus.FAIL)
        throw BusinessException.of(LogicErrorCode.WHEEL_OF_FORTUNE_WINNER_CONFIRMATION_ERROR)
    }

    private suspend fun checkProvidedWinnerOffer(headers: Headers, offerDate: String, winnerOfferId: Int) {
        val suggestedOffersByKey: SuggestedOffers? = suggestedOffersRepository.getSuggestedOffersByKey(
            "${CacheConfiguration.SUGGESTED_OFFERS_CACHE_NAME}::${headers.userId},$offerDate"
        )
        if (suggestedOffersByKey == null) {
            logger.warn {
                "Wheel of fortune winner id not found for user with id ${headers.userId}, winner offer id = $winnerOfferId and offer date = $offerDate"
            }
            throw BusinessException.of(LogicErrorCode.WHEEL_OF_FORTUNE_WINNER_NOT_FOUND)
        }
        if (winnerOfferId != suggestedOffersByKey.winnerOffer.id) {
            logger.error {
                "Provided winner offer id $winnerOfferId does not match with cached one $suggestedOffersByKey"
            }
            throw BusinessException.of(LogicErrorCode.WHEEL_OF_FORTUNE_WINNER_MISMATCH)
        }
    }



    private companion object : KLogging()
}
//@Service
//class WheelOfFortuneConfirmationService (
//    private val wheelOfFortuneSummaryService: WheelOfFortuneSummaryService,
//    private val promotedCashbackAvailabilityService: PromotedCashbackAvailabilityService,
//    private val suggestedOffersRepository: SuggestedOffersRepository,
//    private val wheelOfFortuneProviderService: WheelOfFortuneProviderService,
//    private val auditService: AuditService,
//) {
//
//    suspend fun confirmOffer(headers: Headers, offerConfirmationRequest: OfferConfirmationRequest) {
//        val auditOperationReference = auditService.createAuditOperation(
//            headers = headers,
//            programId = WHEEL_OF_FORTUNE_PROGRAM_ID,
//            idsToConfirm = listOf(offerConfirmationRequest.winnerOfferId),
//        )
//
//        checkConfirmationRequirements(headers, offerConfirmationRequest, auditOperationReference)
//
//        try {
//            auditService.updateAuditOperationStatus(
//                headers = headers,
//                programId = WHEEL_OF_FORTUNE_PROGRAM_ID,
//                auditOperationReference = auditOperationReference,
//                status = OperationStatus.PROGRESS,
//            )
//            wheelOfFortuneProviderService.confirmOffer(
//                headers = headers,
//                offerConfirmationRequest = offerConfirmationRequest,
//            )
//            auditService.updateAuditOperationStatus(
//                headers = headers,
//                programId = WHEEL_OF_FORTUNE_PROGRAM_ID,
//                auditOperationReference = auditOperationReference,
//                status = OperationStatus.SUCCESS,
//            )
//        } catch (e: Exception) {
//            logger.error(e) {
//                "Wheel of fortune confirmation failed for user with id ${headers.userId} and request " +
//                        "$offerConfirmationRequest due to internal problem"
//            }
//            auditService.updateAuditOperationStatus(
//                headers = headers,
//                programId = WHEEL_OF_FORTUNE_PROGRAM_ID,
//                auditOperationReference = auditOperationReference,
//                status = OperationStatus.FAIL,
//            )
//            throw BusinessException.of(LogicErrorCode.WHEEL_OF_FORTUNE_WINNER_CONFIRMATION_ERROR)
//        }
//    }
//
//    private suspend fun checkConfirmationRequirements(
//        headers: Headers,
//        offerConfirmationRequest: OfferConfirmationRequest,
//        auditOperationReference: String,
//    ) {
//        try {
//            promotedCashbackAvailabilityService.checkPromotedCashbackProgramAvailable(
//                headers,
//                WHEEL_OF_FORTUNE_PROGRAM_ID,
//                offerConfirmationRequest.offerDate,
//            )
//            wheelOfFortuneSummaryService.checkOfferNotConfirmed(headers, offerConfirmationRequest.offerDate)
//            checkProvidedWinnerOffer(headers, offerConfirmationRequest)
//        } catch (e: Exception) {
//            auditService.updateAuditOperationStatus(
//                headers = headers,
//                programId = WHEEL_OF_FORTUNE_PROGRAM_ID,
//                auditOperationReference = auditOperationReference,
//                status = OperationStatus.VALIDATION_FAIL,
//            )
//            throw e
//        }
//
//    }
//
//    private suspend fun checkProvidedWinnerOffer(headers: Headers, offerConfirmationRequest: OfferConfirmationRequest) {
//        val suggestedOffersByKey: SuggestedOffers? = suggestedOffersRepository.getSuggestedOffersByKey(
//            "${CacheConfiguration.SUGGESTED_OFFERS_CACHE_NAME}::${headers.userId},${offerConfirmationRequest.offerDate}"
//        )
//        if (suggestedOffersByKey == null) {
//            logger.warn {
//                "Wheel of fortune winner id not found for user with id ${headers.userId}, request: $offerConfirmationRequest"
//            }
//            throw BusinessException.of(LogicErrorCode.WHEEL_OF_FORTUNE_WINNER_NOT_FOUND)
//        }
//        if (offerConfirmationRequest.winnerOfferId != suggestedOffersByKey.winnerOffer.id) {
//            logger.error {
//                "Provided winner offer id $offerConfirmationRequest does not match with cached one $suggestedOffersByKey"
//            }
//            throw BusinessException.of(LogicErrorCode.WHEEL_OF_FORTUNE_WINNER_MISMATCH)
//        }
//    }
//
//    private companion object : KLogging()
//}