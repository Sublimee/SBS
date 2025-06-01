# Пример 1

Если говорить о Java и других языках, работающих поверх JVM, то порядок полей в объявлении класса может коррелировать с порядком в памяти экземпляра, но это не гарантируется спецификацией. Порядок может отличаться между разными JVM и даже между запусками.

Есть класс:

```java
public class Student implements Serializable {
    public String name;
    public int rollNumber;
    public char gender;

    public Student(int rollNumber, String name, char gender) {
        this.rollNumber = rollNumber;
        this.name = name;
        this.gender = gender;
    }
}
```

Так как класс помечен маркерным интерфейсом и мы явно не указали serialVersionUID, то поле будет сгенерировано за нас автоматически.Этот процесс:

Значение serialVersionUID может отличаться между версиями JVM, его стабильность не гарантируется между компиляциями (хотя в этом аспекте он достаточно стабилен). Даже незначительные изменения в классе могут изменить вычисленный serialVersionUID, в чем мы сейчас и убедимся.

Посмотрим, как размещаются поля в памяти при помощи библиотеки JOL (Java Object Layout):

```java
Student student = new Student(101, "Harsh", 'M');
System.out.println(ClassLayout.parseInstance(student).toPrintable());
```

```text
org.example.Student object internals:
OFF  SZ               TYPE DESCRIPTION               VALUE
  0   8                    (object header: mark)     0x0000000000000001 (non-biasable; age: 0)
  8   4                    (object header: class)    0x01197148
 12   4                int Student.rollNumber        101
 16   2               char Student.gender            M
 18   2                    (alignment/padding gap)   
 20   4   java.lang.String Student.name              (object)
Instance size: 24 bytes
Space losses: 2 bytes internal + 0 bytes external = 2 bytes total
```

Также попробуем выполнить сериализацию с помощью библиотеки org.apache.commons.lang3.SerializationUtils:

```java
Base64.getEncoder().encodeToString(SerializationUtils.serialize(student));
```

Получим:

```text
rO0ABXNyABNvcmcuZXhhbXBsZS5TdHVkZW50kjdRoWi2d8cCAANDAAZnZW5kZXJJAApyb2xsTnVtYmVyTAAEbmFtZXQAEkxqYXZhL2xhbmcvU3RyaW5nO3hwAE0AAABldAAFSGFyc2g=
```

Поменяем порядок следования полей:

```java
public class Student implements Serializable {
    public char gender;
    public String name;
    public int rollNumber;

    public Student(char gender, String name, int rollNumber) {
        this.gender = gender;
        this.name = name;
        this.rollNumber = rollNumber;
    }
}
```

Результат работы JOL идентичен:

```text
org.example.Student object internals:
OFF  SZ               TYPE DESCRIPTION               VALUE
  0   8                    (object header: mark)     0x0000000000000001 (non-biasable; age: 0)
  8   4                    (object header: class)    0x01197148
 12   4                int Student.rollNumber        101
 16   2               char Student.gender            M
 18   2                    (alignment/padding gap)   
 20   4   java.lang.String Student.name              (object)
Instance size: 24 bytes
Space losses: 2 bytes internal + 0 bytes external = 2 bytes total
```

А вот SerializationUtils отработал по-другому (строки отличаются):

```text
rO0ABXNyABNvcmcuZXhhbXBsZS5TdHVkZW50KyZahd0yn10CAANDAAZnZW5kZXJJAApyb2xsTnVtYmVyTAAEbmFtZXQAEkxqYXZhL2xhbmcvU3RyaW5nO3hwAE0AAABldAAFSGFyc2g=
```

При попытке десериализовать первый массив байтов, сохранив обновленное объявление класса Student, получим:

```java
SerializationUtils.deserialize(Base64.getDecoder().decode("rO0ABXNyABNvcmcuZXhhbXBsZS5TdHVkZW50kjdRoWi2d8cCAANDAAZnZW5kZXJJAApyb2xsTnVtYmVyTAAEbmFtZXQAEkxqYXZhL2xhbmcvU3RyaW5nO3hwAE0AAABldAAFSGFyc2g="));
```

```text
org.apache.commons.lang3.SerializationException: java.io.InvalidClassException: org.example.Student; local class incompatible: stream classdesc serialVersionUID = -7910764466764613689, local class serialVersionUID = 3109272123734138717
```

Защита от дурака сработала.

Зададим serialVersionUID = 1 явно для обоих классов и повторим эксперимент. Результат работы JOL идентичен предыдущим, но в этом случае объекты будут сериализованы в одну и ту же строку:

```text
rO0ABXNyABNvcmcuZXhhbXBsZS5TdHVkZW50AAAAAAAAAAECAANDAAZnZW5kZXJJAApyb2xsTnVtYmVyTAAEbmFtZXQAEkxqYXZhL2xhbmcvU3RyaW5nO3hwAE0AAABldAAFSGFyc2g=
```

Попробуем ее десериализовать, заменив объявление на второе. Как и ожидалось, десериализация прошла успешно. Это говорит нам о том, что serialVersionUID, если он проставлен явно, можно забыть обновить.

# Пример 2

Если хочется гарантировать порядок и типы полей и обеспечить обратную совместимость при сериализации/десериализации, то нужно использовать FlatBuffers, Avro, Protobuf.

# Вывод

Попробуем обобщить полученные результаты:
1) нельзя в принципе опираться на порядок полей в API, если это не зафиксировано контрактом;
2) в качестве контракта могут выступать схемы и/или версии;
3) ничего не поможет поддерживать долгосрочную поддержку API, если нет контроля качества, в том числе защиты от дурака (application-level и automated тесты, ревью).

Если мы пишем собственный протокол/библиотеку в соответствии с которым будем проводить сериализацию/десериализацию, то мы скорее всего должны учесть обратную совместимость при проектировании. Если мы не используем схему, не версионируем, а просто полагаемся на порядок следования байт в сериализованном массиве, то нужно обеспечить контроль изменений в соответствии с пунктом 3.

Если мы используем сторонние решения, то нужно смотреть, за счет чего будет обеспечена обратная совместимость, как ее можно нарушить. И опять же нужно следовать пункту 3.