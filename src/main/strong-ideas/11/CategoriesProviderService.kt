package some.company.mobile.loyalty.promoted.cashback.service.proxy

import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.reactive.awaitFirstOrNull
import kotlinx.coroutines.reactive.awaitSingle
import mu.KLogging
import org.springframework.stereotype.Service
import some.company.mobile.cache.aspect.annotation.CacheEvictAsync
import some.company.mobile.cache.aspect.annotation.CachePutAsync
import some.company.mobile.cache.aspect.annotation.CacheableAsync
import some.company.mobile.contract.header.Headers
import some.company.mobile.exceptions.InternalException
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.CATEGORIES_DIRECTORY_CACHE_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.CONFIRMED_CATEGORIES_CACHE_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.PARAMETERS_INDEPENDENT_CACHE_KEY_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.SUGGESTED_CATEGORIES_CACHE_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.MaplProperties
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.model.CategoriesConfirmationRequest
import some.company.mobile.loyalty.promoted.cashback.service.client.model.CategoriesToConfirmRequest
import some.company.mobile.loyalty.promoted.cashback.service.client.model.CategoryDirectoryItem
import some.company.mobile.loyalty.promoted.cashback.service.client.model.CategoryToConfirm
import some.company.mobile.loyalty.promoted.cashback.service.client.model.ConfirmedCategories
import some.company.mobile.loyalty.promoted.cashback.service.client.model.SuggestedCategories
import some.company.mobile.loyalty.promoted.cashback.service.client.program.categorical.CategoriesConfirmationClient
import some.company.mobile.loyalty.promoted.cashback.service.client.program.categorical.CategoriesDirectoryClient
import some.company.mobile.loyalty.promoted.cashback.service.client.program.categorical.CategoriesSuggestionClient

@Service
class CategoriesProviderService(
    private val categoriesDirectoryClient: CategoriesDirectoryClient,
    private val categoriesSuggestionClient: CategoriesSuggestionClient,
    private val categoriesConfirmationClient: CategoriesConfirmationClient,
    private val maplProperties: MaplProperties,
) {

    @CacheableAsync(
        cacheName = CATEGORIES_DIRECTORY_CACHE_NAME,
        key = PARAMETERS_INDEPENDENT_CACHE_KEY_NAME,
    )
    suspend fun getCategoriesDirectory(headers: Headers): Map<Int, CategoryDirectoryItem> = try {
        categoriesDirectoryClient
            .getCategoriesDirectory(
                channelId = headers.channelId,
                request = maplProperties.uwsCustomerLoyaltyCategoriesRequest,
            )
            .awaitSingle()
            .associateBy { it.getId() }
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        logger.error(e) { "Failed getting categories directory from MAPL for user with id ${headers.userId}" }
        throw e
    }

    @CachePutAsync(
        cacheName = CATEGORIES_DIRECTORY_CACHE_NAME,
        key = PARAMETERS_INDEPENDENT_CACHE_KEY_NAME,
    )
    suspend fun updateCategoriesDirectory(headers: Headers) = getCategoriesDirectory(headers)

    @CacheableAsync(
        cacheName = SUGGESTED_CATEGORIES_CACHE_NAME,
        key = "{#headers.userId, #offerDate}",
    )
    suspend fun getSuggestedCategories(headers: Headers, offerDate: String): SuggestedCategories = try {
        val suggestedCategories: SuggestedCategories = categoriesSuggestionClient
            .getSuggestedCategories(
                channelId = headers.channelId,
                userId = headers.userId,
                period = offerDate,
            )
            .awaitSingle()

        if (suggestedCategories.totalCount != suggestedCategories.categories.size) {
            throw InternalException.of(LogicErrorCode.SUGGESTED_CATEGORIES_COUNT_MISMATCH_ERROR)
        }
        suggestedCategories
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        logger.error(e) {
            "Failed getting suggested categories from MAPL for user with id ${headers.userId} and " +
                    "offer date $offerDate"
        }
        throw e
    }

    @CacheableAsync(
        cacheName = CONFIRMED_CATEGORIES_CACHE_NAME,
        key = "{#headers.userId, #offerDate}",
    )
    suspend fun getConfirmedCategories(headers: Headers, offerDate: String): ConfirmedCategories? {
        val confirmedCategories: ConfirmedCategories = try {
            categoriesConfirmationClient
                .getConfirmedCategories(channelId = headers.channelId, userId = headers.userId, period = offerDate)
                .awaitSingle()
        } catch (e: CancellationException) {
            throw e
        } catch (e: Exception) {
            logger.error(e) {
                "Failed getting confirmed categories from MAPL for user with id ${headers.userId} and offer " +
                        "date $offerDate"
            }
            throw e
        }

        return if (confirmedCategories.categories.isEmpty()) {
            null
        } else {
            confirmedCategories
        }
    }

    @CacheEvictAsync(
        cacheNames = [CONFIRMED_CATEGORIES_CACHE_NAME],
        key = "{#headers.userId, #categoriesConfirmationRequest.offerDate}",
        ignoreCacheError = true,
    )
    suspend fun confirmCategories(
        headers: Headers,
        categoriesConfirmationRequest: CategoriesConfirmationRequest,
    ) = try {
        val suggestedCategories = categoriesSuggestionClient
            .getSuggestedCategories(
                channelId = headers.channelId,
                userId = headers.userId,
                period = categoriesConfirmationRequest.offerDate,
            ).awaitSingle().categories

        categoriesConfirmationClient
            .confirmCategories(
                channelId = headers.channelId,
                userId = headers.userId,
                period = categoriesConfirmationRequest.offerDate,
                categoriesToConfirmRequest = CategoriesToConfirmRequest(
                    categories = categoriesConfirmationRequest.categoriesIdsToConfirm.map {
                        CategoryToConfirm(
                            id = it,
                            percentRate = suggestedCategories.first { category -> category.id == it }.percentRate,
                        )
                    }),
            )
            .awaitFirstOrNull()
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        logger.error(e) {
            "Categories confirmation failed for user with id ${headers.userId} and request " +
                    "$categoriesConfirmationRequest"
        }
        throw e
    }

    private companion object : KLogging()
}