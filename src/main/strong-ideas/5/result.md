В примерах [1](1%2FPromotedCashbackAvailabilityService.kt) и [2](2%2FConfirmationService.kt) даны комментарии, которые вытекают из особенностей эксплуатации программы.
В примерах [3](3%2FCardsSectionService.kt) и [4](4%2FCategoriesProviderService.kt) приведены причины, по которым были выбраны соответствующие реализации.

Подводя итог, хочется сказать, что комментарий должен отражать не то, что есть в коде, а то, чего в нем нет. Чистый код позволяет быстро и правильно считать алгоритм, но не более. 

Комментарий может рассказать:
* о причинах выбора того или иного решения, например, почему оно стало deprecated
* о баге в библиотеке/смежной системе/...
* об особенностях, которые вытекают из требований эксплуатации
* и т.д.

Часть задач может решить документация, но она все же не так близка к коду (хранится отдельно от него), как этого бы хотелось.

Комментарии, как и документация, нуждаются в периодическом обслуживании. Качество этого обслуживания зависит сложившейся культуры в рамках компании/команды культуры. Если эта культура низкая, то я бы не рекомендовал использовать в коде комментарии, так как они быстро разъедутся с дизайном. На ревью каждый разработчик должен понимать, что он не только валидирует решение на уровне кода, но и на уровне дизайна.