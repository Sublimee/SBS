## **2. Уровень классов.**

### **2.1. Класс слишком большой (нарушение SRP), или в программе создаётся слишком много его инстансов (подумайте, почему это плохой признак).**

Нарушение SRP [CardCashbackTariffService.java](CardCashbackTariffService.java): пытаемся уместить в одном классе схожие функциональности, но предназначенные для разных экранов. Требуется разделить функциональность на два класса, а необходимую общую функциональность вынести в абстрактный класс. Решение выполнено на скорую руку, быстро покрывается тестами для обеспечения покрытия, но абсолютно не поддерживаемо. 

### **2.2. Класс слишком маленький или делает слишком мало.**

В одном из наших сервисов мы обращаемся к более чем 10 сервисам бэкенда для предоставления двух программ лояльности (сразу возникает риторический вопрос, а правильно ли спроектированы сервисы бэкенда, раз их требуется столько много?). Для того чтобы сделать удобную обертку над каждым из них можно сделать по отдельному сервису. В таком варианте классов получается слишком много и родственная функциональность излишне дробится. Лучшим решением выглядит разбиение всего скоупа сервисов на близкие по решаемой задаче, чтобы лишний раз не мельчить. Это позволяет лучше ориентироваться в проекте и делает код проекта чище. 

[WheelOfFortuneProviderService.kt](WheelOfFortuneProviderService.kt)
[CommonProviderService.kt](CommonProviderService.kt)
[CategoriesProviderService.kt](CategoriesProviderService.kt)
[AvailabilityProviderService.kt](AvailabilityProviderService.kt)

### **2.3. В классе есть метод, который выглядит более подходящим для другого класса.**

В качестве примера предложу класс [CardCashbackTariffConverter.java](CardCashbackTariffConverter.java). В имени класса речь идет о тарифах, а методы работают с условиями кэшбэка. Вероятно, название класса не соответствует выполняемым функциям, хотя вполне возможно, что названия методов не соответствуют выполняемым функциям. Без анализа исходного кода сложно делать однозначный вывод. Однако такое расхождение встречается достаточно редко. Наиболее распространена проблема, когда в классе есть метод, который хочется вынести в отдельный/другой класс. Как метод оказался в этом классе? Например, некоторый участок кода вынесли в отдельный метод, но для простоты тестирования его оставили в исходном классе.

### **2.4. Класс хранит данные, которые загоняются в него в множестве разных мест в программе.**

Точного примера мне найти не удалось, однако видел нечто похожее на [BuilderExample.java](BuilderExample.java). Объект билдера кочевал из сервиса в сервис в сервис, постепенно наполняясь данными. Почему код был написан таким образом? Вероятно, билдер в зависимости от условий наполнялся по-разному, в связи с чем можно было выстраивать своего рода дерево для конструирования объекта. Такой код, например, можно заменить "конструктором", для которого заранее будут подготовлены все необходимые для формирования объекта данные.

### **2.5. Класс зависит от деталей реализации других классов.**

Большое количество Java-приложений используют Spring Framework. Не в последнюю очередь потому, что он позволяет снизить связность используемых классов. Далее показан процесс снижения связности классов.

Вот как бы выглядела самая простая реализация Java-приложения, которая должна взаимодействовать с БД. PersonService должен знать о деталях реализации PersonDao, так как должен сконструировать объект.

```java
public class PersonService {
    private final IPersonDao personDao;

    PersonService() {
        this.personDao = new PersonDao("url");
    }
}

class PersonDao implements IPersonDao {
    private final String url;

    PersonDao(String url) {
        this.url = url;
    }
}

interface IPersonDao {
}
```

В случае применения паттерна ServiceLocator детали реализации не видны в PersonService, однако они перетекают в ServiceLocator.

```java
public class PersonService {
    private final IPersonDao personDao;

    PersonService() {
        this.personDao = ServiceLocator.getPersonDao();
    }
}

class PersonDao implements IPersonDao {
    private final String url;

    PersonDao(String url) {
        this.url = url;
    }
}

class ServiceLocator{
    private ServiceLocator(){
    }
    
    static PersonDao getPersonDao(){
        return new PersonDao("url");
    }
}
```

То, как сейчас работает Spring.

```java
public class PersonService {
    private final IPersonDao personDao;

    PersonService(IPersonDao personDao) {
        this.personDao = personDao;
    }
}

class PersonDao implements IPersonDao {
    private final String url;

    PersonDao(String url) {
        this.url = url;
    }
}

interface IPersonDao {
}
```

Такой подход позволяет держать детали реализации внутри класса.

### **2.6. Приведение типов вниз по иерархии (родительские классы приводятся к дочерним).**

Нисключение (downcasting) удобно, но оно сопряжено с риском непредвиденных ошибок среды выполнения, если фактическое значение не может быть представлено в узком типе. Каждое такое место в коде должно иметь обработку такой исключительной ситуации, что уже выглядит ошибочно с точки зрения дизайна. Кажется, что например, при работе с коллекциями требуется хранить рядом объекты только с тем типом из иерархии, с которым предполагается работать. То же касается и одиночных переменных и полей. Если одиночный объект или коллекция разнородных объектов из иерархии приходит извне, то при десериализации стоит единожды явно определить тип или разделить объекты по типам в зависимости от того, на каком уровне из иерархии предполагается работа с объектом/объектами.

### **2.7. Когда создаётся класс-наследник для какого-то класса, приходится создавать классы-наследники и для некоторых других классов.**

Если обратиться к примеру 3.2, но модифицировать условие таким образом, что пользователь может иметь несколько карт партнеров, то для вычисления ставки с использованием паттерна стратегия нам понадобится много классов. В самом простом варианте это будет выглядеть так: 

