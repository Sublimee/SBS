from task11 import BloomFilter

# Рефлексия

# 5. Словарь с использованием упорядоченного списка по ключу.

# В моей доработанной реализации узла сразу хранится и значение и ключ. Это позволяет не вводить второй список. Вдобавок
# к этому удаление элементов в моем варианте проще: не требуется пересчитывать индексы в списке с ключами.


# 2.* Алгоритм слияния нескольких фильтров Блюма.

# вероятность ложного срабатывания увеличится, так как итоговый фильтр представляет собой "сумму" менее наполненных фильтров
def merge(filters):
    result = BloomFilter(filters[0].filter_len)

    for f in filters:
        result.bit_array |= f.bit_array

    return result

# 3.* Реализуйте удаление элементов.

class BloomFilterWithRemove:

    def __init__(self, f_len):
        self.filter_len = f_len
        self.bit_array = 0
        self.counts = [0] * self.filter_len

    def hash1(self, str1):
        return self._hash(str1, 17)

    def hash2(self, str1):
        return self._hash(str1, 223)

    def _hash(self, str, random):
        result = 0
        for c in str:
            result = (result * random + ord(c)) % self.filter_len
        return result

    def add(self, str1):
        hash1 = self.hash1(str1)
        hash2 = self.hash2(str1)

        self.counts[hash1] += 1
        self.counts[hash2] += 1

        self._set_bit(hash1)
        self._set_bit(hash2)

    def remove(self, str1):
        hash1 = self.hash1(str1)
        hash2 = self.hash2(str1)

        self.counts[hash1] -= 1
        if self.counts[hash1] == 0:
            self._remove_bit(hash1)

        self.counts[hash2] -= 1
        if self.counts[hash2] == 0:
            self._remove_bit(hash2)

    def _set_bit(self, bit):
        self.bit_array |= 1 << bit

    def _remove_bit(self, bit):
        self.bit_array &= ~(1 << bit)

    def is_value(self, str1):
        return self._check_bit(self.bit_array, self.hash1(str1)) and self._check_bit(self.bit_array, self.hash2(str1))

    def _check_bit(self, bit_array, bit):
        return ((bit_array >> bit) & 1) == 1


# 4.* Восстановить исходное множество.

# Затрудняюсь. Было бы полезно при добавлении одинаковых значений в фильтр в предыдущем задании.