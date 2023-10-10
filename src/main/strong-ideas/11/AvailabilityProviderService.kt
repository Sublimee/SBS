package ru.alfabank.mobile.loyalty.promoted.cashback.service.proxy

import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.reactive.awaitSingle
import mu.KLogging
import org.springframework.stereotype.Service
import ru.alfabank.mobile.cache.aspect.annotation.CachePutAsync
import ru.alfabank.mobile.cache.aspect.annotation.CacheableAsync
import ru.alfabank.mobile.contract.header.Headers
import ru.alfabank.mobile.exceptions.BusinessException
import ru.alfabank.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.AVAILABLE_PROGRAM_PERIODS_CACHE_NAME
import ru.alfabank.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.PARAMETERS_INDEPENDENT_CACHE_KEY_NAME
import ru.alfabank.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.USER_LOYALTIES_CACHE_NAME
import ru.alfabank.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties
import ru.alfabank.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import ru.alfabank.mobile.loyalty.promoted.cashback.service.client.common.AvailableProgramsPeriodsClient
import ru.alfabank.mobile.loyalty.promoted.cashback.service.client.common.UserLoyaltiesClient
import ru.alfabank.mobile.loyalty.promoted.cashback.service.client.model.ProgramPeriods

@Service
class AvailabilityProviderService(
    private val availableProgramsPeriodsClient: AvailableProgramsPeriodsClient,
    private val userLoyaltiesClient: UserLoyaltiesClient,
    private val programsProperties: ProgramsProperties,
) {

    @CacheableAsync(cacheName = USER_LOYALTIES_CACHE_NAME, key = "#headers.userId")
    suspend fun getUserPromotedCashbackProgramsByBonusAccountTypes(headers: Headers): Map<Int, List<Int>> = try {
        userLoyaltiesClient
            .getLoyaltyProgramIdsByBonusAccountsType(
                channelId = headers.channelId,
                userId = headers.userId,
            )
            .awaitSingle()
            .keyValueList
            .filter {
                it.loyaltyProgramIds
                    .any { loyaltyProgramId -> programsProperties.isPromotedCashbackProgram(loyaltyProgramId) }
            }.associate {
                it.bonusAccountTypeId to it.loyaltyProgramIds.filter { loyaltyProgramId ->
                    programsProperties.isPromotedCashbackProgram(loyaltyProgramId)
                }
            }
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        logger.error(e) { "Failed getting promoted cashback programs by bonus account types from MAPL for user with id ${headers.userId}" }
        throw BusinessException.of(LogicErrorCode.PROMOTED_CASHBACK_AVAILABILITY_FETCH_ERROR)
    }

    @CacheableAsync(cacheName = AVAILABLE_PROGRAM_PERIODS_CACHE_NAME, key = PARAMETERS_INDEPENDENT_CACHE_KEY_NAME)
    suspend fun getAvailableProgramsPeriods(headers: Headers): List<ProgramPeriods> = try {
        availableProgramsPeriodsClient
            .getAvailableProgramsPeriods(channelId = headers.channelId)
            .awaitSingle()
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        logger.error(e) { "Failed getting available programs periods from MAPL for user with id ${headers.userId}" }
        throw e
    }

    @CachePutAsync(cacheName = AVAILABLE_PROGRAM_PERIODS_CACHE_NAME, key = PARAMETERS_INDEPENDENT_CACHE_KEY_NAME)
    suspend fun updateAvailableProgramsPeriods(headers: Headers) = getAvailableProgramsPeriods(headers)

    private companion object : KLogging()
}