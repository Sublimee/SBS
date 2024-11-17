## Задание 2

### Пример 1

В Kotlin отказались от проверяемых исключений, которые должны были в Java указываться в сигнатуре метода и соответствующим образом обрабатываться. Kotlin поощряет использование альтернативного подхода к обработке ошибок, а именно применение абстракции результата операции [Result](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/-result/). Result инкапсулирует успешный результат со значением типа T или сбой с исключением. Класс предоставляет нам ряд методов, которые можно использовать для понимания статуса выполнения операции и получения ее результата.

Таким образом при выполнении некоторого блока кода, который может закончиться исключением, необходимо прибегнуть, например, к следующей обертке:

```kotlin
inline fun <T, R> T.runCatching(block: T.() -> R): Result<R> =
    try {
        Result.success(block())
    } catch (e: Throwable) {
        Result.failure(e)
    }
```

Так будет выглядеть обработка результата операции:

```kotlin
widgetService.runCatching {
    getProgramWidget(
        ...
    )
}
.onFailure {
    logger.error(it) { ... }
}
.getOrNull()
```

### Пример 2

Еще одна абстракция, только реализованная на уровне компилятора -- корутины Kotlin и suspend функции в частности. Они скрывают от нас асинхронную сущность кода за обычным императивным кодом. Нам не нужно задумываться о сложности управления потоками, мы концентрируемся на бизнес-логике. В этом их ключевое преимущество над многословными CompletableFeature, RxJava, WebFlux.

Посмотрим на пример игрушечного кода:

```kotlin
    suspend fun myFun() {
        printFun("Before")
        delay(1000)
        printFun("After")
    }

    suspend fun printFun(someTest: String): Boolean {
        println(someTest)
        return true
    }
```

И что скрывается за ним:

```java
   // Декомпилированный байткод myFun
   static Object myFun$suspendImpl(final WheelOfFortuneConfirmationServiceV2 $this, Continuation $completion) {
      Object $continuation;
      label37: {
         if ($completion instanceof <undefinedtype>) {
            $continuation = (<undefinedtype>)$completion;
            if ((((<undefinedtype>)$continuation).label & Integer.MIN_VALUE) != 0) {
               ((<undefinedtype>)$continuation).label -= Integer.MIN_VALUE;
               break label37;
            }
         }

         $continuation = new ContinuationImpl($completion) {
            Object L$0;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return WheelOfFortuneConfirmationServiceV2.myFun$suspendImpl($this, (Continuation)this);
            }
         };
      }

      Object var4;
      label30: {
         Object $result = ((<undefinedtype>)$continuation).result;
         var4 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
         switch (((<undefinedtype>)$continuation).label) {
            case 0:
               ResultKt.throwOnFailure($result);
               ((<undefinedtype>)$continuation).L$0 = $this;
               ((<undefinedtype>)$continuation).label = 1;
               if ($this.printFun("Before", (Continuation)$continuation) == var4) {
                  return var4;
               }
               break;
            case 1:
               $this = (WheelOfFortuneConfirmationServiceV2)((<undefinedtype>)$continuation).L$0;
               ResultKt.throwOnFailure($result);
               break;
            case 2:
               $this = (WheelOfFortuneConfirmationServiceV2)((<undefinedtype>)$continuation).L$0;
               ResultKt.throwOnFailure($result);
               break label30;
            case 3:
               ResultKt.throwOnFailure($result);
               return Unit.INSTANCE;
            default:
               throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
         }

         ((<undefinedtype>)$continuation).L$0 = $this;
         ((<undefinedtype>)$continuation).label = 2;
         if (DelayKt.delay(1000L, (Continuation)$continuation) == var4) {
            return var4;
         }
      }

      ((<undefinedtype>)$continuation).L$0 = null;
      ((<undefinedtype>)$continuation).label = 3;
      if ($this.printFun("After", (Continuation)$continuation) == var4) {
         return var4;
      } else {
         return Unit.INSTANCE;
      }
   }
```

### Пример 3

Проект Spring Data предоставляет нам возможность создания точных абстракций над хранилищами данных. По сравнению, например, с JDBC мы больше не заботимся о соединениях, выражениях (Statement во всех проявлениях), вычленении результата (ResultSet) и т.д., а работаем с данными. Мы можем точно выражать намерения и получать предсказуемый результат:

Вот пример одного из множества примеров возможных реализаций:

```java
@Repository
public interface AccountsRepository extends PagingAndSortingRepository<Account, Long>, JpaSpecificationExecutor<Account> {

    Optional<List<Account>> getAccountsByClientId(final Long clientId);

    Optional<Account> getAccountById(final Long id);

}
```

### Пример 4

Но если говорить о такой абстракции, как ReactiveMongoTemplate (org.springframework.data:spring-data-mongodb:4.1.5), то такой вызов не будет ограничивать количество элементов, которые будут обновлены (limit(batchSize) будет проигнорирован):

