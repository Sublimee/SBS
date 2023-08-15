package some.company.mobile.loyalty.promoted.cashback.service

import some.company.mobile.contract.header.Headers
import some.company.mobile.entity.operation.OperationStatus
import some.company.mobile.loyalty.promoted.cashback.service.audit.AuditService

abstract class ConfirmationService(
    private val auditService: AuditService,
) {
    abstract val programId: Int

    suspend fun confirm(headers: Headers, idsToConfirm: List<Int>, offerDate: String) {
        val auditOperationReference = auditService.createAuditOperation(
            headers = headers,
            programId = programId,
            idsToConfirm = idsToConfirm,
        )

        checkConfirmationRequirements(headers, idsToConfirm, offerDate, auditOperationReference)

        try {
            updateAuditStatus(headers, auditOperationReference, OperationStatus.PROGRESS)
            updateAuditStatus(headers, auditOperationReference, OperationStatus.SUCCESS)
            performConfirmation(headers, idsToConfirm, offerDate)
        } catch (e: Exception) {
            handleException(headers, e, auditOperationReference)
        }
    }

    abstract suspend fun checkConfirmationRequirements(
        headers: Headers,
        idsToConfirm: List<Int>,
        offerDate: String,
        auditOperationReference: String
    )

    abstract suspend fun performConfirmation(headers: Headers, idsToConfirm: List<Int>, offerDate: String)

    abstract suspend fun handleException(headers: Headers, e: Exception, auditOperationReference: String)

    protected suspend fun updateAuditStatus(headers: Headers, auditOperationReference: String, status: OperationStatus) {
        auditService.updateAuditOperationStatus(
            headers = headers,
            programId = programId,
            auditOperationReference = auditOperationReference,
            status = status
        )
    }
}