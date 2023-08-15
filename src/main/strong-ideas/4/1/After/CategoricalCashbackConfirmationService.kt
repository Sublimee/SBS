package some.company.mobile.loyalty.promoted.cashback.service

import mu.KLogging
import org.springframework.stereotype.Service
import some.company.mobile.contract.header.Headers
import some.company.mobile.entity.operation.OperationStatus.FAIL
import some.company.mobile.entity.operation.OperationStatus.PROGRESS
import some.company.mobile.entity.operation.OperationStatus.SUCCESS
import some.company.mobile.entity.operation.OperationStatus.VALIDATION_FAIL
import some.company.mobile.exceptions.BusinessException
import some.company.mobile.exceptions.InternalException
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties.Companion.CATEGORICAL_CASHBACK_PROGRAM_ID
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.model.CategoriesConfirmationRequest
import some.company.mobile.loyalty.promoted.cashback.service.audit.AuditService
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CategoriesProviderService

@Service
class CategoricalCashbackConfirmationService(
    private val categoriesProviderService: CategoriesProviderService,
    private val promotedCashbackAvailabilityService: PromotedCashbackAvailabilityService,
    private val auditService: AuditService,
) {

    suspend fun confirmCategories(headers: Headers, categoriesConfirmationRequest: CategoriesConfirmationRequest) {
        val auditOperationReference: String = auditService.createAuditOperation(
            headers = headers,
            programId = CATEGORICAL_CASHBACK_PROGRAM_ID,
            idsToConfirm = categoriesConfirmationRequest.categoriesIdsToConfirm,
        )

        checkCategoriesConfirmationRequirements(headers, categoriesConfirmationRequest, auditOperationReference)

        try {
            auditService.updateAuditOperationStatus(
                headers = headers,
                programId = CATEGORICAL_CASHBACK_PROGRAM_ID,
                auditOperationReference = auditOperationReference,
                status = PROGRESS,
            )
            categoriesProviderService.confirmCategories(headers, categoriesConfirmationRequest)
            auditService.updateAuditOperationStatus(
                headers = headers,
                programId = CATEGORICAL_CASHBACK_PROGRAM_ID,
                auditOperationReference = auditOperationReference,
                status = SUCCESS,
            )
        } catch (e: Exception) {
            logger.error(e) {
                "Categories confirmation failed for user with id ${headers.userId} and request $categoriesConfirmationRequest"
            }
            auditService.updateAuditOperationStatus(
                headers = headers,
                programId = CATEGORICAL_CASHBACK_PROGRAM_ID,
                auditOperationReference = auditOperationReference,
                status = FAIL,
            )
            throw BusinessException.of(LogicErrorCode.CATEGORIES_CONFIRMATION_ERROR)
        }
    }

    private suspend fun checkCategoriesConfirmationRequirements(
        headers: Headers,
        categoriesConfirmationRequest: CategoriesConfirmationRequest,
        auditOperationReference: String,
    ) {
        try {
            promotedCashbackAvailabilityService.checkPromotedCashbackProgramAvailable(
                headers = headers,
                programId = CATEGORICAL_CASHBACK_PROGRAM_ID,
                offerDate = categoriesConfirmationRequest.offerDate,
            )
            checkSpecifiedPeriodCategoriesNotConfirmed(headers, categoriesConfirmationRequest)
            checkCategoriesCountMatchRequirement(headers, categoriesConfirmationRequest)
        } catch (e: Exception) {
            auditService.updateAuditOperationStatus(
                headers = headers,
                programId = CATEGORICAL_CASHBACK_PROGRAM_ID,
                auditOperationReference = auditOperationReference,
                status = VALIDATION_FAIL,
            )
            throw BusinessException.of(LogicErrorCode.CATEGORIES_CONFIRMATION_ERROR)
        }
    }

    private suspend fun checkCategoriesCountMatchRequirement(
        headers: Headers,
        categoriesConfirmationRequest: CategoriesConfirmationRequest,
    ) {
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

    private suspend fun checkSpecifiedPeriodCategoriesNotConfirmed(
        headers: Headers,
        categoriesConfirmationRequest: CategoriesConfirmationRequest,
    ) {
        val confirmedCategories =
            categoriesProviderService.getConfirmedCategories(headers, categoriesConfirmationRequest.offerDate)
        if (confirmedCategories != null) {
            throw InternalException.of(LogicErrorCode.SPECIFIED_PERIOD_CATEGORIES_ALREADY_CONFIRMED)
        }
    }

    private companion object : KLogging()
}