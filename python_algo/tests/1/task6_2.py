import ctypes

from task4_2 import MinStack
from task6 import Deque


# 7.1. Сложность addHead/removeHead и addTail/removeTail

# При использовании двусвязного списка addHead/removeHead и addTail/removeTail выполнятся за O(1): нужно только
# убрать/установить соответствующие ссылки, что не зависит от числа элементов. При использовании динамического массива
# сложность ddTail/removeTail будет O(1) не считая перестроения массива, а addHead/removeHead -- O(N), так как сложность
# перестроения уже входит в сложность удаления добавления головы со свдвигом стоящих за ней элементов.

# 7.2. Тесты

# В файле task6_3.py

# 7.3.* Палиндромом.

def isPalindrome(s):
    # проверяем на None и пустую строку, это не палиндром
    if s is None or len(s) == 0:
        return False

    # выделяем только буквы и приводим их к нижнему регистру
    lower_s = ""
    for ch in s:
        if ch.isalpha():
            lower_s += ch.lower()

    # строим deque
    d = build_deque(list(lower_s))

    # пока не останется один символ для нечетного количества символов исходной строки или 0 симвовлов для четного
    # количества символов исходной строки, сравниваем по символу из начала и конца строки
    while d.size() > 1:
        # если они не совпадают, то строка не палиндром
        if d.removeFront() != d.removeTail():
            return False

    # остался 1 или 0 символов -> палиндром
    return True
    # можно было бы сделать за один проход строки, если бы сразу анализировали голову и хвост на принадлежность к буквам


def build_deque(values):
    d = Deque()
    for v in values:
        d.addTail(v)
    return d


# 7.4.* Напишите метод, который возвращает минимальный элемент деки за O(1).

# Долго пытался сделать аналогично идее с MinStack (с одним стеком), но возможность удаления
# и хвоста и головы нарушали идею, хотя логически понимал, что работа с хвостом и работы с головой должны обрабатываться
# независимо.
#
# Работаем с головой и с хвостом через два разных стека, а когда в одном из стеков заканчиваются элементы то 
# перекладываем другой стек и продолжаем забирать элементы. Алгоритм будет просаживаться по производительности, если 
# эксплуатировать эту идею и забирать то с конца, то с начала деки. Для оптимизации этой идеи надо было расширить 
# MinStack до MinDeque, чтобы когда закончатся элементы в одной деке можно было бы не переливать весь стек, а 
# ограничиться лишь одним элементом.

class DequeMin:
    def __init__(self):
        self.front = MinStack()
        self.tail = MinStack()
        self.elements_count = 0

    def addTail(self, item):
        self.tail.push(item)
        self.elements_count += 1

    def addFront(self, item):
        self.front.push(item)
        self.elements_count += 1

    def removeFront(self):
        if self.elements_count == 0:
            return None

        if self.front.size() != 0:
            self.elements_count -= 1
            return self.front.pop()

        while self.tail.size() != 0:
            self.front.push(self.tail.pop())

        self.elements_count -= 1
        return self.front.pop()

    def removeTail(self):
        if self.elements_count == 0:
            return None

        if self.tail.size() != 0:
            self.elements_count -= 1
            return self.tail.pop()

        while self.front.size() != 0:
            self.tail.push(self.front.pop())

        self.elements_count -= 1
        return self.tail.pop()

    def size(self):
        return self.elements_count

    def min(self):
        if self.elements_count == 0:
            return None
        if self.front.size() == 0:
            return self.tail.min()
        if self.tail.size() == 0:
            return self.front.min()
        return min(self.tail.min(), self.front.min())


# 7.5.* Реализуйте двустороннюю очередь с помощью динамического массива. Методы добавления и удаления элементов с обоих
# концов деки должны работать за амортизированное время o(1).

# Рефлексия:
# При вставке первого элемента задаем голову и хвост. В целом это может быть любой элемент массива, но проще начинать с
# нулевого или последнего индекса. Если при вставке в голову/хвост вываливаемся за границы массива, то индекс нужно
# соответствующим образом пересчитать. Если при очередной вставке некуда вставлять элемент, то нужно увеличивать размер
# массива. Я при этом переносил все элементы, начиная с 0 индекса, хотя опять же можно выбирать любой. При удалении
# элементов нужно так же следить за тем, чтобы не вывалиться за пределы массива + за существованием хвоста и головы.
# Уменьшение размера массива не проводил для упрощения реализации.
#
# Таким образом вставка/удаление элемента за исключением случаев увеличения размера массива не требуют сдвига элементов
# и могут быть оценены в o(1).

class Deque2:
    INIT_CAPACITY = 4

    def __init__(self):
        self.count = 0
        self.capacity = self.INIT_CAPACITY
        self.array = self.make_array(self.capacity)
        self.head_index = None
        self.tail_index = None

    def make_array(self, new_capacity):
        return (new_capacity * ctypes.py_object)()

    def size(self):
        return self.count

    def addFront(self, item):
        if self.count == self.capacity:
            self.resize(2 * self.capacity)

        if self.head_index is None:
            self.head_index = self.capacity - 1
            self.tail_index = self.head_index
        elif self.head_index - 1 < 0:
            self.head_index = self.capacity - 1
        else:
            self.head_index = self.head_index - 1

        self.array[self.head_index] = item
        self.count += 1

    def addTail(self, item):
        if self.count == self.capacity:
            self.resize(2 * self.capacity)

        if self.tail_index is None:
            self.head_index = 0
            self.tail_index = self.head_index
        elif self.tail_index + 1 == self.capacity:
            self.tail_index = 0
        else:
            self.tail_index = self.tail_index + 1

        self.array[self.tail_index] = item
        self.count += 1

    def resize(self, new_capacity):
        new_array = self.make_array(new_capacity)

        for i in range(self.count):
            new_array[i] = self.array[(self.head_index + i) % self.capacity]

        self.head_index = 0
        self.tail_index = self.capacity - 1
        self.array = new_array
        self.capacity = new_capacity

    def removeFront(self):
        result = None
        if self.head_index is not None:
            result = self.array[self.head_index]
            self.array[self.head_index] = None
            self.head_index = (self.head_index + 1) % self.capacity
            self.count -= 1

        if self.count == 0:
            self.head_index = None
            self.tail_index = None
        elif self.count == 1:
            self.tail_index = self.head_index

        return result

    def removeTail(self):
        result = None
        if self.tail_index is not None:
            result = self.array[self.tail_index]
            self.array[self.tail_index] = None
            self.tail_index = self.tail_index - 1 if self.tail_index - 1 >= 0 else self.capacity - 1
            self.count -= 1

        if self.count == 0:
            self.head_index = None
            self.tail_index = None
        elif self.count == 1:
            self.head_index = self.tail_index

        return result

# 7.6.* Функция проверки баланса скобок.

# Было выполнено в 6 пункте темы "4. Стек"
