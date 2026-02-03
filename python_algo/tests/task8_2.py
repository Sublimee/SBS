# Рефлексия


# 4. Проверка строки на палиндром.

# Решение идентично.


# 5. Минимальный элемент деки за O(1).

# Я думал над такой реализацией, но не понял что делать если мы столкнемся с такой последовательностью:

# addTail 5
# добавляем 5 в конец дополнительной деки
# -> [5]

# addTail 6
# добавляем 6 в конец дополнительной деки
# -> [5, 6]

# addTail 4
# удаляем элементы из конца дополнительной деки, пока её последний элемент больше или равен 4
# -> []
# добавляем 4 в конец дополнительной деки
# -> [4]

# В дополнительной деке остался всего один элемент, который не соотносится с декой со значениями. Вероятно, я что-то не
# понимаю.


# 6. Двусторонняя очередь на базе динамического массива.

# Мной была реализована очередь в диначисеском массиве



# Решения

# 3.* Динамическая хэш-таблица

class HashTable2:
    def __init__(self, sz, stp):
        self.size = sz
        self.step = stp
        self.slots = [None] * self.size
        self.count = 0

    def hash_fun(self, str):
        if not str:
            return 0
        h = 0
        for ch in str:
            h = (31 * h + ord(ch)) & 0xFFFFFFFF
        return h % self.size

    def seek_slot(self, value):
        init_index = self.hash_fun(value)

        if self.slots[init_index] is None or self.slots[init_index] == value:
            return init_index

        next_index = (init_index + self.step) % self.size
        while next_index != init_index:
            if self.slots[next_index] is None or self.slots[next_index] == value:
                return next_index
            next_index = (next_index + self.step) % self.size

        return None

    def put(self, value):
        if (self.count + 1) / self.size > 0.75:
            self.resize()

        slot = self.seek_slot(value)
        if slot is None:
            return None

        if self.slots[slot] is None:
            self.count += 1

        self.slots[slot] = value

        return slot

    def resize(self):
        old_slots = self.slots
        self.size = self.size * 2
        self.slots = [None] * self.size
        self.count = 0
        if self.step % 2 == 0:
            self.step += 1
        for x in old_slots:
            if x is not None:
                self.put(x)

    def find(self, value):
        slot = self.seek_slot(value)
        if slot is None or self.slots[slot] != value:
            return None
        return slot

# 4.* Двойное хэширование

# Как и ранее операции вставки и поиска в лучшем случае выполняются за O(1), в худшем — за O(N). Однако в среднем, при
# удачном выборе hash_fun2, решение будет выдавать лучшие результаты, за счёт того, статичный шаг хуже динамически
# вычисляемого при возникновении коллизии.

class DoubleHashTable:
    def __init__(self, sz):
        self.size = sz
        self.slots = [None] * self.size

    def hash_fun(self, s):
        if not s:
            return 0
        h = 0
        for ch in s:
            h = (31 * h + ord(ch)) & 0xFFFFFFFF
        return h % self.size

    def hash_fun2(self, s):
        if not s:
            return 1
        h = 0x12345678
        for ch in s:
            h = (31 * h + ord(ch)) & 0xFFFFFFFF
        return (h % (self.size - 1)) + 1

    def seek_slot(self, value):
        init_index = self.hash_fun(value)
        step = 1 + (self.hash_fun2(value) % (self.size - 1))

        if self.slots[init_index] is None or self.slots[init_index] == value:
            return init_index

        next_index = (init_index + step) % self.size
        while next_index != init_index:
            if self.slots[next_index] is None or self.slots[next_index] == value:
                return next_index
            next_index = (next_index + step) % self.size

        return None

    def put(self, value):
        slot = self.seek_slot(value)
        if slot is None:
            return None
        self.slots[slot] = value
        return slot

    def find(self, value):
        slot = self.seek_slot(value)
        if slot is None or self.slots[slot] != value:
            return None
        return slot

# 5.* Хэш-таблица с солью

class HashTableSalted:
    def __init__(self, sz, stp, salt):
        self.salt = salt
        self.size = sz
        self.step = stp
        self.slots = [None] * self.size

    def hash_fun(self, str):
        if not str:
            return 0
        h = self.salt
        for ch in str:
            h = (31 * h + ord(ch)) & 0xFFFFFFFF
        return h % self.size

    def seek_slot(self, value):
        init_index = self.hash_fun(value)

        if self.slots[init_index] is None or self.slots[init_index] == value:
            return init_index

        next_index = (init_index + self.step) % self.size
        while next_index != init_index:
            if self.slots[next_index] is None or self.slots[next_index] == value:
                return next_index
            next_index = (next_index + self.step) % self.size

        return None

    def put(self, value):
        slot = self.seek_slot(value)
        if slot is None:
            return None
        self.slots[slot] = value
        return slot

    def find(self, value):
        slot = self.seek_slot(value)
        if slot is None or self.slots[slot] != value:
            return None
        return slot