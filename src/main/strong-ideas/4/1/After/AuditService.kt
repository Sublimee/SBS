package some.company.mobile.loyalty.promoted.cashback.service.audit

import mu.KLogging
import org.springframework.stereotype.Service
import some.company.mobile.contract.header.Headers
import some.company.mobile.entity.operation.OperationStatus
import some.company.mobile.exceptions.InternalException
import some.company.mobile.loyalty.promoted.cashback.configuration.AuditRequestParams
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.service.ws.WsAccountClickPaymentService

@Service
class AuditService(
    private val wsAccountClickPaymentService: WsAccountClickPaymentService,
    private val programsProperties: ProgramsProperties,
) {

    suspend fun createAuditOperation(
        headers: Headers,
        programId: Int,
        idsToConfirm: List<Int>,
    ): String = wsAccountClickPaymentService.createAuditOperation(
        headers = headers,
        providerData = getAuditRequestParams(programId),
        idsToConfirm = idsToConfirm,
    )

    suspend fun updateAuditOperationStatus(
        headers: Headers,
        programId: Int,
        auditOperationReference: String,
        status: OperationStatus,
    ) {
        wsAccountClickPaymentService.changeAuditOperationStatus(
            headers = headers,
            providerData = getAuditRequestParams(programId),
            auditOperationReference = auditOperationReference,
            status = status,
        )
    }

    private suspend fun getAuditRequestParams(programId: Int): AuditRequestParams {
        return programsProperties.propertiesById["$programId"]!!.auditRequestParams
    }

    private companion object : KLogging()
}