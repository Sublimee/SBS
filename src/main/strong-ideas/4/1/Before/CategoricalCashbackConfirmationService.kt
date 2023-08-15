package some.company.mobile.loyalty.promoted.cashback.service

import mu.KLogging
import org.springframework.stereotype.Service
import some.company.mobile.contract.header.Headers
import some.company.mobile.entity.operation.OperationStatus
import some.company.mobile.exceptions.BusinessException
import some.company.mobile.exceptions.InternalException
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties.Companion.CATEGORICAL_CASHBACK_PROGRAM_ID
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.model.CategoriesConfirmationRequest
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CategoriesProviderService
import some.company.mobile.loyalty.promoted.cashback.service.ws.WsAccountClickPaymentService

@Service
class CategoricalCashbackConfirmationService(
    private val categoriesProviderService: CategoriesProviderService,
    private val promotedCashbackAvailabilityService: PromotedCashbackAvailabilityService,
    private val wsAccountClickPaymentService: WsAccountClickPaymentService,
    private val programsProperties: ProgramsProperties,
) {

    suspend fun confirmCategories(headers: Headers, categoriesConfirmationRequest: CategoriesConfirmationRequest) {
        val auditOperationReference = createAuditOperation(headers, categoriesConfirmationRequest)

        try {
            promotedCashbackAvailabilityService.checkPromotedCashbackProgramAvailable(
                headers = headers,
                programId = CATEGORICAL_CASHBACK_PROGRAM_ID,
                offerDate = categoriesConfirmationRequest.offerDate,
            )
            validateCategoriesConfirmationRequest(headers, categoriesConfirmationRequest)

            updateAuditOperationStatus(headers, auditOperationReference, OperationStatus.PROGRESS)
            categoriesProviderService.confirmCategories(headers, categoriesConfirmationRequest)
            updateAuditOperationStatus(headers, auditOperationReference, OperationStatus.SUCCESS)
        } catch (e: Exception) {
            logger.error(e) {
                "Categories confirmation failed for user with id ${headers.userId} and request $categoriesConfirmationRequest"
            }
            updateAuditOperationStatus(headers, auditOperationReference, OperationStatus.FAIL)
            throw BusinessException.of(LogicErrorCode.CATEGORIES_CONFIRMATION_ERROR)
        }
    }

    private suspend fun validateCategoriesConfirmationRequest(
        headers: Headers,
        categoriesConfirmationRequest: CategoriesConfirmationRequest,
    ) {
        val confirmedCategories =
            categoriesProviderService.getConfirmedCategories(headers, categoriesConfirmationRequest.offerDate)
        if (confirmedCategories != null) {
            throw InternalException.of(LogicErrorCode.SPECIFIED_PERIOD_CATEGORIES_ALREADY_CONFIRMED)
        }

        val requiredConfirmedCategoriesCount = categoriesProviderService.getSuggestedCategories(
            headers = headers,
            offerDate = categoriesConfirmationRequest.offerDate,
        ).requiredCount
        if (categoriesConfirmationRequest.categoriesIdsToConfirm.size != requiredConfirmedCategoriesCount) {
            logger.error {
                "User with id ${headers.userId} tried confirm $categoriesConfirmationRequest but acceptance threshold " +
                        "is $requiredConfirmedCategoriesCount"
            }
            throw InternalException.of(LogicErrorCode.CONFIRMED_CATEGORIES_COUNT_MISMATCH_ERROR)
        }
    }

    private suspend fun createAuditOperation(
        headers: Headers,
        categoriesConfirmationRequest: CategoriesConfirmationRequest
    ) = wsAccountClickPaymentService.createAuditOperation(
        headers = headers,
        providerData = programsProperties.getCategoricalCashbackProgramProperties().auditRequestParams,
        idsToConfirm = categoriesConfirmationRequest.categoriesIdsToConfirm,
    )?.reference

    private suspend fun updateAuditOperationStatus(
        headers: Headers,
        auditOperationReference: String?,
        status: OperationStatus
    ) = wsAccountClickPaymentService.changeAuditOperationStatus(
        headers = headers,
        providerData = programsProperties.getCategoricalCashbackProgramProperties().auditRequestParams,
        auditOperationReference = auditOperationReference,
        status = status,
    )

    private companion object : KLogging()
}