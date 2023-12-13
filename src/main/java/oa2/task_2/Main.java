package oa2.task_2;


// Базовый класс
abstract class Character {

    public void hurt() {
        System.out.println("Emotional damage!");
    }

}

class Civilian extends Character {

    // наследник изменяет поведение класса-родителя
    public void hurt() {
        System.out.println("Peace!");
    }

}

class Warrior extends Character {

    // наследник расширяет функциональность класса-родителя
    public void cry() {
        System.out.println("I'll bring emotional damage!");
    }
}