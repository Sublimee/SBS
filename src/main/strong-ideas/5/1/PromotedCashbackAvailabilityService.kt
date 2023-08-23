import kotlinx.coroutines.async
import kotlinx.coroutines.coroutineScope
import mu.KLogging
import org.springframework.stereotype.Service
import some.company.mobile.contract.header.Headers
import some.company.mobile.exceptions.BusinessException
import some.company.mobile.exceptions.InternalException
import some.company.mobile.loyalty.promoted.cashback.configuration.ProgramsProperties
import some.company.mobile.loyalty.promoted.cashback.exception.LogicErrorCode
import some.company.mobile.loyalty.promoted.cashback.model.PromotedCashbackAvailability
import some.company.mobile.loyalty.promoted.cashback.service.client.model.ProgramPeriods
import some.company.mobile.loyalty.promoted.cashback.service.client.model.PromotedCashbackCardTerms
import some.company.mobile.loyalty.promoted.cashback.service.proxy.AvailabilityProviderService
import some.company.mobile.loyalty.promoted.cashback.service.proxy.FeatureToggleApiService

/**
 * Класс предоставляет информацию о доступности клиенту повышенного кэшбэка (ПК) в целом и конкретных программ ПК в
 * частности. Разделение обусловлено использованием двух независимых групп сервисов: одна группа сервисов бэкенда
 * используется для определения наличия необходимых условий, чтобы предоставить пользователю ПК, а вторая группа
 * сервисов бэкенда и конфигурационный сервис мидл-слоя используются для определения наличия необходимых условий для
 * предоставления возможности использования конкретной программы ПК.
 *
 * Таким образом, возможна ситуация, когда пользователю потенциально доступен ПК, но недоступна ни одна конкретная
 * программа ПК.
 *
 * Можно ли сразу проверять доступность клиенту ПК и хотя бы одной программы ПК? На момент написания комментария
 * нагрузка, которую могут держать сервисы бэкенда, не позволяет это сделать. Разнесение во времени проверок позволяет
 * снизить нагрузку и в некоторых случаях не делать лишних вызовов для определения доступности конкретных программ ПК.
 */
@Service
class PromotedCashbackAvailabilityService(
    private val availabilityProviderService: AvailabilityProviderService,
    private val featureToggleApiService: FeatureToggleApiService,
    private val userCardsTermsService: UserCardsTermsService,
    private val programsProperties: ProgramsProperties,
) {

    suspend fun getPromotedCashbackAvailability(headers: Headers): PromotedCashbackAvailability = try {
        val userCardsTerms: List<PromotedCashbackCardTerms> =
            userCardsTermsService.getUserPromotedCashbackCardsTerms(headers)

        PromotedCashbackAvailability(
            isAvailable = userCardsTerms.isNotEmpty(),
            userCardsTerms = userCardsTerms,
        )
    } catch (e: Exception) {
        logger.error(e) { "Failed getting promoted cashback availability for user with id ${headers.userId}" }
        throw BusinessException.of(LogicErrorCode.PROMOTED_CASHBACK_AVAILABILITY_FETCH_ERROR)
    }

    suspend fun isPromotedCashbackProgramAvailable(
        headers: Headers,
        programId: Int,
        offerDate: String,
    ): Boolean = coroutineScope {
        if (!programsProperties.isPromotedCashbackProgramId(programId)) {
            false
        } else {
            val availableProgramsPeriodsDeferred = async { getAvailableProgramsPeriods(headers) }
            val isProgramFeatureActiveDeferred = async { isProgramFeatureActive(headers, programId) }

            val isProgramProvided: Boolean = isProgramProvided(headers, programId)

            val isOfferDateValid = availableProgramsPeriodsDeferred.await()
                .find { it.programId == programId }?.periods?.contains(offerDate)

            isProgramFeatureActiveDeferred.await() && isProgramProvided && isOfferDateValid == true
        }
    }

    suspend fun checkPromotedCashbackProgramAvailable(
        headers: Headers,
        programId: Int,
        offerDate: String,
    ) {
        val isPromotedCashbackProgramAvailable = isPromotedCashbackProgramAvailable(
            headers = headers,
            programId = programId,
            offerDate = offerDate,
        )
        if (!isPromotedCashbackProgramAvailable) {
            throw InternalException.of(LogicErrorCode.PROMOTED_CASHBACK_PROGRAM_NOT_AVAILABLE)
        }
    }

    suspend fun getAvailableProgramsPeriods(headers: Headers): List<ProgramPeriods> =
        availabilityProviderService.getAvailableProgramsPeriods(headers)

    suspend fun isProgramFeatureActive(
        headers: Headers,
        programId: Int,
    ): Boolean = featureToggleApiService.hasFeature(
        headers = headers,
        feature = programsProperties.propertiesById["$programId"]!!.feature,
    )

    private suspend fun isProgramProvided(
        headers: Headers,
        programId: Int,
    ): Boolean {
        val promotedCashbackAvailability: PromotedCashbackAvailability = getPromotedCashbackAvailability(headers)
        val supportedProgramIds: List<Int> =
            promotedCashbackAvailability.userCardsTerms.flatMap { it.promotedCashbackProgramIds }

        return supportedProgramIds
            .toSet()
            .contains(programId)
    }

    private companion object : KLogging()
}