# Пример 1

Нашел метод getOfferDetails из проекта 2 (о котором писал в прошлых заданиях) на 150 строк :). Есть его участок, который смешивает формирование двух объектов:

```java
String bannerName = null;
String logoName = null;

for (var banner : offerEntity.getBannerEntityList()) {
    if (banner.getBannerType() == BANNER)
        bannerName = banner.getFileName();
    else if (banner.getBannerType() == LOGO)
        logoName = banner.getFileName();
}
```

```java
String bannerName = offerEntity.getBannerEntityList().stream()
    .filter(banner -> banner.getBannerType() == BANNER)
    .map(BannerEntity::getFileName)
    .findFirst()
    .orElse(null);

String logoName = offerEntity.getBannerEntityList().stream()
    .filter(banner -> banner.getBannerType() == LOGO)
    .map(BannerEntity::getFileName)
    .findFirst()
    .orElse(null);
```

Теперь бросаются в глаза проблемы дизайна:
1) getBannerEntityList вроде бы должен отдавать список баннеров (Banner в имени), но внутри хранятся как баннеры (BANNER), так и логотипы (LOGO). Вполне вероятно, что Banner в имени метода имеет смысл переименовать. Придется уточнять требования и контракт хранимых данных.
2) исходный код не останавливался на первом найденном элементе каждого типа (BANNER/LOGO), поиск шел по всей коллекции. Было ли это задумано? Нужен ли последний найденный элемент? Может наличие нескольких элементов нарушает контракт? Придется уточнять требования и контракт хранимых данных.

Теперь эта логика может разъехаться по отдельным методам:

```java
String bannerName = firstBannerFileName(offer);
String logoName   = firstLogoFileName(offer);


private static String firstBannerFileName(OfferEntity offer) {
    return firstFileNameByType(offerEntity, BannerType.BANNER);
}

private static String firstLogoFileName(OfferEntity offer) {
    return firstFileNameByType(offerEntity, BannerType.LOGO); 
}

private static String firstFileNameByType(OfferEntity offer, BannerType type) {
    Predicate<BannerEntity> byProvidedBannerType = b -> b.getBannerType() == type;
    var banners = Optional.ofNullable(offer.getBannerEntityList()).orElse(List.of())
            .stream()
            .filter(byProvidedBannerType)
            .map(BannerEntity::getFileName)
            .findFirst()
            .orElse(null);
}
```

# Пример 2

Перейдем к участку кода из следующего метода:

```java
...

List<PaymentEntity> payments = new ArrayList<>();
var totalReestrCashback = ZERO;

for (var stat : groupedStatistics) {
    var newPayment = PaymentEntity.builder()
            .partnerEntity(partnerRepository.findById(stat.getPartnerId()).orElseThrow())
            .offerEntity(offerService.getOfferById(stat.getOfferId()))
            .status(WAITING_FOR_RECONCILIATION)
            .totalSum(stat.getTotalSum())
            .totalCashback(stat.getTotalCashback())
            .transactionCount(stat.getTransactionCount())
            .isPaid(false)
            .partnerOrder(1)
            .build();

    totalReestrCashback = totalReestrCashback.add(newPayment.getTotalCashback());
    payments.add(newPayment);
}

...
```

Видим как минимум 2 глобальных ответственности: по сбору payments и по подсчету totalReestrCashback и много вызовов к БД. Внесем правки:

```java
List<PaymentEntity> payments = getPayments(groupedStatistics);
BigDecimal totalReestrCashback = getTotalReestrCashback(payments); // от голого BigDecimal лучше уйти

...

@NotNull
private static BigDecimal getTotalReestrCashback(List<PaymentEntity> payments) {
    return payments.stream().map(PaymentEntity::getTotalCashback).reduce(ZERO, BigDecimal::add);
}

@NotNull
private List<Payment> getPayments(List<OfferStatistics> groupedStatistics) {
    Map<UUID, Partner> partners = getPartners(groupedStatistics); // сокращаем число вызовов к БД
    Map<UUID, Offer> offers = getOffers(groupedStatistics); // сокращаем число вызовов к БД

    return groupedStatistics.stream().map(stat -> PaymentEntity.builder() // тут можно рассмотреть вариант скрывающего детали билдер или конструктор
            .partnerEntity(partners.get(stat.getPartnerId()))
            .offerEntity(offers.get(stat.getOfferId()))
            ...
    ).toList();
}

private Map<UUID, Offer> getOffers(List<OfferStatistics> groupedStatistics) {
    Set<UUID> offerIds = groupedStatistics.stream()
            .map(it-> it.getId())
            .collect(Collectors.toSet());
    return offerService.getAllBy(offerIds).stream()
            .collect(Collectors.toMap(Offer::getId, Function.identity()));
}

@NotNull
private static Map<UUID, PartnerEntity> getPartners(List<OfferStatistics> groupedStatistics) {
    LinkedHashSet<UUID> partnerIds = groupedStatistics.stream()
            .map(OfferStatistics::getPartnerId)
            .filter(Objects::nonNull)
            .collect(Collectors.toCollection(LinkedHashSet::new));

    Map<UUID, PartnerEntity> partnersById = partnerService.getAllBy(partnerIds).stream()
            .collect(Collectors.toMap(PartnerEntity::getId, Function.identity()));

    var missing = partnerIds.stream()
            .filter(byNotExist(partnersById))
            .map(UUID::toString)
            .toList();
    if (!missing.isEmpty()) {
        throw new NotFoundException(NOT_FOUND, "Partners " + String.join(",", missing) + " missing in DB.");
    }

    return partnersById;
}

@NotNull
private static Predicate<UUID> byNotExist(Map<UUID, PartnerEntity> partnersById) {
    return id -> !partnersById.containsKey(id);
}
```

