package some.company.mobile.loyalty.promoted.cashback.service.widget

import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.coroutineScope
import some.company.mobile.contract.header.Headers
import some.company.mobile.loyalty.promoted.cashback.model.ProgramWidget

interface WidgetService {

    suspend fun isProgramFeatureActive(headers: Headers): Boolean

    suspend fun getProgramWidgets(headers: Headers, periods: List<String>): List<ProgramWidget> =
        if (isProgramFeatureActive(headers)) {
            coroutineScope {
                periods
                    .map { period ->
                        async {
                            getProgramWidget(headers, period)
                        }
                    }
                    .awaitAll()
            }
        } else {
            emptyList()
        }

    suspend fun getProgramWidget(headers: Headers, period: String): ProgramWidget

    companion object {
        const val SUGGESTED_WIDGET_PROPERTIES_ID = 1
        const val CONFIRMED_WIDGET_PROPERTIES_ID = 2
    }
}