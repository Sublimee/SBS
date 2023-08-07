package some.company.loyalty.promoted.cashback.controller

import org.junit.jupiter.api.Test
import some.company.loyalty.promoted.cashback.BaseIntegrationTest
import some.company.loyalty.promoted.cashback.docs.SummaryControllerDocs
import some.company.loyalty.promoted.cashback.stubForAvailableProgramsPeriodsClient
import some.company.loyalty.promoted.cashback.stubForCardsApiClientGetMaskedCards
import some.company.loyalty.promoted.cashback.stubForCardsApiClientGetMaskedCards500
import some.company.loyalty.promoted.cashback.stubForCategoriesConfirmationClientGetConfirmedCategories
import some.company.loyalty.promoted.cashback.stubForCategoriesDirectoryClient
import some.company.loyalty.promoted.cashback.stubForCategoriesDirectoryClient500
import some.company.loyalty.promoted.cashback.stubForCategoriesSuggestionClient
import some.company.loyalty.promoted.cashback.stubForCustomerAvailableLoyaltyClient
import some.company.loyalty.promoted.cashback.stubForFeatureToggleApiClient
import some.company.loyalty.promoted.cashback.stubForFeatureToggleApiClient500
import some.company.loyalty.promoted.cashback.stubForLoyaltyApiClientGetBonusAccountList
import some.company.loyalty.promoted.cashback.stubForLoyaltyCardsTermsClient
import some.company.loyalty.promoted.cashback.stubForOffersConfirmationClientGetConfirmedOfferId
import some.company.loyalty.promoted.cashback.stubForOffersDirectoryClient
import some.company.loyalty.promoted.cashback.stubForOffersSuggestionClient
import some.company.loyalty.promoted.cashback.stubForUserInterfaceContentClient
import some.company.loyalty.promoted.cashback.stubForUserInterfaceContentClient500
import some.company.loyalty.promoted.cashback.stubForWidgetsSettingsClient
import some.company.loyalty.promoted.cashback.stubForWidgetsSettingsClient500

class SummaryControllerTest : BaseIntegrationTest() {

    @Test
    fun `must successfully return suggested period categorical cashback summary`() {
        val stubForLoyaltyApiClientGetBonusAccountList =
            wireMockServer.stubForLoyaltyApiClientGetBonusAccountList("bonus-accounts-list-without-kids.json")
        val stubForFeatureToggleApiClient =
            wireMockServer.stubForFeatureToggleApiClient("categorical-cashback.json")
        val stubForCardsApiClientGetMaskedCards =
            wireMockServer.stubForCardsApiClientGetMaskedCards("supported-cards.json")
        val stubForLoyaltyCardsTermsClient =
            wireMockServer.stubForLoyaltyCardsTermsClient("no-card-contract-id.json")
        val stubForCategoriesDirectoryClient =
            wireMockServer.stubForCategoriesDirectoryClient("complete-categories.json")
        val stubForAvailableProgramsPeriodsClient =
            wireMockServer.stubForAvailableProgramsPeriodsClient("suggested.json")
        val stubForUserInterfaceContentClient =
            wireMockServer.stubForUserInterfaceContentClient("correct.json")
        val stubForCategoriesConfirmationClientGetConfirmedCategories =
            wireMockServer.stubForCategoriesConfirmationClientGetConfirmedCategories(
                responseBodyFileName = "no-confirmed-categories.json",
                period = APRIL,
            )
        val stubForCategoriesSuggestionClient =
            wireMockServer.stubForCategoriesSuggestionClient(
                responseBodyFileName = "some-suggested-categories.json",
                period = APRIL,
            )

        val exchange = webTestClient.get()
            .uri("/summary/categorical-cashback?offerDate=$APRIL")
            .androidMobileHeaders()
            .exchange()

        exchange
            .expectStatus().isOk
            .expectBody()
            .json(getExpectedResponse("summary/categorical-cashback/suggested.json"), true)
            .consumeWith(
                SummaryControllerDocs.buildCategoricalCashbackSummarySuggestedResponseSnippet(
                    "summary/categorical-cashback/suggested",
                    invocationSupplier {
                        listOf(
                            getInvocationSpec(
                                "Список бонусных счетов пользователя",
                                "loyalty-api",
                                stubForLoyaltyApiClientGetBonusAccountList,
                            ),
                            getInvocationSpec(
                                "Программы повышенного кэшбэка и соответствующие им периоды действия",
                                "UWSAvailablePeriods",
                                stubForAvailableProgramsPeriodsClient
                            ),
                            getInvocationSpec(
                                "Наличие у пользователя соответствующего ФТ",
                                "feature-toggle-api",
                                stubForFeatureToggleApiClient
                            ),
                            getInvocationSpec(
                                "Список карт пользователя",
                                "cards-api",
                                stubForCardsApiClientGetMaskedCards
                            ),
                            getInvocationSpec(
                                "Справочник условий повышенного кэшбэка по картам",
                                "UWSLoyaltyCardInfo",
                                stubForLoyaltyCardsTermsClient
                            ),
                            getInvocationSpec(
                                "Справочник категорий",
                                "UWSCustomerLoyaltyCategories",
                                stubForCategoriesDirectoryClient
                            ),
                            getInvocationSpec(
                                "Список выбранных категорий",
                                "UWSCustomerConfirmationsCCB",
                                stubForCategoriesConfirmationClientGetConfirmedCategories
                            ),
                            getInvocationSpec(
                                "Список предложенных для выбора категорий",
                                "UWSCustomerCategoriesCCB",
                                stubForCategoriesSuggestionClient
                            ),
                            getInvocationSpec(
                                "Конфигурация статичных полей",
                                "UWSCustomerAdvertOffers",
                                stubForUserInterfaceContentClient
                            )
                        )
                    }
                )
            )
    }

