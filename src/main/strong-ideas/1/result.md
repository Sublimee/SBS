# Примеры рефакторинга (в соответствующих папках)

## Пример 1

* Убрал nullable переменную progress
* Блоки кода, повышающие ЦС, вынес в методы
* Удалил блок else при проверке loyaltyKey
* 
## Пример 2

* Заменил цикл for на Stream
* Избавился от вложенных if и else

## Пример 3

* Заменил цикл for на Stream
* Избавился от вложенных if и else
* Заменил if на Optional
* Блоки кода, повышающие ЦС, вынес в методы

# Резюме

Цикломатическая сложность показывает сложность программы на основе количества возможных путей ее выполнения. Чем выше ЦС, тем больше тестов потребуется для обеспечения полного покрытия. Таким образом, высокая ЦС усложняет процесс тестирования, а именно требует больше усилий для поддержания актуальности и работоспособности тестовых сценариев. Вот яркий пример из кодовой базы:
```
@ParameterizedTest
@CsvSource(
    "C3,ANDROID,11,58,",
    "M2,ANDROID,11,58,''",
    "M2,ANDROID,11,59,",
    "M2,ANDROID,11,60,",
    "M2,IOS,11,58,",
    "M2,IOS,11,59,",
    "M2,IOS,11,60,",
)
fun `must return correct subtitle due to vary headers`(
```
Очевидно, в тестируемом методе присутствует большое число ветвлений, которое порождает большое число тестов. Какие здесь могут быть проблемы? При добавлении очередного ветвления в коде число тестов, необходимых для обеспечения покрытия метода будет увеличиваться. Также потребуется внести изменения в список аргументов всех ранее написанных тестов. При этом достаточно просто можно пропустить (не добавить) интересующий кейс. При изменении значений (порогов, констант и т.д.) потребуется доработка всех тестов.

Такой код требует рефакторинга, так как является тяжело поддерживаемым. Обычно, уже на этапе написания тестов появляется непреодолимое желание уменьшить его ЦС, чтобы облегчить свои страдания.  

Как добиться снижения ЦС?
1) Использовать синтаксические конструкции и стандартные библиотеки языка: элвис-оператор, non-nullable типы, регекспы и т.д.
2) Разделить код на более мелкие методы.
3) Выносить повторяющиеся блоки кода в отдельные методы.
4) Использовать полиморфизм.
5) Писать код в декларативном стиле.
6) По возможности делать состояние объекта неизменяемым.
7) Применять паттерны проектирования.