package ru.alfabank.mobile.loyalty.promoted.cashback.service.proxy

import kotlinx.coroutines.reactive.awaitFirstOrNull
import kotlinx.coroutines.reactive.awaitSingle
import mu.KLogging
import org.springframework.stereotype.Service
import ru.alfabank.mobile.cache.aspect.annotation.CacheEvictAsync
import ru.alfabank.mobile.cache.aspect.annotation.CachePutAsync
import ru.alfabank.mobile.cache.aspect.annotation.CacheableAsync
import ru.alfabank.mobile.contract.header.Headers
import ru.alfabank.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.CONFIRMED_OFFER_ID_CACHE_NAME
import ru.alfabank.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.OFFERS_DIRECTORY_CACHE_NAME
import ru.alfabank.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.SUGGESTED_OFFERS_CACHE_NAME
import ru.alfabank.mobile.loyalty.promoted.cashback.configuration.SummaryProperties
import ru.alfabank.mobile.loyalty.promoted.cashback.model.OfferConfirmationRequest
import ru.alfabank.mobile.loyalty.promoted.cashback.repository.UserSuggestedOffersRepository
import ru.alfabank.mobile.loyalty.promoted.cashback.repository.entity.UserSuggestedOffers
import ru.alfabank.mobile.loyalty.promoted.cashback.service.client.model.ConfirmOfferRequest
import ru.alfabank.mobile.loyalty.promoted.cashback.service.client.model.OfferDirectoryItem
import ru.alfabank.mobile.loyalty.promoted.cashback.service.client.model.SuggestedOffers
import ru.alfabank.mobile.loyalty.promoted.cashback.service.client.model.UwsOffersDirectoryRequest
import ru.alfabank.mobile.loyalty.promoted.cashback.service.client.program.wheel.of.fortune.OffersConfirmationClient
import ru.alfabank.mobile.loyalty.promoted.cashback.service.client.program.wheel.of.fortune.OffersDirectoryClient
import ru.alfabank.mobile.loyalty.promoted.cashback.service.client.program.wheel.of.fortune.OffersSuggestionClient
import java.time.LocalDateTime
import kotlin.coroutines.cancellation.CancellationException

@Service
class WheelOfFortuneProviderService(
    private val userSuggestedOffersRepository: UserSuggestedOffersRepository,
    private val offersConfirmationClient: OffersConfirmationClient,
    private val offersDirectoryClient: OffersDirectoryClient,
    private val offersSuggestionClient: OffersSuggestionClient,
    private val summaryProperties: SummaryProperties,
) {

    @CacheableAsync(
        cacheName = OFFERS_DIRECTORY_CACHE_NAME,
        key = "#offerDate",
    )
    suspend fun getOffersDirectory(headers: Headers, offerDate: String): Map<Int, OfferDirectoryItem> {
        return try {
            offersDirectoryClient
                .getOffersDirectory(
                    channelId = headers.channelId,
                    request = UwsOffersDirectoryRequest(offerDate),
                )
                .awaitSingle().associateBy { it.id }
        } catch (e: CancellationException) {
            throw e
        } catch (e: Exception) {
            logger.error(e) {
                "Failed getting offers directory from MAPL for user with id ${headers.userId} and offer date $offerDate"
            }
            throw e
        }
    }

    @CachePutAsync(
        cacheName = OFFERS_DIRECTORY_CACHE_NAME,
        key = "#offerDate",
    )
    suspend fun updateOffersDirectory(headers: Headers, offerDate: String) = getOffersDirectory(headers, offerDate)

    @CacheableAsync(
        cacheName = SUGGESTED_OFFERS_CACHE_NAME,
        key = "{#headers.userId, #offerDate}",
    )
    suspend fun getSuggestedOffersFromCacheOrFetch(headers: Headers, offerDate: String): SuggestedOffers = try {
        val cachedSuggestedOffers: SuggestedOffers? = getSuggestedOffersFromCache(headers, offerDate)
        if (cachedSuggestedOffers != null) {
            cachedSuggestedOffers
        } else {
            val suggestedOffers = offersSuggestionClient
                .getSuggestedOffers(
                    channelId = headers.channelId,
                    userId = headers.userId,
                    period = offerDate,
                )
                .awaitSingle()
            userSuggestedOffersRepository.save(
                UserSuggestedOffers(
                    userId = headers.userId,
                    offerDate = offerDate,
                    suggestedOffers = suggestedOffers,
                    expireTime = LocalDateTime.now().plus(summaryProperties.wheelOfFortune.suggestedOffersCacheTtl)
                )
            )
            suggestedOffers
        }
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        logger.error(e) {
            "Failed getting suggested offers for user with id ${headers.userId} and offer date $offerDate"
        }
        throw e
    }

    suspend fun getSuggestedOffersFromCache(headers: Headers, offerDate: String): SuggestedOffers? =
        userSuggestedOffersRepository.findByUserIdAndOfferDate(headers.userId, offerDate)?.suggestedOffers

    @CacheableAsync(
        cacheName = CONFIRMED_OFFER_ID_CACHE_NAME,
        key = "{#headers.userId, #offerDate}",
    )
    suspend fun getConfirmedOfferId(headers: Headers, offerDate: String): Int? {
        return try {
            offersConfirmationClient
                .getConfirmedOfferId(
                    channelId = headers.channelId,
                    userId = headers.userId,
                    period = offerDate,
                )
                .awaitSingle().offerId
        } catch (e: CancellationException) {
            throw e
        } catch (e: Exception) {
            logger.error(e) {
                "Failed getting confirmed offer from MAPL for user with id ${headers.userId} and " +
                        "offer date $offerDate"
            }
            throw e
        }
    }

    @CacheEvictAsync(
        cacheNames = [CONFIRMED_OFFER_ID_CACHE_NAME],
        key = "{#headers.userId, #offerConfirmationRequest.offerDate}",
        ignoreCacheError = true,
    )
    suspend fun confirmOffer(
        headers: Headers,
        offerConfirmationRequest: OfferConfirmationRequest,
    ) {
        try {
            offersConfirmationClient
                .confirmOffer(
                    channelId = headers.channelId,
                    userId = headers.userId,
                    period = offerConfirmationRequest.offerDate,
                    request = ConfirmOfferRequest(offerId = offerConfirmationRequest.winnerOfferId),
                )
                .awaitFirstOrNull()
        } catch (e: CancellationException) {
            throw e
        } catch (e: Exception) {
            logger.error(e) {
                "Offer confirmation failed for user with id ${headers.userId} and request $offerConfirmationRequest"
            }
            throw e
        }
    }

    private companion object : KLogging()
}