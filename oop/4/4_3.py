import random

class Animal:
    def foo(self):
        pass

class Cat(Animal):
    def foo(self):
        print("Кошка мурлычет")

class Bird(Animal):
    def foo(self):
        print("Птица поет")


def fill_animals(animals: list[Animal]) -> None:
    animals.clear()

    for _ in range(500):
        if random.random() < 0.5:
            animals.append(Cat())
        else:
            animals.append(Bird())


animals: list[Animal] = []
fill_animals(animals)

# фактически вызывается Cat.foo() или Bird.foo() в зависимости от реального типа объекта (полиморфизм подтипов)
for animal in animals:
    animal.foo()