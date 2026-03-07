from task10 import PowerSet

# Рефлексия

# 3. Динамическая хэш-таблица.

# Решение идентично.

# 5. ddos хэш-таблицы и соль.

# Не сообразил, что соль можно передавать извне (если это имелось в виду). Это, кажется, сильно менее удобный API для
# пользователей, но, действительно, эффективно решает поставленную задачу. Дуамл над идеей, как получать соль
# динамически внутри метода, но в таком случае положить элемент легко, а достать невозможно).



# 4.* Декартово произведение множеств.

def cartesian_product(set1: PowerSet, set2: PowerSet):
    if set1 is None or set2 is None:
        return None

    result = PowerSet()

    for value1 in set1.hashtable.slots:
        if value1 is None:
            continue
        for value2 in set2.hashtable.slots:
            if value2 is None:
                continue
            result.put((value1, value2))

    return result


# 5.* Пересечение нескольких множеств.

def intersection_multiple(sets):
    result = sets[0]

    for s in sets:
        result = result.intersection(s)

    return result

# 6.* Bag

class Bag:
    def __init__(self, sz):
        self.size = sz
        self.slots = [None] * self.size
        self.counts = [None] * self.size

    def hash_fun(self, key):
        return hash(key) % self.size

    def put(self, key):
        slot = self._seek_slot_for_put(key)
        if slot is None:
            return
        if self.slots[slot] == key:
            self.counts[slot] += 1
        else:
            self.slots[slot] = key
            self.counts[slot] = 1

    def remove(self, key):
        slot = self._seek_slot_for_remove(key)
        if slot is None:
            return
        if self.slots[slot] != key:
            return

        if self.counts[slot] == 1:
            self.slots[slot] = None
            self.counts[slot] = 0
        else:
            self.counts[slot] -= 1

    def get_all(self):
        result = []
        for i in range(len(self.slots)):
            value = self.slots[i]
            if value is not None:
                result.append((value, self.counts[i]))
        return result

    def _seek_slot_for_remove(self, key):
        init_index = self.hash_fun(key)

        if (self.slots[init_index] is None and self.counts[init_index] is None) or self.slots[init_index] == key:
            return init_index

        next_index = (init_index + 1) % self.size
        while next_index != init_index:
            if (self.slots[next_index] is None and self.counts[next_index] is None) or self.slots[next_index] == key:
                return next_index
            next_index = (next_index + 1) % self.size

        return None

    def _seek_slot_for_put(self, key):
        init_index = self.hash_fun(key)

        if self.slots[init_index] is None or self.slots[init_index] == key:
            return init_index

        next_index = (init_index + 1) % self.size
        while next_index != init_index:
            if self.slots[next_index] is None or self.slots[next_index] == key:
                return next_index
            next_index = (next_index + 1) % self.size

        return None