# Рефлексия

# 9. Слияние двух упорядоченных списков в один.

# Решение идентично.

# 10. Проверка наличия заданного упорядоченного под-списка в текущем списке.

# Решение идентично.

# 11. Ищем наиболее часто встречающееся значение в списке.

# Решение идентично.

# 12. Индекс заданного элемента в списке за O(log N).

# По исходной постановке не реализовал именно по причине того, что "для его работы требуется возможность индексации
# элементах упорядоченного списка, для чего в реализации можно использовать динамический массив.". Кажется, что
# список -- просто неподходящая для такой задачи структура и при необходимости поиска за O(log N) нужно сразу
# переходить к динамическому массиву.


# Дополнительные задачи

# 5.* Словарь с использованием упорядоченного списка.

# Временная сложность операций:
# вставки: O(N)
# удаления: O(N)
# поиска: O(N)

# Сложность каждой из операций завязана на сложности поиска. Если применить бинарный поиск, то сложность всех операций
# станет логарифмической.

class Node:
    def __init__(self, k, v):
        self.key = k
        self.value = v
        self.prev = None
        self.next = None


class OrderedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def compare(self, v1, v2):
        if v1 < v2:
            result = -1
        elif v1 == v2:
            result = 0
        else:
            result = 1
        return result

    def add(self, key, value):
        new_node = Node(key, value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.count += 1
            return

        current = self.head

        while current is not None and self.compare(current.key, key) == -1:
            current = current.next

        if current is None:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        elif current.prev is None:
            new_node.next = current
            current.prev = new_node
            self.head = new_node
        else:
            new_node.next = current
            new_node.prev = current.prev
            new_node.next.prev = new_node
            new_node.prev.next = new_node

        self.count += 1


    def find(self, key):
        current = self.head
        while current is not None:
            if current.key == key or self.compare(key, current.key) == -1:
                break
            current = current.next

        if current and current.key == key:
            return current
        return None


    def delete(self, key):
        to_delete = self.find(key)
        if to_delete is None:
            return

        next_node = to_delete.next
        prev_node = to_delete.prev

        if prev_node is None:
            self.head = next_node
        else:
            prev_node.next = next_node

        if next_node is None:
            self.tail = prev_node
        else:
            next_node.prev = prev_node

        self.count -= 1


class OrderedStringList(OrderedList):
    def __init__(self):
        super(OrderedStringList, self).__init__()

    def compare(self, v1, v2):
        v1_normalized = v1.strip()
        v2_normalized = v2.strip()
        if v1_normalized < v2_normalized:
            result = -1
        elif v1_normalized == v2_normalized:
            result = 0
        else:
            result = 1
        return result

class NativeDictionary2:
    def __init__(self):
        self.pairs = OrderedStringList()

    def is_key(self, key):
        pair = self.pairs.find(key)
        if pair is None:
            return False
        return True

    def put(self, key, value):
        pair = self.pairs.find(key)
        if pair is None:
            self.pairs.add(key, value)
            return
        pair.value = value

    def get(self, key):
        pair = self.pairs.find(key)
        if pair is None:
            return None
        return pair.value

    def delete(self, key):
        self.pairs.delete(key)


# 6.* Создайте словарь, в котором ключи представлены битовыми строками фиксированной длины.

# Вероятно, сделал не то, так как не сообразил, как выполнить "Реализуйте методы добавления, удаления и поиска
# элементов, используя битовые операции для ускорения работы.". Ускорение hash_fun есть, но в других методах
# используется лишь косвенно.

class NativeDictionary3:
    def __init__(self, sz):
        self.size = sz
        self.slots = [None] * self.size
        self.values = [None] * self.size

    # Предусловие:
    # key -- строка вида "0101..." фиксированной длины со значением в двоичной системе счисления, не превышающим размер
    # словаря
    def hash_fun(self, key):
        return int(key, 2)

    # Предусловие:
    # key -- строка вида "0101..." фиксированной длины со значением в двоичной системе счисления, не превышающим размер
    # словаря
    def is_key(self, key):
        slot = self._seek_slot(key)
        if slot is not None and self.slots[slot] == key:
            return True
        return False

    # Предусловие:
    # key -- строка вида "0101..." фиксированной длины со значением в двоичной системе счисления, не превышающим размер
    # словаря
    def put(self, key, value):
        slot = self._seek_slot(key)
        self.slots[slot] = key
        self.values[slot] = value

    # Предусловие:
    # key -- строка вида "0101..." фиксированной длины со значением в двоичной системе счисления, не превышающим размер
    # словаря
    def get(self, key):
        slot = self._seek_slot(key)
        if slot is None:
            return None
        return self.values[slot]

    # Предусловие:
    # key -- строка вида "0101..." фиксированной длины со значением в двоичной системе счисления, не превышающим размер словаря
    def _seek_slot(self, key):
        init_index = self.hash_fun(key)

        if self.slots[init_index] is None or self.slots[init_index] == key:
            return init_index

        next_index = (init_index + 1) % self.size
        while next_index != init_index:
            if self.slots[next_index] is None or self.slots[next_index] == key:
                return next_index
            next_index = (next_index + 1) % self.size

        return None