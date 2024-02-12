4. Наследования вариаций

4.1. Наследование с функциональной вариацией (functional variation inheritance)

```java
class Human {
    // Базовый метод, который будет переопределен
    void greet() {
        System.out.println("Hello, I'm a human.");
    }
}

class Child extends Human {
    // Переопределение метода greet без изменения сигнатуры
    @Override
    void greet() {
        System.out.println("Hi, I'm a child.");
    }
}
```

4.2. Наследование с вариацией типа (type variation inheritance)

```java
class Human {
    void greet() {
        System.out.println("Hello, I'm a human.");
    }
}

class Adult extends Human {
    // Перегрузка метода greet с добавлением параметра name
    void greet(String name) {
        System.out.println("Hello, " + name + ", I'm an adult.");
    }
}
```

5) Наследование с конкретизацией (reification inheritance)

```java
abstract class Vehicle {
    // Абстрактный метод, который будет реализован в потомках
    abstract void move();
}

class Car extends Vehicle {
    // Конкретная реализация метода move для автомобиля
    @Override
    void move() {
        System.out.println("The car moves on the road.");
    }
}

class Bicycle extends Vehicle {
    // Конкретная реализация метода move для велосипеда
    @Override
    void move() {
        System.out.println("The bicycle moves on the bike path.");
    }
}
```

6) Структурное наследование (structure inheritance)

```java
public class Task implements Runnable {
    private String message;
    
    public Task(String message) {
        this.message = message;
    }
    
    @Override
    public void run() {
        // Полезная работа
    }
}
```