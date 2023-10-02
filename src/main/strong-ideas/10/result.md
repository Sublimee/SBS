1. Превращаем лист в словарь, где в качестве ключа идентификатор типа бонусного счета, а в качестве значения - идентификаторы программ лояльности, который подпадают под условие. В строке 2 пытаемся объединить формирование словаря и формирование значения, что ухудшает читаемость.

```
1    }.associate {
2        it.bonusAccountTypeId to it.loyaltyProgramIds.filter { loyaltyProgramId ->
3            programsProperties.isPromotedCashbackProgram(loyaltyProgramId)
4        }
5    }
```
Получение значения лучше вынести для снижения когнитивной нагрузки:

```
1    }.associate {
2        it.bonusAccountTypeId to toFilteredLoyaltyProgramIds(it)
3    }
```

2. Перегруженная вложенными условиями строка  

```
.filter { terms -> cardsWithPromotedCashback.any { card -> card.matches(terms) } }
```

может быть заменена на более простую с помощью функции-расширения:

```
.filter { it.matchesAny(cardsWithPromotedCashback) }
```

Так как такое сопоставление используется повсеместно, то оно может быть организовано таким образом. Если операция не тиражируется, то лучше вынести ее либо в приватный метод, либо в утильный класс.

3. Компактная, но перегруженная вычислениями строка:

```
title = "${TRAILING_ZEROS_REMOVE_FORMATTER.format(category.percentRate)}% ${categoryDirectoryItem.getName()}",
```
    
Лучше вынести ее формирование в метод, тогда и вызов и код ее формирования будут понятнее:

```
...
title = getSectionTitle(category, categoryDirectoryItem),
... 

private fun getSectionTitle(
    category: Category,
    categoryDirectoryItem: CategoryDirectoryItem,
) : String {
    val percentRate = "${TRAILING_ZEROS_REMOVE_FORMATTER.format(category.percentRate)}"
    val categoryDirectoryItemName = categoryDirectoryItem.getName()
    return "$percentRate% $categoryDirectoryItemName"
}
```

4. Всегда стоит рассматривать все возможности, которые предоставляет библиотека, тогда можно записать достаточно неказистый код:

```
verify(categoriesDirectoryClient, times(0)).getCategoriesDirectory(any())
```

в более понятном и читаемом стиле:

```
verifyNoInteractions(categoriesDirectoryClient).getCategoriesDirectory(any())
```


5. В строке 3:

```
1   val supportedAppVersion = summaryProperties.wheelOfFortune.partnerOffersFeatureSupportByOs[headers.os]
2
3   return if (headers.channelId == M2 && supportedAppVersion != null && headers.appVersion < supportedAppVersion) {
```

хотим проверить два условия:

1) что канал запроса пользователя M2
2) что версия приложения пользователя меньше поддерживаемой

однако инородное условие проверки переданных версий из конфигурации (supportedAppVersion != null) выбивает при чтении из колеи. В этом случае лучше спрятать его под капот отдельного метода, как и строку 1:

```
return if (headers.channelId == M2 && isAppVerionSupported(headers) {
```

Как оказалось, SRP можно применять не только к классам и методам целиком, но и к отдельным строкам. Каждая строка в идеале должна выражать одну законченную мысль. В то же время каждая строка не должна быть перегружена. 

Предложения со сложными оборотами подобны в этом смысле сложному витиеватому коду. Если каждое предложение будет кратко и четко выражать свою мысль, то и текст будет считываться легко: вам не придется перечитывать предложения повторно в поисках смысла. Пользователю такого класса будет непросто считывать идею и поддерживать такой код.

Если при чтении кода, который вы не трогали хотя бы неделю, вам приходится заострять внимание на определенных строках, чтобы понять смысл написанного, то это потенциальный кандидат для рефакторинга. Исходя из моей практики чаще всего в роли таких кандидатов выступают:

* сложные выражения внутри логики, написанной в функциональном стиле (пример 1, 2);
* лаконичные, но перегруженные строки(пример 3);
* длинные условия (пример 5).