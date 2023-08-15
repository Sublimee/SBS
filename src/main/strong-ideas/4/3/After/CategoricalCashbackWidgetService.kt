package some.company.mobile.loyalty.promoted.cashback.service.widget

import org.springframework.stereotype.Service
import some.company.mobile.contract.header.Headers
import some.company.mobile.exceptions.InternalException
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties.Companion.CATEGORICAL_CASHBACK_PROGRAM_ID
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.model.Icon
import some.company.mobile.loyalty.promoted.cashback.model.ProgramWidget
import some.company.mobile.loyalty.promoted.cashback.service.PromotedCashbackAvailabilityService
import some.company.mobile.loyalty.promoted.cashback.service.client.model.Category
import some.company.mobile.loyalty.promoted.cashback.service.client.model.WidgetSettings
import some.company.mobile.loyalty.promoted.cashback.service.client.model.getConfirmedWidgetContent
import some.company.mobile.loyalty.promoted.cashback.service.client.model.getSuggestedWidgetContent
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CategoriesProviderService
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CommonProviderService

@Service
class CategoricalCashbackWidgetService(
    private val categoriesProviderService: CategoriesProviderService,
    private val commonProviderService: CommonProviderService,
    private val programsProperties: ProgramsProperties,
    private val promotedCashbackAvailabilityService: PromotedCashbackAvailabilityService,
) : WidgetService {

    override fun getProgramId(): Int {
        return CATEGORICAL_CASHBACK_PROGRAM_ID
    }

    override suspend fun isProgramFeatureActive(headers: Headers): Boolean =
        promotedCashbackAvailabilityService.isProgramFeatureActive(
            headers = headers,
            programId = getProgramId(),
        )

    override suspend fun getProgramWidget(
        headers: Headers,
        period: String,
    ): ProgramWidget {
        val confirmedCategories = categoriesProviderService.getConfirmedCategories(headers, period)
        val widgetSettings = commonProviderService.getWidgetSettings(
            headers = headers,
            programId = getProgramId(),
            period = period,
        )
        return if (confirmedCategories == null) {
            getSuggestedProgramWidget(
                period = period,
                widgetSettings = widgetSettings,
            )
        } else {
            getConfirmedProgramWidget(
                headers = headers,
                period = period,
                widgetSettings = widgetSettings,
                confirmedCategories = confirmedCategories.categories,
            )
        }
    }

    private suspend fun getSuggestedProgramWidget(
        period: String,
        widgetSettings: WidgetSettings,
    ): ProgramWidget = ProgramWidget(
        id = getProgramId(),
        title = widgetSettings.getSuggestedWidgetContent().title!!,
        date = period,
        icons = emptyList(),
        deeplink = String.format(
            programsProperties.getCategoricalCashbackProgramProperties().suggested.deeplinkTemplate,
            period,
        ),
        subtitle = widgetSettings.subtitle,
        backgroundImageURL = widgetSettings.backgroundImageURL,
        iconURL = widgetSettings.iconURL,
        backgroundColor = widgetSettings.getSuggestedWidgetContent().backgroundColor,
        confirmed = false,
    )

    private suspend fun getConfirmedProgramWidget(
        headers: Headers,
        period: String,
        widgetSettings: WidgetSettings,
        confirmedCategories: List<Category>,
    ): ProgramWidget = ProgramWidget(
        id = getProgramId(),
        title = widgetSettings.getConfirmedWidgetContent().title!!,
        date = period,
        icons = getConfirmedProgramWidgetIcons(headers, confirmedCategories),
        deeplink = String.format(
            programsProperties.getCategoricalCashbackProgramProperties().confirmed.deeplinkTemplate,
            period,
        ),
        backgroundColor = widgetSettings.getConfirmedWidgetContent().backgroundColor,
        confirmed = true,
    )

    private suspend fun getConfirmedProgramWidgetIcons(
        headers: Headers,
        confirmedCategories: List<Category>,
    ): List<Icon> {
        val categoriesDirectory = categoriesProviderService.getCategoriesDirectory(headers)

        return confirmedCategories
            .map {
                categoriesDirectory[it.id]
                    ?: throw InternalException.of(LogicErrorCode.CATEGORIES_DIRECTORY_ITEM_NOT_FOUND)
            }
            .map {
                Icon(
                    imageURL = it.getImageURL(),
                    iconPackLink = it.getIconLink(),
                    color = it.getColor(),
                    imageURLSquare = it.getImageURLSquareOrDefault(programsProperties.placeholderImageSquare),
                )
            }
    }
}