    @Test
    fun `must successfully return confirmed period categorical cashback summary`() {
        val stubForLoyaltyApiClientGetBonusAccountList =
            wireMockServer.stubForLoyaltyApiClientGetBonusAccountList("bonus-accounts-list-without-kids.json")
        val stubForFeatureToggleApiClient =
            wireMockServer.stubForFeatureToggleApiClient("categorical-cashback.json")
        val stubForCardsApiClientGetMaskedCards =
            wireMockServer.stubForCardsApiClientGetMaskedCards("supported-cards.json")
        val stubForLoyaltyCardsTermsClient =
            wireMockServer.stubForLoyaltyCardsTermsClient("no-card-contract-id.json")
        val stubForCategoriesDirectoryClient =
            wireMockServer.stubForCategoriesDirectoryClient("complete-categories.json")
        val stubForAvailableProgramsPeriodsClient =
            wireMockServer.stubForAvailableProgramsPeriodsClient("confirmed.json")
        val stubForUserInterfaceContentClient =
            wireMockServer.stubForUserInterfaceContentClient("correct.json")
        val stubForCategoriesConfirmationClientGetConfirmedCategories =
            wireMockServer.stubForCategoriesConfirmationClientGetConfirmedCategories(
                responseBodyFileName = "some-confirmed-categories.json",
                period = MARCH,
            )

        val exchange = webTestClient.get()
            .uri("/summary/categorical-cashback?offerDate=$MARCH")
            .androidMobileHeaders()
            .exchange()

        exchange
            .expectStatus().isOk
            .expectBody()
            .json(getExpectedResponse("summary/categorical-cashback/confirmed.json"), true)
            .consumeWith(
                SummaryControllerDocs.buildCategoricalCashbackSummaryConfirmedResponseSnippet(
                    "summary/categorical-cashback/confirmed",
                    invocationSupplier {
                        listOf(
                            getInvocationSpec(
                                "Список бонусных счетов пользователя",
                                "loyalty-api",
                                stubForLoyaltyApiClientGetBonusAccountList,
                            ),
                            getInvocationSpec(
                                "Программы повышенного кэшбэка и соответствующие им периоды действия",
                                "UWSAvailablePeriods",
                                stubForAvailableProgramsPeriodsClient
                            ),
                            getInvocationSpec(
                                "Наличие у пользователя соответствующего ФТ",
                                "feature-toggle-api",
                                stubForFeatureToggleApiClient
                            ),
                            getInvocationSpec(
                                "Список карт пользователя",
                                "cards-api",
                                stubForCardsApiClientGetMaskedCards
                            ),
                            getInvocationSpec(
                                "Справочник условий повышенного кэшбэка по картам",
                                "UWSLoyaltyCardInfo",
                                stubForLoyaltyCardsTermsClient
                            ),
                            getInvocationSpec(
                                "Справочник категорий",
                                "UWSCustomerLoyaltyCategories",
                                stubForCategoriesDirectoryClient
                            ),
                            getInvocationSpec(
                                "Список выбранных категорий",
                                "UWSCustomerConfirmationsCCB",
                                stubForCategoriesConfirmationClientGetConfirmedCategories
                            ),
                            getInvocationSpec(
                                "Конфигурация статичных полей",
                                "UWSCustomerAdvertOffers",
                                stubForUserInterfaceContentClient
                            )
                        )
                    }
                )
            )
    }

