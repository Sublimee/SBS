```java

class Animal {
    // Метод, который будет переопределен
    void sound() {
        System.out.println("Animal makes a sound");
    }
}

class Dog extends Animal {
    // Переопределение метода sound
    @Override
    void sound() {
        System.out.println("Dog barks");
    }
}

public class Main {
    public static void main(String[] args) {
        // Создаем объект класса Animal
        Animal myAnimal = new Animal();
        // Создаем объект класса Dog
        Animal myDog = new Dog();

        // Вызываем метод sound на каждом из объектов
        // Динамическое связывание здесь позволяет вызвать метод sound() класса Dog,
        // даже если объект myDog объявлен как тип Animal
        myAnimal.sound(); // Выведет "Animal makes a sound"
        myDog.sound();    // Выведет "Dog barks" из-за динамического связывания
    }
}
```