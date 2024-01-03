Массивы в Java ковариантны:

```java
String[] strings = new String[] {"a", "b", "c"};
Object[] arr = strings;
```

Дженерики могут быть:

1) инвариантны

```java
List<Integer> ints = Arrays.asList(1,2,3);
List<Number> nums = ints; // compile-time error
```

2) ковариантны (```List<Integer>``` — подтип ```List<? extends Number>```): 

```java
List<Integer> ints = new ArrayList<Integer>();
List<? extends Number> nums = ints;
```

3) контравариантны (```List<Number>``` является подтипом ```List<? super Integer>```):

```java
List<Number> nums = new ArrayList<Number>();
List<? super Integer> ints = nums;
```