    @Test
    fun `must fail while getting suggested categorical cashback summary due to incomplete categories directory`() {
        wireMockServer.stubForLoyaltyApiClientGetBonusAccountList("bonus-accounts-list-without-kids.json")
        wireMockServer.stubForFeatureToggleApiClient("categorical-cashback.json")
        wireMockServer.stubForCardsApiClientGetMaskedCards("supported-cards.json")
        wireMockServer.stubForLoyaltyCardsTermsClient("no-card-contract-id.json")
        wireMockServer.stubForCategoriesDirectoryClient("incomplete-categories.json")
        wireMockServer.stubForAvailableProgramsPeriodsClient("suggested.json")
        wireMockServer.stubForCategoriesConfirmationClientGetConfirmedCategories(
            responseBodyFileName = "no-confirmed-categories.json",
            period = APRIL,
        )
        wireMockServer.stubForUserInterfaceContentClient("correct.json")
        wireMockServer.stubForCategoriesSuggestionClient(
            responseBodyFileName = "some-suggested-categories.json",
            period = APRIL,
        )

        val exchange = webTestClient.get()
            .uri("/summary/categorical-cashback?offerDate=$APRIL")
            .androidMobileHeaders()
            .exchange()

        exchange
            .expectStatus().is5xxServerError
            .expectBody()
            .consumeWith(errorConsumer("summary/categorical-cashback/internal-server-error"))
    }

    @Test
    fun `must fail while getting categorical cashback summary due to user interface content client error`() {
        wireMockServer.stubForLoyaltyApiClientGetBonusAccountList("bonus-accounts-list-without-kids.json")
        wireMockServer.stubForFeatureToggleApiClient("categorical-cashback.json")
        wireMockServer.stubForCardsApiClientGetMaskedCards("supported-cards.json")
        wireMockServer.stubForLoyaltyCardsTermsClient("no-card-contract-id.json")
        wireMockServer.stubForAvailableProgramsPeriodsClient("confirmed.json")
        wireMockServer.stubForCategoriesDirectoryClient("complete-categories.json")
        wireMockServer.stubForUserInterfaceContentClient500()
        wireMockServer.stubForCategoriesConfirmationClientGetConfirmedCategories(
            responseBodyFileName = "some-confirmed-categories.json",
            period = MARCH,
        )

        val exchange = webTestClient.get()
            .uri("/summary/categorical-cashback?offerDate=$MARCH")
            .androidMobileHeaders()
            .exchange()

        exchange
            .expectStatus().is5xxServerError
            .expectBody()
            .json(getExpectedResponse("summary/categorical-cashback/internal-server-error.json"))
            .consumeWith(errorConsumer("summary/categorical-cashback/internal-server-error"))
    }

    @Test
    fun `must fail while getting categorical cashback summary due to promoted cashback unavailable`() {
        wireMockServer.stubForLoyaltyApiClientGetBonusAccountList("bonus-accounts-list-without-kids.json")
        wireMockServer.stubForFeatureToggleApiClient("categorical-cashback.json")
        wireMockServer.stubForCardsApiClientGetMaskedCards("not-supported-cards.json")
        wireMockServer.stubForLoyaltyCardsTermsClient("no-card-contract-id.json")
        wireMockServer.stubForAvailableProgramsPeriodsClient("confirmed.json")

        val exchange = webTestClient.get()
            .uri("/summary/categorical-cashback?offerDate=$MARCH")
            .androidMobileHeaders()
            .exchange()

        exchange
            .expectStatus().is5xxServerError
            .expectBody()
            .json(getExpectedResponse("summary/categorical-cashback/internal-server-error.json"))
    }

