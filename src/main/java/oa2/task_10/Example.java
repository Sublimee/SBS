package oa2.task_10;

class BaseClass {
    // Этот метод не может быть переопределен в наследниках
    public final void nonOverridableMethod() {
        System.out.println("Этот метод не может быть переопределен.");
    }

    // Этот метод может быть переопределен в наследниках
    public void overridableMethod() {
        System.out.println("Этот метод может быть переопределен.");
    }
}

class DerivedClass extends BaseClass {
    // Ошибка: не удастся переопределить nonOverridableMethod()
    // @Override
    // public void nonOverridableMethod() {
    //     System.out.println("Попытка переопределения.");
    // }

    // Этот метод успешно переопределяет метод из класса-предка
    @Override
    public void overridableMethod() {
        System.out.println("Переопределенный метод.");
    }
}

public class Example {
    public static void main(String[] args) {
        DerivedClass derived = new DerivedClass();
        derived.nonOverridableMethod(); // Вызовет метод из BaseClass
        derived.overridableMethod();    // Вызовет переопределенный метод из DerivedClass
    }
}