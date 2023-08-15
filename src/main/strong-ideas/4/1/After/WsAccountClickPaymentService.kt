package some.company.mobile.loyalty.promoted.cashback.service.ws

import kotlinx.coroutines.reactive.awaitSingle
import mu.KLogging
import org.springframework.stereotype.Service
import some.company.api.payment.account.AccountClickPaymentAddClient
import some.company.api.payment.account.AccountClickPaymentAddField
import some.company.api.payment.account.AccountClickPaymentAddRequest
import some.company.api.payment.account.FieldType
import some.company.mobile.contract.header.Headers
import some.company.mobile.entity.operation.OperationStatus
import some.company.mobile.exceptions.InternalException
import some.company.mobile.loyalty.promoted.cashback.configuration.AuditRequestParams
import some.company.mobile.loyalty.promoted.cashback.configuration.WidgetWebViewConditions
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.service.proxy.FeatureToggleApiService
import java.time.Clock
import java.time.Instant

@Service
class WsAccountClickPaymentService(
    private val featureToggleApiService: FeatureToggleApiService,
    private val accountClickPaymentAddClient: AccountClickPaymentAddClient,
    private val widgetWebViewConditions: WidgetWebViewConditions,
    private val clock: Clock,
) {

    suspend fun createAuditOperation(
        headers: Headers,
        providerData: AuditRequestParams,
        idsToConfirm: List<Int>,
    ): String = try {
        val request = AccountClickPaymentAddRequest.builder()
            .type(providerData.type)
            .route(providerData.route)
            .status(OperationStatus.CREATE.code)
            .channelId(headers.channelId)
            .operationDateTime(Instant.now(clock))
            .userId(headers.userId)
            .fields(getRequestFields(headers, idsToConfirm))
            .build()

        accountClickPaymentAddClient.async(headers.channelId, request).awaitSingle().reference
    } catch (e: Exception) {
        logger.error(e) { "Can't create CL2 operation for user ${headers.userId}" }
        throw InternalException.of(LogicErrorCode.CREATE_AUDIT_OPERATION_ERROR)
    }

    suspend fun changeAuditOperationStatus(
        headers: Headers,
        providerData: AuditRequestParams,
        auditOperationReference: String,
        status: OperationStatus,
    ) {
        try {
            AccountClickPaymentAddRequest.builder()
                .reference(auditOperationReference)
                .type(providerData.type)
                .status(status.code)
                .build()
                .apply { accountClickPaymentAddClient.async(headers.channelId, this).awaitSingle() }
        } catch (e: Exception) {
            logger.error(e) {
                "Can't update CL2 operation for user ${headers.userId} and reference $auditOperationReference with status $status"
            }
            throw InternalException.of(LogicErrorCode.UPDATE_AUDIT_OPERATION_ERROR)
        }
    }

    private suspend fun getRequestFields(
        headers: Headers,
        idsToConfirm: List<Int>,
    ): MutableList<AccountClickPaymentAddField> {
        val requestFields = mutableListOf(
            AccountClickPaymentAddField.builder()
                .fieldType(FieldType.CHAR)
                .fieldName(IDS_TO_CONFIRM_PARAM_NAME)
                .fieldValue(idsToConfirm.joinToString(separator = ","))
                .build()
        )

        if (isWebViewRequest(headers)) {
            requestFields.add(
                AccountClickPaymentAddField.builder()
                    .fieldType(FieldType.CHAR)
                    .fieldName(WEBVIEW_PARAM_NAME)
                    .fieldValue(WEBVIEW_PARAM_VALUE)
                    .build()
            )
        }

        return requestFields
    }

    private suspend fun isWebViewRequest(headers: Headers): Boolean =
        featureToggleApiService.hasFeature(headers, widgetWebViewConditions.feature)

    private companion object : KLogging() {
        private const val IDS_TO_CONFIRM_PARAM_NAME = "#IDKA"
        private const val WEBVIEW_PARAM_NAME = "#AIWV"
        private const val WEBVIEW_PARAM_VALUE = "WebView"
    }
}