    @Test
    fun `must fail while getting categorical cashback summary due to cards-api error`() {
        wireMockServer.stubForLoyaltyApiClientGetBonusAccountList("bonus-accounts-list-without-kids.json")
        wireMockServer.stubForCardsApiClientGetMaskedCards500()
        wireMockServer.stubForLoyaltyCardsTermsClient("no-card-contract-id.json")

        val exchange = webTestClient.get()
            .uri("/summary/categorical-cashback?offerDate=$MARCH")
            .androidMobileHeaders()
            .exchange()

        exchange
            .expectStatus().is5xxServerError
            .expectBody()
            .json(getExpectedResponse("summary/categorical-cashback/internal-server-error.json"))
    }

    @Test
    fun `must fail while getting categorical cashback summary due to categories directory client error`() {
        wireMockServer.stubForLoyaltyApiClientGetBonusAccountList("bonus-accounts-list-without-kids.json")
        wireMockServer.stubForFeatureToggleApiClient("categorical-cashback.json")
        wireMockServer.stubForCardsApiClientGetMaskedCards("supported-cards.json")
        wireMockServer.stubForLoyaltyCardsTermsClient("no-card-contract-id.json")
        wireMockServer.stubForAvailableProgramsPeriodsClient("confirmed.json")
        wireMockServer.stubForCategoriesDirectoryClient500()
        wireMockServer.stubForCategoriesConfirmationClientGetConfirmedCategories(
            responseBodyFileName = "some-confirmed-categories.json",
            period = MARCH,
        )

        val exchange = webTestClient.get()
            .uri("/summary/categorical-cashback?offerDate=$MARCH")
            .androidMobileHeaders()
            .exchange()

        exchange
            .expectStatus().is5xxServerError
            .expectBody()
            .json(getExpectedResponse("summary/categorical-cashback/internal-server-error.json"))
    }

    @Test
    fun `must successfully return suggested programs summary`() {
        val stubForLoyaltyApiClientGetBonusAccountList =
            wireMockServer.stubForLoyaltyApiClientGetBonusAccountList("bonus-accounts-list-without-kids.json")
        val stubForWidgetsSettingsClient =
            wireMockServer.stubForWidgetsSettingsClient("april.json")
        val stubForFeatureToggleApiClient =
            wireMockServer.stubForFeatureToggleApiClient("all-programs.json")
        val stubForCardsApiClientGetMaskedCards =
            wireMockServer.stubForCardsApiClientGetMaskedCards("supported-cards.json")
        val stubForLoyaltyCardsTermsClient =
            wireMockServer.stubForLoyaltyCardsTermsClient("no-card-contract-id.json")
        val stubForAvailableProgramsPeriodsClient =
            wireMockServer.stubForAvailableProgramsPeriodsClient("suggested.json")
        val stubForCategoriesConfirmationClientGetConfirmedCategories =
            wireMockServer.stubForCategoriesConfirmationClientGetConfirmedCategories(
                responseBodyFileName = "no-confirmed-categories.json",
                period = APRIL,
            )
        val stubForOffersConfirmationClientGetConfirmedOfferId =
            wireMockServer.stubForOffersConfirmationClientGetConfirmedOfferId(
                responseBodyFileName = "no-confirmed-offer.json",
                period = APRIL,
            )
        val stubForUserInterfaceContentClient =
            wireMockServer.stubForUserInterfaceContentClient("correct.json")

        val exchange = webTestClient.get()
            .uri("/summary/programs?bonusAccountTypeId=180")
            .androidMobileHeaders()
            .exchange()

        exchange
            .expectStatus().isOk
            .expectBody()
            .json(getExpectedResponse("summary/programs/suggested.json"))
            .consumeWith(
                SummaryControllerDocs.buildProgramsSummaryResponse(
                    "summary/programs",
                    invocationSupplier {
                        listOf(
                            getInvocationSpec(
                                "Список бонусных счетов пользователя",
                                "loyalty-api",
                                stubForLoyaltyApiClientGetBonusAccountList,
                            ),
                            getInvocationSpec(
                                "Настройки виджетов",
                                "UWSAttractiveOffers",
                                stubForWidgetsSettingsClient
                            ),
                            getInvocationSpec(
                                "Наличие у пользователя соответствующих ФТ",
                                "feature-toggle-api",
                                stubForFeatureToggleApiClient
                            ),
                            getInvocationSpec(
                                "Список карт пользователя",
                                "cards-api",
                                stubForCardsApiClientGetMaskedCards
                            ),
                            getInvocationSpec(
                                "Справочник условий повышенного кэшбэка по картам",
                                "UWSLoyaltyCardInfo",
                                stubForLoyaltyCardsTermsClient
                            ),
                            getInvocationSpec(
                                "Программы повышенного кэшбэка и соответствующие им периоды действия",
                                "UWSAvailablePeriods",
                                stubForAvailableProgramsPeriodsClient
                            ),
                            getInvocationSpec(
                                "Список выбранных категорий",
                                "UWSCustomerConfirmationsCCB",
                                stubForCategoriesConfirmationClientGetConfirmedCategories
                            ),
                            getInvocationSpec(
                                "Список подтвержденных офферов",
                                "UWSCustomerConfirmationsOffer",
                                stubForOffersConfirmationClientGetConfirmedOfferId
                            ),
                            getInvocationSpec(
                                "Конфигурация статичных полей",
                                "UWSCustomerAdvertOffers",
                                stubForUserInterfaceContentClient
                            )
                        )
                    }
                )
            )
    }