# Пример 3

Было:
```java
try (
    InputStream fis = templateResource.getInputStream();
    XWPFDocument doc = new XWPFDocument(fis);
    ByteArrayOutputStream outputStream = new ByteArrayOutputStream()
) {
    List<XWPFParagraph> paragraphs = doc.getParagraphs();
        for (var p : paragraphs) {
            var buffer = new StringBuilder();
            for (var run : p.getRuns()) {
                var text = run.getText(0);
                if (text != null) buffer.append(text);
            }
            var replaced = replaceAll(buffer.toString(), replacements);
            for (int i = p.getRuns().size() - 1; i >= 0; i--) p.removeRun(i);
            if (!replaced.isEmpty()) p.createRun().setText(replaced, 0);
        }
    
        doc.write(outputStream);
        return new ByteArrayResource(outputStream.toByteArray());
    }
}
```

Стало:

```java
try (
     InputStream fis = resource.getInputStream();
     XWPFDocument doc = new XWPFDocument(fis);
     ByteArrayOutputStream out = new ByteArrayOutputStream()
) {
    doc.getParagraphs().forEach(p -> {
        String original = getParagraphText(p);
        String replaced = applyReplacements(original, replacements);
        rewriteParagraph(p, replaced);
    });

    doc.write(out);
    return new ByteArrayResource(out.toByteArray());
}

...

private String getParagraphText(XWPFParagraph p) {
    return p.getRuns().stream()
            .map(r -> r.getText(0))
            .filter(Objects::nonNull)
            .collect(Collectors.joining());
}

private String applyReplacements(String src, Map<String, String> replacements) {
    String s = src;
    for (var e : replacements.entrySet()) { // получилось читабельнее, чем с reduce
        s = s.replace(e.getKey(), Objects.toString(e.getValue(), ""));
    }
    return s;
}

private void rewriteParagraph(XWPFParagraph p, String text) {
    IntStream.iterate(p.getRuns().size() - 1, i -> i >= 0, i -> i--).forEach(p::removeRun);
    if (!text.isEmpty()) {
        p.createRun().setText(text, 0);
    }
}
```

# Пример 4

Было:

```java
var cashbackSum = ZERO;
var kbSum = ZERO;

for (var projection : paymentTypeSumProjectionList) {

    if (!isNull(projection.getType())) {
        if (projection.getType().equals("cashback"))
            cashbackSum = projection.getSumma().setScale(2, HALF_UP);

        if (projection.getType().equals("kb"))
            kbSum = projection.getSumma().setScale(2, HALF_UP);
    }
}
```

Стало:

```java
var cashbackSum = findSumByType(paymentTypeSumProjectionList, "cashback");
var kbSum = findSumByType(paymentTypeSumProjectionList, "kb");

...

private BigDecimal findSumByType(List<PaymentTypeSumProjection> list, String type) {
    return list.stream()
            .filter(p -> type.equals(p.getType()))
            .map(p -> p.getSum().setScale(2, RoundingMode.HALF_UP))
            .findFirst()
            .orElse(BigDecimal.ZERO);
}
```

# Вывод

Функциональный стиль по природе подразумевает стремление к SRP: будешь писать большие тела внутри функциональных цепочек -> код станет менее понятным, чем без них. Короткие чистые функции складываются в композицию, обеспечивая высокую поддерживаемость (чтение/тестирование/изменение) за счет явного отражения цепочки намерений.

Общая идея, которая хорошо сработала во всех примерах -- сначала сформулировать свои намерения, затем -- кодировать его минимальной функцией с понятным именем (привет самодокументация!).

Удалось избавиться от перемежающейся логики, которая была написана для получения различных частей результата, выделив основные этапа и выстроив их в последовательность. Выделение этапов, в том числе, подталкивает к уменьшению размеров методов, так как из каши появляются вполне себе структурные блоки, которыми проще оперировать.

Что в примерах выше можно было бы улучшить? Отказаться от сырых типов и ужесточить контракты с точки зрения nullability (конечно, Kotlin в этом смысле будет выразительнее, чтобы лишний раз не заниматься filter(Objects::nonNull)). Это позволит еще точнее передавать замысел кода, абстрагируясь от технических деталей.
