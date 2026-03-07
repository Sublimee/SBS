class BloomFilter:

    def __init__(self, f_len):
        self.filter_len = f_len
        self.bit_array = 0


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
        self._set_bit(self.hash1(str1))
        self._set_bit(self.hash2(str1))

    def _set_bit(self, bit):
        self.bit_array |= 1 << bit

    def is_value(self, str1):
        return self._check_bit(self.bit_array, self.hash1(str1)) and self._check_bit(self.bit_array, self.hash2(str1))

    def _check_bit(self, bit_array, bit):
        return ((bit_array >> bit) & 1) == 1