    @Test
    fun `must successfully return confirmed programs summary`() {
        wireMockServer.stubForLoyaltyApiClientGetBonusAccountList("bonus-accounts-list-without-kids.json")
        wireMockServer.stubForWidgetsSettingsClient("march.json")
        wireMockServer.stubForFeatureToggleApiClient("all-programs.json")
        wireMockServer.stubForCardsApiClientGetMaskedCards("supported-cards.json")
        wireMockServer.stubForLoyaltyCardsTermsClient("no-card-contract-id.json")
        wireMockServer.stubForAvailableProgramsPeriodsClient("confirmed.json")
        wireMockServer.stubForCategoriesDirectoryClient("complete-categories.json")
        wireMockServer.stubForUserInterfaceContentClient("correct.json")
        wireMockServer.stubForCategoriesConfirmationClientGetConfirmedCategories(
            responseBodyFileName = "some-confirmed-categories.json",
            period = MARCH,
        )
        wireMockServer.stubForOffersConfirmationClientGetConfirmedOfferId(
            responseBodyFileName = "confirmed-offer.json",
            period = MARCH,
        )
        wireMockServer.stubForOffersDirectoryClient(
            responseBodyFileName = "some-offers.json",
            period = MARCH,
        )
        wireMockServer.stubForOffersSuggestionClient(
            responseBodyFileName = "some-offers.json",
            period = MARCH,
        )

        val exchange = webTestClient.get()
            .uri("/summary/programs?bonusAccountTypeId=180")
            .androidMobileHeaders()
            .exchange()

        exchange
            .expectStatus().isOk
            .expectBody()
            .json(getExpectedResponse("summary/programs/confirmed.json"), true)
    }

    @Test
    fun `must successfully return empty programs response due to feature-toggle-api error`() {
        wireMockServer.stubForLoyaltyApiClientGetBonusAccountList("bonus-accounts-list-without-kids.json")
        wireMockServer.stubForWidgetsSettingsClient("april.json")
        wireMockServer.stubForFeatureToggleApiClient500()
        wireMockServer.stubForCardsApiClientGetMaskedCards("supported-cards.json")
        wireMockServer.stubForLoyaltyCardsTermsClient("no-card-contract-id.json")
        wireMockServer.stubForAvailableProgramsPeriodsClient("confirmed.json")
        wireMockServer.stubForUserInterfaceContentClient("correct.json")

        val exchange = webTestClient.get()
            .uri("/summary/programs?bonusAccountTypeId=180")
            .androidMobileHeaders()
            .exchange()

        exchange
            .expectStatus().isOk
            .expectBody()
            .json(getExpectedResponse("summary/programs/empty.json"))
    }

