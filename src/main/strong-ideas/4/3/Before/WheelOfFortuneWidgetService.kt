package some.company.mobile.loyalty.promoted.cashback.service.widget

import org.springframework.stereotype.Service
import some.company.mobile.contract.header.Headers
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties.Companion.WHEEL_OF_FORTUNE_PROGRAM_ID
import some.company.mobile.loyalty.promoted.cashback.model.Icon
import some.company.mobile.loyalty.promoted.cashback.model.ProgramWidget
import some.company.mobile.loyalty.promoted.cashback.service.PromotedCashbackAvailabilityService
import some.company.mobile.loyalty.promoted.cashback.service.client.model.OfferDirectoryItem
import some.company.mobile.loyalty.promoted.cashback.service.client.model.WidgetSettings
import some.company.mobile.loyalty.promoted.cashback.service.client.model.getConfirmedWidgetContent
import some.company.mobile.loyalty.promoted.cashback.service.client.model.getSuggestedWidgetContent
import some.company.mobile.loyalty.promoted.cashback.service.proxy.CommonProviderService
import some.company.mobile.loyalty.promoted.cashback.service.proxy.WheelOfFortuneProviderService
import some.company.mobile.loyalty.promoted.cashback.util.DateTimeUtils.getPrepositionalMonthName

@Service
class WheelOfFortuneWidgetService(
    private val promotedCashbackAvailabilityService: PromotedCashbackAvailabilityService,
    private val commonProviderService: CommonProviderService,
    private val programsProperties: ProgramsProperties,
    private val wheelOfFortuneProviderService: WheelOfFortuneProviderService,
) : WidgetService {

    override suspend fun isProgramFeatureActive(headers: Headers): Boolean =
        promotedCashbackAvailabilityService.isProgramFeatureActive(
            headers = headers,
            programId = WHEEL_OF_FORTUNE_PROGRAM_ID,
        )

    override suspend fun getProgramWidget(headers: Headers, period: String): ProgramWidget {
        val confirmedOfferId = wheelOfFortuneProviderService.getConfirmedOfferId(headers, period)
        val widgetSettings = commonProviderService.getWidgetSettings(
            headers = headers,
            programId = WHEEL_OF_FORTUNE_PROGRAM_ID,
            period = period,
        )
        return if (confirmedOfferId == null) {
            getSuggestedProgramWidget(
                period = period,
                widgetSettings = widgetSettings,
            )
        } else {
            getConfirmedProgramWidget(
                headers = headers,
                period = period,
                widgetSettings = widgetSettings,
                confirmedOfferId = confirmedOfferId,
            )
        }
    }

    private suspend fun getSuggestedProgramWidget(
        period: String,
        widgetSettings: WidgetSettings,
    ): ProgramWidget = ProgramWidget(
        id = WHEEL_OF_FORTUNE_PROGRAM_ID,
        title = widgetSettings.getSuggestedWidgetContent().title!!,
        date = period,
        icons = emptyList(),
        deeplink = String.format(
            programsProperties.getWheelOfFortuneProgramProperties().suggested.deeplinkTemplate,
            period
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
        confirmedOfferId: Int?
    ): ProgramWidget {
        val confirmedWidgetProperties = programsProperties.getWheelOfFortuneProgramProperties().confirmed
        val confirmedOfferDirectoryItem = getConfirmedOfferDirectoryItem(headers, period, confirmedOfferId)

        return ProgramWidget(
            id = WHEEL_OF_FORTUNE_PROGRAM_ID,
            title = String.format(
                confirmedWidgetProperties.titleTemplate!!,
                confirmedOfferDirectoryItem.content.confirmedOfferWidgetTitlePrefix,
                getPrepositionalMonthName(period),
            ),
            date = period,
            icons = listOf(
                Icon(
                    imageURL = confirmedOfferDirectoryItem.content.partnerIconReplacementURL,
                    imageURLSquare = confirmedOfferDirectoryItem.content.partnerIconReplacementURL,
                )
            ),
            deeplink = String.format(confirmedWidgetProperties.deeplinkTemplate, period),
            backgroundColor = widgetSettings.getConfirmedWidgetContent().backgroundColor,
            confirmed = true,
        )
    }

    private suspend fun getConfirmedOfferDirectoryItem(
        headers: Headers,
        period: String,
        confirmedOfferId: Int?,
    ): OfferDirectoryItem = wheelOfFortuneProviderService.getOffersDirectory(headers, period)[confirmedOfferId]!!
}