```kotlin
    val query = Query()
        .addCriteria(...)
        .limit(batchSize)

    val update = Update()
        ...

    val updateResult = mongoTemplate.updateMulti(
        query,
        update,
        entityClass
    ).awaitFirstOrNull()
```

Кажется, что такую абстракцию сложно назвать точной. Нам нужно знать какие-то особенности внутренней работы фреймворка, чтобы предугадать результат. Чтобы реализовать нашу идею, приходится прибегать к последовательности вызовов:

```kotlin
        val ids = mongoTemplate.find(
            Query()
                ...
                .limit(batchSize),
                ...
        )

        val updateQuery = Update()
            ...

        mongoTemplate.update(documentClass)
            .matching(
                Criteria.where(ID_FIELD).inValues(ids)
            )
            .apply(updateQuery)
            .all()
            .awaitFirst()
```

### Пример 5

Хорошими продуманными абстракциями изобилует k8s. Для примера рассмотрим ресурсы для управления подключаемыми томами.

Обычно администратор хранилища выделяет пространство пользователям (пользовательским приложениям), а затем пользователи используют выделенное хранилище для своих нужд. В Kubernetes для этого служит абстракция PersistentVolume. Она предоставляет единый API для управления системами хранения (NFS, GlusterFS, CephFS, iSCSI и др.). Каждый pod может запросить требуемое пространство из PV, используя абстракцию Persistent Volume Claim (PVC).

Создадим PV на примере локального хранилища:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
```

Это хранилище будет использовать папку /mnt/data.

Теперь создадим PVC:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pv-claim
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
```

Из хранилища в 10 Гб будет запрошено 3 Гб. А теперь подключим хранилище к приложению:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: task-pv-pod
spec:
  volumes:
    - name: task-pv-storage
      persistentVolumeClaim:
        claimName: task-pv-claim
  containers:
    - name: task-pv-container
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: task-pv-storage
```

Теперь при запуске контейнера nginx данный PV будет примонтирован по пути /usr/share/nginx/html. Почти как docker bind mount.

Под не знает, где физически расположено хранилище, что оно из себя представляет, а просто работает с любезно предоставленной нам абстракцией ФС: записывает и считывает данные, как будто это обычная ФС.

## Задание 3 и Вывод

Как, наверное, несложно было заметить, все приведенные примеры напрямую не относились к бизнес-коду. Как я ни пытался найти точные абстракции, я их не находил. Требовалось предварительно вычислить из моделей и интерфейсов много мусора, который отделял их от чистого идеала.

Наиболее близкой, как мне казалось, должна была быть абстракция для заправочных станций. Увидев, модель, у меня опустились руки: я увидел тот самый беспорядочный мир.

```kotlin
@Document
data class Station(
    @field:Id
    val externalId: String,
    val name: String,
    val brand: String,
    val address: String,
    val location: Location,
    val fuels: List<Fuel>,
    val isOrderBefore: Boolean,
    val isTakeBefore: Boolean,
    val mapId: Int,
    val maxPrice: Double?,
)
```

Взаимозаменяемые isOrderBefore и isTakeBefore. mapId -- идентификатор Яндекса для отображения на более удобного отображения на картах. Отдельно живующие адрес address и локация location. maxPrice на уровне Station (ну не цену же станции имели в виду). Да, это документ (@Document) из MongoDB, который может легко расширяться. Это сыграло с ним злую шутку.

Самое время обратиться к определению Дейкстры: "мы хотим открыть для себя новый семантический уровень мышления, на котором мы парадоксально можем быть абсолютно точны -- ещё более точны, чем даже на уровне синтаксиса кода."

Дизайн системы -- есть отображение реального мира и его процессов. Прежде чем приступать к написанию кода, мы должны продумать, какими абстракциями реального мира мы хотим и будем оперировать. Тут же стоит отметить, что одна и та же сущность или процесс реального мира могут быть приведены к разным абстракциям в зависимости от нашей точки зрения, их понимания и решаемой задачи.

Код -- лишь конкретное отображение дизайна с использованием фич языка, которые нам в этом помогают. Если дизайн системы плохой (плохо выбраны абстракции), то код будет гарантированно плохой (неподдерживаемый, сложный и т.п.). С другой стороны, если у нас есть хороший дизайн, то код не обязательно получится хорошим. Более того в последующем такой код будет влиять на дизайн. Может ли быть наоборот: хороший код (поддерживаемый, выполняющий задачу), который выполнен на основе плохого дизайна? Определенно, нет. В этом смысле код никогда не станет точнее более высокого уровня мышления о программе.

Как это знание я могу применить в своей практике? Главное -- не отходить от отображения реального мира через абстракции в коде. Добавленные легким движением руки очередной if или новый параметр может навсегда разрушить стройный дизайн системы.