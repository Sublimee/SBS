Что если мы хотим добавить классу несколько независимых функциональностей классу, а множественное наследование языком не предусмотрено? Языки Ruby и Scala имеют встроенную поддержку Mixins и Traits соответственно. Механизм миксинов позволяет добавлять поведение к классам путем комбинирования кода без наследования. Миксины в отличие от классов не предполагают инстанциирование. Однако важно, что методы миксинов имеют доступ к self (this) как любый другие методы класса.

В Java схожую поддержку нативно можно реализовать с помощью [интерфейсов с default-методами](..%2F..%2Fjava%2Fstrong%2Fideas%2Flesson_8%2Fexample_1%2FMixin.java) или  [класса-миксины](..%2F..%2Fjava%2Fstrong%2Fideas%2Flesson_8%2Fexample_2%2FMixin.java). Такая реализация не настолько удобна, так как требует вынесения состояния миксинов (если оно есть) в класс, который будет расширяться.

Также есть вариант с применением АОП (aspectj, например). Мы можем объявить интерфейс, но целевому классу не потребуется его имплементировать — за него это сделает аспект:

```java
interface Commentable {

    List<String> getComments();

    void addComment(String comment);
}

aspect CommentableAspect {

    private List<String> Commentable.comments;
 
    public final String Commentable.getComments() {
        return this.comment;
    }
     
    public final void Commentable.addComment(String comment) {
        this.getComments().add(comment);
    }
}
```

Миксины -- это еще один способ сократить дублирование кода и обойти ограничение множественного наследования. В классах-наследниках т.о. появляется возможность частично переиспользовать требуемую функциональность классов-родителей.