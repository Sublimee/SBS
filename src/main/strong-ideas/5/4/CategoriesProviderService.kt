import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.reactive.awaitFirstOrNull
import kotlinx.coroutines.reactive.awaitSingle
import mu.KLogging
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Service
import some.company.mobile.cache.aspect.annotation.CacheEvictAsync
import some.company.mobile.cache.aspect.annotation.CacheableAsync
import some.company.mobile.contract.header.Headers
import some.company.mobile.exceptions.InternalException
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.CATEGORIES_CONFIRMATION_REQUEST_OFFER_DATE_CACHE_KEY_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.CATEGORIES_DIRECTORY_CACHE_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.CONFIRMED_CATEGORIES_CACHE_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.OFFER_DATE_CACHE_KEY_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.PARAMETERS_INDEPENDENT_CACHE_KEY_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.SUGGESTED_CATEGORIES_CACHE_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.CacheConfiguration.Companion.USER_ID_CACHE_KEY_NAME
import some.company.mobile.loyalty.promoted.cashback.configuration.MaplProperties
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.model.CategoriesConfirmationRequest
import some.company.mobile.loyalty.promoted.cashback.service.client.model.CategoryDirectoryItem
import some.company.mobile.loyalty.promoted.cashback.service.client.model.CategoryToConfirm
import some.company.mobile.loyalty.promoted.cashback.service.client.model.CategoriesToConfirmRequest
import some.company.mobile.loyalty.promoted.cashback.service.client.model.ConfirmedCategories
import some.company.mobile.loyalty.promoted.cashback.service.client.model.SuggestedCategories
import some.company.mobile.loyalty.promoted.cashback.service.client.program.categorical.CategoriesConfirmationClient
import some.company.mobile.loyalty.promoted.cashback.service.client.program.categorical.CategoriesDirectoryClient
import some.company.mobile.loyalty.promoted.cashback.service.client.program.categorical.CategoriesSuggestionClient

@Service
class CategoriesProviderService {

    ...

    /**
     * Бизнес попросил предсказуемости очистки кэша, чтобы он был гарантированно предсказуемо обновлен в начале каждого 
     * часа. Независимо от настройки времени жизни записей (ttl) в начале каждого часа будут запрошены свежие данные.  
     */
    @Scheduled(cron = "@hourly")
    @CacheEvictAsync(
        cacheNames = [CATEGORIES_DIRECTORY_CACHE_NAME],
        allEntries = true,
        ignoreCacheError = true,
    )
    suspend fun evictCategoriesDirectoryCache() {
        logger.info { "$CATEGORIES_DIRECTORY_CACHE_NAME cache evicted" }
    }

    private companion object : KLogging()
}