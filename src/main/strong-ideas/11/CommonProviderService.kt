package some.company.mobile.loyalty.promoted.cashback.service.proxy

import kotlinx.coroutines.reactive.awaitSingle
import mu.KLogging
import org.springframework.stereotype.Service
import some.company.mobile.cache.aspect.annotation.CachePutAsync
import some.company.mobile.cache.aspect.annotation.CacheableAsync
import some.company.mobile.contract.header.Headers
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.PARAMETERS_INDEPENDENT_CACHE_KEY_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.PROMOTED_CASHBACK_CARDS_TERMS_CACHE_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.USER_INTERFACE_CONTENT_CACHE_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.WIDGET_SETTINGS_CACHE_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.MaplProperties
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties
import some.company.mobile.loyalty.promoted.cashback.service.client.common.LoyaltyCardTermsClient
import some.company.mobile.loyalty.promoted.cashback.service.client.common.UserInterfaceContentClient
import some.company.mobile.loyalty.promoted.cashback.service.client.common.WidgetsSettingsClient
import some.company.mobile.loyalty.promoted.cashback.service.client.model.PromotedCashbackCardTerms
import some.company.mobile.loyalty.promoted.cashback.service.client.model.UserInterfaceContent
import some.company.mobile.loyalty.promoted.cashback.service.client.model.UwsAttractiveOffersRequest
import some.company.mobile.loyalty.promoted.cashback.service.client.model.WidgetSettings
import some.company.mobile.loyalty.promoted.cashback.util.isNotNullOrEmpty
import kotlin.coroutines.cancellation.CancellationException

@Service
class CommonProviderService(
    private val loyaltyCardTermsClient: LoyaltyCardTermsClient,
    private val userInterfaceContentClient: UserInterfaceContentClient,
    private val widgetsSettingsClient: WidgetsSettingsClient,
    private val maplProperties: MaplProperties,
    private val programsProperties: ProgramsProperties,
) {

    @CacheableAsync(cacheName = WIDGET_SETTINGS_CACHE_NAME, key = "{#period}")
    suspend fun getWidgetSettings(headers: Headers, period: String): Map<Int, WidgetSettings> = try {
        widgetsSettingsClient
            .getWidgetsSettings(
                channelId = headers.channelId,
                request = UwsAttractiveOffersRequest(
                    from = period,
                    to = period,
                )
            )
            .awaitSingle()
            .associateBy { it.programId }
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        logger.error(e) { "Failed getting widget settings from MAPL for period $period" }
        throw e
    }

    @CachePutAsync(cacheName = WIDGET_SETTINGS_CACHE_NAME, key = "{#period}")
    suspend fun updateWidgetSettings(headers: Headers, period: String) = getWidgetSettings(headers, period)

    @CacheableAsync(cacheName = USER_INTERFACE_CONTENT_CACHE_NAME, key = PARAMETERS_INDEPENDENT_CACHE_KEY_NAME)
    suspend fun getUserInterfaceContent(headers: Headers): UserInterfaceContent = try {
        userInterfaceContentClient
            .getUserInterfaceContent(
                channelId = headers.channelId,
                userId = headers.userId,
                request = maplProperties.uwsCustomerAdvertOffersRequest,
            )
            .awaitSingle()
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        logger.error(e) { "Failed getting user interface content from MAPL for user with id ${headers.userId}" }
        throw e
    }

    @CachePutAsync(cacheName = USER_INTERFACE_CONTENT_CACHE_NAME, key = PARAMETERS_INDEPENDENT_CACHE_KEY_NAME)
    suspend fun updateUserInterfaceContent(headers: Headers) = getUserInterfaceContent(headers)

    @CacheableAsync(cacheName = PROMOTED_CASHBACK_CARDS_TERMS_CACHE_NAME, key = PARAMETERS_INDEPENDENT_CACHE_KEY_NAME)
    suspend fun getPromotedCashbackCardsTerms(headers: Headers): Set<PromotedCashbackCardTerms> = try {
        loyaltyCardTermsClient
            .getLoyaltyCardsTerms(channelId = headers.channelId)
            .awaitSingle()
            .filter { it.bonusAccountTypeId != null }
            .filter {
                it.loyaltyProgramIds
                    ?.filter { loyaltyProgramId -> programsProperties.isPromotedCashbackProgram(loyaltyProgramId) }
                    .isNotNullOrEmpty()
            }
            .map {
                PromotedCashbackCardTerms(
                    cardType = it.cardType,
                    defaultCardType = it.defaultCardType,
                    cardContractId = it.cardContractId,
                    servicePackage = it.servicePackage,
                    bonusAccountTypeId = it.bonusAccountTypeId!!,
                    promotedCashbackProgramIds = it.loyaltyProgramIds!!.filter { loyaltyProgramId ->
                        programsProperties.isPromotedCashbackProgram(loyaltyProgramId)
                    },
                    cardCashbackTermsId = it.cardCashbackTermsId,
                    defaultImageURL = it.defaultImageURL,
                    defaultCardName = it.defaultCardName,
                    cashbackPercentRate = it.cashbackPercentRate,
                    priority = it.getPriority(),
                )
            }
            .toSet()
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        logger.error(e) { "Failed getting promoted cashback cards terms from MAPL" }
        throw e
    }

    @CachePutAsync(cacheName = PROMOTED_CASHBACK_CARDS_TERMS_CACHE_NAME, key = PARAMETERS_INDEPENDENT_CACHE_KEY_NAME)
    suspend fun updatePromotedCashbackCardsTerms(headers: Headers) = getPromotedCashbackCardsTerms(headers)

    private companion object : KLogging()
}