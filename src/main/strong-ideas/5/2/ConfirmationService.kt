package some.company.mobile.loyalty.promoted.cashback.service

import some.company.mobile.contract.header.Headers
import some.company.mobile.entity.operation.OperationStatus
import some.company.mobile.loyalty.promoted.cashback.service.audit.AuditService

/**
 * Класс задает структуру выполнения операции подтверждения выбора пользователя по программе повышенного кэшбэка (ПК).
 *
 * Прохождение по этапам операции подтверждения выбора пользователя исходя из требований функционального сопровождения
 * фиксируется в системе аудита в соответствии со следующей статусной моделью:
 *
 *   INIT   →   VALIDATION_FAIL
 *    ↓
 * PROGRESS →   FAIL
 *    ↓
 * SUCCESS  →    ↑
 *
 * Создание операции аудита (со статусом INIT) может быть неуспешным. В этом случае операция аудита не создается,
 * пользователю возвращается ошибка подтверждения выбора.
 *
 * Операция из статуса SUCCESS может попасть в статус FAIL, если после фиксации статуса SUCCESS, подтверждение выбора
 * завершилось неуспешно.
 *
 * Совместно с функциональным сопровождением на основе данных аудита может быть проведен разбор нештатных ситуаций.
 */
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
            updateAuditStatus(headers, auditOperationReference, OperationStatus.FAIL)
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