    @Test
    fun `must fail while getting programs summary due to promoted cashback unavailable`() {
        wireMockServer.stubForLoyaltyApiClientGetBonusAccountList("bonus-accounts-list-without-kids.json")
        wireMockServer.stubForCardsApiClientGetMaskedCards("not-supported-cards.json")
        wireMockServer.stubForLoyaltyCardsTermsClient("no-card-contract-id.json")

        val exchange = webTestClient.get()
            .uri("/summary/programs?bonusAccountTypeId=180")
            .androidMobileHeaders()
            .exchange()

        exchange
            .expectStatus().is5xxServerError
            .expectBody()
            .json(getExpectedResponse("summary/programs/not-supported.json"))
            .consumeWith(errorConsumer("summary/programs/not-supported"))
    }


    @Test
    fun `must fail while getting programs summary due to widget settings service error`() {
        wireMockServer.stubForLoyaltyApiClientGetBonusAccountList("bonus-accounts-list-without-kids.json")
        wireMockServer.stubForWidgetsSettingsClient500()
        wireMockServer.stubForFeatureToggleApiClient("all-programs.json")
        wireMockServer.stubForCardsApiClientGetMaskedCards("supported-cards.json")
        wireMockServer.stubForLoyaltyCardsTermsClient("no-card-contract-id.json")
        wireMockServer.stubForAvailableProgramsPeriodsClient("suggested.json")
        wireMockServer.stubForCategoriesConfirmationClientGetConfirmedCategories(
            responseBodyFileName = "no-confirmed-categories.json",
            period = APRIL,
        )

        val exchange = webTestClient.get()
            .uri("/summary/programs?bonusAccountTypeId=180")
            .androidMobileHeaders()
            .exchange()

        exchange
            .expectStatus().is5xxServerError
            .expectBody()
            .json(getExpectedResponse("summary/programs/internal-server-error.json"))
    }

    @Test
    fun `must fail while getting programs summary due to cards-api error`() {
        wireMockServer.stubForLoyaltyApiClientGetBonusAccountList("bonus-accounts-list-without-kids.json")
        wireMockServer.stubForWidgetsSettingsClient("april.json")
        wireMockServer.stubForFeatureToggleApiClient("categorical-cashback.json")
        wireMockServer.stubForCardsApiClientGetMaskedCards500()
        wireMockServer.stubForLoyaltyCardsTermsClient("no-card-contract-id.json")

        val exchange = webTestClient.get()
            .uri("/summary/programs?bonusAccountTypeId=180")
            .androidMobileHeaders()
            .exchange()

        exchange
            .expectStatus().is5xxServerError
            .expectBody()
            .json(getExpectedResponse("summary/programs/internal-server-error.json"))
            .consumeWith(errorConsumer("summary/programs/internal-server-error"))
    }

    @Test
    fun `must fail while getting programs summary due to category directory service error`() {
        wireMockServer.stubForLoyaltyApiClientGetBonusAccountList("bonus-accounts-list-without-kids.json")
        wireMockServer.stubForWidgetsSettingsClient("april.json")
        wireMockServer.stubForFeatureToggleApiClient("categorical-cashback.json")
        wireMockServer.stubForCardsApiClientGetMaskedCards("supported-cards.json")
        wireMockServer.stubForLoyaltyCardsTermsClient("no-card-contract-id.json")
        wireMockServer.stubForAvailableProgramsPeriodsClient("confirmed.json")
        wireMockServer.stubForCategoriesDirectoryClient500()
        wireMockServer.stubForCategoriesConfirmationClientGetConfirmedCategories(
            responseBodyFileName = "some-confirmed-categories.json",
            period = MARCH,
        )

        val exchange = webTestClient.get()
            .uri("/summary/programs?bonusAccountTypeId=180")
            .androidMobileHeaders()
            .exchange()

        exchange
            .expectStatus().is5xxServerError
            .expectBody()
            .json(getExpectedResponse("summary/programs/internal-server-error.json"))
    }
}