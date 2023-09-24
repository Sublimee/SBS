package some.company.mobile.loyalty.promoted.cashback.service

import some.company.mobile.contract.header.Headers
import some.company.mobile.exceptions.InternalException
import some.company.mobile.loyalty.promoted.cashback.configuration.SummaryProperties
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.model.Button
import some.company.mobile.loyalty.promoted.cashback.model.CategoriesSection
import some.company.mobile.loyalty.promoted.cashback.model.CategoryRepresentation
import some.company.mobile.loyalty.promoted.cashback.service.client.model.Category
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CategoriesProviderService
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CommonProviderService

open class AbstractSummary(
    private val categoriesProviderService: CategoriesProviderService,
    private val categoryRepresentationService: CategoryRepresentationService,
    private val commonProviderService: CommonProviderService,
    private val summaryProperties: SummaryProperties,
) {

    suspend fun agreementTermsButton(headers: Headers) = Button(
        title = summaryProperties.categoricalCashback.agreementTermsTitle,
        documentUrl = commonProviderService.getUserInterfaceContent(headers).categoricalCashbackTermsDocumentURL,
    )

    suspend fun getCategoriesSection(
        headers: Headers,
        userCategories: List<Category>,
        acceptanceThreshold: Int? = null,
    ) = CategoriesSection(
        categories = getUserCategoriesRepresentation(headers, userCategories),
        acceptanceThreshold = acceptanceThreshold,
    )

    private suspend fun getUserCategoriesRepresentation(
        headers: Headers,
        userCategories: List<Category>,
    ): List<CategoryRepresentation> {
        val categoriesDirectory = categoriesProviderService.getCategoriesDirectory(headers)
        return userCategories
            .sortedByDescending { it.priority }
            .map {
                it to (categoriesDirectory[it.id]
                    ?: throw InternalException.of(LogicErrorCode.CATEGORIES_DIRECTORY_ITEM_NOT_FOUND))
            }
            .map { (category, categoryDirectoryItem) ->
                categoryRepresentationService.toRepresentation(headers, category, categoryDirectoryItem)
            }
    }

}