```java
interface BonusAccount {
    double ratio();
}

class TravelBonusAccount implements BonusAccount {
    public double ratio() {
        return 2;
    }
}

class PremiumBonusAccount implements BonusAccount {
    public double ratio() {
        return 3;
    }
}

class PremiumTravelBonusAccount implements BonusAccount {
    public double ratio() {
        return 4;
    }
}
```

Ситуация усугубляется, если комбинируются независимые сущности, тогда количество классов будет равно их декартовому произведению.

### **2.8. Дочерние классы не используют методы и атрибуты родительских классов, или переопределяют родительские методы.**

Дочерние классы не используют методы и атрибуты родительских классов, например, если в приложении есть объемный абстрактный класс или интерфейс:

```
interface Contract {
    fun getDetailsEndpoint(userId: String, account: InternalBonusAccount): String?
    fun getOrder(): Int
    fun getWidgetTitle(account: InternalBonusAccount): String?
    fun getBonusTitle(account: InternalBonusAccount): String?
    fun getWidgetSubtitle(account: InternalBonusAccount): String?
    fun getBonusSubtitle(account: InternalBonusAccount): String?
    fun getWidgetDescription(account: InternalBonusAccount): String?
    fun getBonusDescription(account: InternalBonusAccount): String?
    fun getWidgetBackgroundUrl(): String
    fun getBonusBackgroundUrl(): String?
    fun getVersion(): Int
    fun getType(): Type
    fun getLoyaltyProperties(): LoyaltyProperties
    fun getWidgetStyle(): Style?
    fun getBonusStyle(): Style?
    fun getNotAllowedAccountStatus(): Set<Status> = setOf(Status.CLOSED)
    fun getDeepLink(): String?
}
```

Близкие бизнес-сущности, представленные в виде набора классов, пытаются реализовать все методы, которые к ним могут не иметь отношения. Так разные бонусные счета или соответствующие им виджеты хотя и близки друг к другу, но могут отличаться по набору выполняемых с ними действий.

Переопределение родительских методов обычно является сигналом для того, чтобы пересмотреть логику построения иерархии. Возможно, вы захотите использовать другие методы наращивания функциональности: композиция, паттерн Посетитель, примеси и т.д.

## **3. Уровень приложения.**

### **3.1. Одна модификация требует внесения изменений в несколько классов.**

Недавно делал доработку, которая позволяла обрабатывать бонусные счета со статусом NEW и ACTIVE одинаково (ранее статус NEW игнорировался). Я изучил код на предмет обработки статуса ACTIVE. Он использовался в двух частях кода:
1) там где и планировался, в сервисе для получения отфильтрованного списка бонусных счетов, который является оберткой для сервиса бэкенда
2) скопированный другим разработчиком вариант в другом классе

Почему так произошло? Исходный метод был приватный, соответственно для простоты он был скопирован и применен к вызову сервиса бэкенда напрямую. Написанный мной сервис (обертка над сервисом бэкенда с фильтрацией) был проигнорирован. К чему это привело? Изменение бизнес-требований требовало внесения изменений в несколько классов. Я заменил вызов сервиса бэкенда на вызов своего сервиса, который уже обеспечивал фильтрацию, а избыточный метод удалил.

Вот как код выглядел:
```
    private suspend fun bonusAccountActiveForCustomer(headers: Headers, accountType: String): Boolean =
        bonusAccountProxy.getBonusAccounts(headers)
            .filter(activeSupportedProgramPredicate())
            ...

    private fun activeSupportedProgramPredicate(): (BonusAccount) -> Boolean = bonusAccount -> bonusAccount.statusId == Status.ACTIVE.value
```

И как он стал выглядеть:

```
    private suspend fun isBonusAccountActiveForCustomer(headers: Headers, accountType: String): Boolean =
        unifiedBonusAccountProviderService.getUnifiedBonusAccounts(headers)
            ...
```


### **3.2. Использование сложных паттернов проектирования там, где можно использовать более простой и незамысловатый дизайн.**

Предположим, что у пользователя есть базовый бонусный счет, который дает базовую ставку начисления бонусных баллов. Если
у пользователя есть карта партнера, то он получит повышенную ставка начисления бонусных баллов. Можно использовать 
паттерн "Декоратор", чтобы высчитывать коэффициенты:

```java
abstract class BonusAccount {
    public abstract int ratio();
}

class BaseBonusAccount extends BonusAccount {
    public double ratio() {
        return 1;
    }
}

abstract class BonusAccountDecorator extends BonusAccount {
    protected final BonusAccount decoratedBonusAccount;

    public BonusAccountDecorator(BonusAccount bonusAccount) {
        this.decoratedBonusAccount = bonusAccount;
    }

    public abstract double ratio();
}

class TravelDecorator extends BonusAccountDecorator {
    public TravelDecorator(BonusAccount bonusAccount) {
        super(bonusAccount);
    }

    public double ratio() {
        return decoratedBonusAccount.ratio() + 1;
    }
}

class PremiumDecorator extends BonusAccountDecorator {
    public PremiumDecorator(BonusAccount bonusAccount) {
        super(bonusAccount);
    }

    public double ratio() {
        return decoratedBonusAccount.ratio() + 2;
    }
}
```

Если, например, пользователь может иметь только одну карту партнера, а коэффициенты меняются нечасто, то можно 
использовать паттерн "Стратегия" для определения различных типов бонусных счетов и их ставок.

```java
interface BonusAccount {
    double ratio();
}

class TravelBonusAccount implements BonusAccount {
    public double ratio() {
        return 2;
    }
}

class PremiumBonusAccount implements BonusAccount {
    public double ratio() {
        return 3;
    }
}
```