Для анализа результатов подключаем логирование выполняемых SQL-запросов:

```properties
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
```

## Пример 1

Пример кода c использованием ORM:

```java
@Entity
@Data
@Table(name = "author", ...)
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode
public class Author {
    
    ...

    @ManyToMany(fetch = FetchType.LAZY, cascade = { CascadeType.PERSIST, CascadeType.MERGE })
    @JoinTable(name = "authors_books",
            joinColumns = { @JoinColumn(name = "author_id") },
            inverseJoinColumns = { @JoinColumn(name = "book_id") })
    private List<Book> books = new ArrayList<Book>();

    ...
}


@Entity
@Table(name = "book")
public class Book {
    
    ...

    @ManyToMany(mappedBy = "books", fetch = FetchType.LAZY)
    private Set<Author> authors = new HashSet<>();

    ...
}
```

### Методы получения списка авторов

```java
@Repository
public interface AuthorsRepository extends JpaRepository<Author, Long> {
    List<Author> findAll();

    @Query("SELECT a FROM Author a")
    List<Author> findAllAuthorsByQuery();
}
```

### Смысловая нагрузка

Получить информацию обо всех авторах без информации по книгам.

### Анализ

Рассмотрим следующий код:

```java
    ...

    @ManyToMany(fetch = FetchType.EAGER, cascade = { CascadeType.PERSIST, CascadeType.MERGE })
    @JoinTable(name = "authors_books",
            joinColumns = { @JoinColumn(name = "author_id") },
            inverseJoinColumns = { @JoinColumn(name = "book_id") })
    private Set<Book> books = new HashSet<>();

    ...
```

При получении из БД информации обо всех авторах будет также запрошена информация обо всех книгах, которые принадлежат этому автору. Причем по каждому автору будет сделан отдельный SQL-запрос для получения списка его книг:

```sql

select
    author0_.author_id as author_i1_1_
from
    author author0_

select
    books0_.author_id as author_i1_2_0_,
    books0_.book_id as book_id2_2_0_,
    book1_.book_id as book_id1_3_1_
from
    authors_books books0_
        inner join
    book book1_
    on books0_.book_id=book1_.book_id
where
    books0_.author_id=?

select
    books0_.author_id as author_i1_2_0_,
    books0_.book_id as book_id2_2_0_,
    book1_.book_id as book_id1_3_1_
from
    authors_books books0_
        inner join
    book book1_
    on books0_.book_id=book1_.book_id
where
    books0_.author_id=?
```

Обычно это не то, что мы хотим сделать (вычитать всю БД), поэтому рекомендуется по-умолчанию использовать FetchType.LAZY, чтобы не провоцировать лишние запросы до тех пор, пока данные о книгах автора, действительно, не понадобятся. Это решение и было применено в исходном примере. Методы ведут себя одинаково:

```sql
    select
        author0_.author_id as author_i1_1_ 
    from
        author author0_
```

поэтому выигрыша в производительности по отношению к SQL-запросу получить не удалось.

## Пример 2

### Смысловая нагрузка

Предположим, что нам необходима возможность получения авторов только со всем списком их книг. При этом получение всех авторов запрещено. 

### Анализ

В таком случае оставим такой вариант получения книг авторов:

```java
    ...

    @ManyToMany(fetch = FetchType.EAGER, cascade = { CascadeType.PERSIST, CascadeType.MERGE })
    @JoinTable(name = "authors_books",
            joinColumns = { @JoinColumn(name = "author_id") },
            inverseJoinColumns = { @JoinColumn(name = "book_id") })
    private Set<Book> books = new HashSet<>();

    ...
```

Добавим еще несколько методов:

```java
@Repository
public interface AuthorsRepository extends JpaRepository<Author, Long> {
    ...
    List<Author> findAuthorByAuthorId();
    ...
}
```

и

```java
public class AuthorsService{

    ...
    
    public Author findAuthorByQuery(Long authorId) {
        TypedQuery<Author> query = entityManager.createQuery(
                "SELECT a FROM Author a " +
                        "LEFT JOIN FETCH a.books " +
                        "WHERE a.authorId = :authorId", Author.class);
        query.setParameter("authorId", authorId);
        return query.getSingleResult();
    }
    
    ...
}
```

Сравним результаты вызовов:

```sql
    select
        author0_.author_id as author_i1_1_ 
    from
        author author0_ 
    where
        author0_.author_id=?

    select
        books0_.author_id as author_i1_2_0_,
        books0_.book_id as book_id2_2_0_,
        book1_.book_id as book_id1_3_1_ 
    from
        authors_books books0_ 
    inner join
        book book1_ 
            on books0_.book_id=book1_.book_id 
    where
        books0_.author_id=?
```

против


```sql
    select
        author0_.author_id as author_i1_1_0_,
        book2_.book_id as book_id1_3_1_,
        books1_.author_id as author_i1_2_0__,
        books1_.book_id as book_id2_2_0__ 
    from
        author author0_ 
    left outer join
        authors_books books1_ 
            on author0_.author_id=books1_.author_id 
    left outer join
        book book2_ 
            on books1_.book_id=book2_.book_id 
    where
        author0_.author_id=?
```

Несмотря на то, что результаты получаются теми же, Hibernate для их получения использует 2 запроса.

## Пример 3

### Смысловая нагрузка
Теперь вы хотите внедрить пагинацию списка авторов.

### Анализ

Для этого можно выбирать из БД всех авторов и на стороне Java высчитывать в соответствии с номером страницы и количеством результатов на ней отфильтровывать данные. Более разумным вариантом выглядит запрос необходимого набора данных из БД:

```java
    public List<Author> findPaginated(int page, int size) {
        return entityManager.createQuery(
                        "SELECT a FROM Author a ORDER BY a.id ASC",
                        Author.class)
                .setMaxResults(size)
                .setFirstResult(page * size)
                .getResultList();
    }
```

Так будет выглядеть запрос:

```sql
    select
        author0_.author_id as author_i1_1_
    from
        author author0_
    order by
        author0_.author_id ASC limit ? offset ?
```

Обошлось без сюрпризов. Такой вариант получения необходимого набора авторов будет гораздо эффективнее выполнения полной выборки.

## Вывод

Hibernate, будучи мощным инструментом для работы с базами данных в Java-приложениях, часто может негативно влиять на производительность системы.
Как и любой другой фреймворк, который делает много под капотом (как и Spring, например), Hibernate требует осознанного использования от оператора. В этом всегда может помочь логирование выполняемых SQL-запросов, которые на этапе отладки должны быть проанализированы. Нас будут интересовать как количество, так и их качество. Новички часто сталкиваются с проблемой производительности при загрузке связанных данных (N+1, eager loading).

В то же время Hibernate предоставляет механизмы для оптимизации запросов, такие как lazy loading для связанных сущностей, batch processing для группировки SQL-запросов и кэширование, чтобы уменьшить количество операций чтения и записи в базу данных.

В большинстве случаев все же проще написать SQL-запрос собственноручно (JPQL/HQL или Criteria API), не полагаясь на эвристики фреймворка.