class NativeCache:

    def __init__(self, sz):
        self.size = sz
        self.slots = [None] * self.size
        self.values = [None] * self.size
        self.hits = [0] * self.size

    def hash_fun(self, key):
        return hash(key) % self.size

    def get(self, key):
        slot = self._seek_slot(key)

        if slot is not None and self.slots[slot] == key:
            self.hits[slot] += 1
            return self.values[slot]

        return None

    def get_freq(self, key):
        slot = self._seek_slot(key)

        if slot is not None and self.slots[slot] == key:
            return self.hits[slot]

        return None

    def put(self, key, value):
        slot = self._seek_empty_slot(key)

        if slot is None:
            index_to_remove = self._seek_lfu_slot()
            self.slots[index_to_remove] = key
            self.values[index_to_remove] = value
            self.hits[index_to_remove] = 0
            return

        if self.slots[slot] != key:
            self.slots[slot] = key
            self.hits[slot] = 0

        self.values[slot] = value

    def _seek_slot(self, key):
        index = self.hash_fun(key)
        start = index

        while True:
            if self.slots[index] == key:
                return index

            index = (index + 1) % self.size
            if index == start:
                return None

    def _seek_empty_slot(self, key):
        index = self.hash_fun(key)
        start = index

        while True:
            if self.slots[index] is None or self.slots[index] == key:
                return index

            index = (index + 1) % self.size
            if index == start:
                return None

    def _seek_lfu_slot(self):
        min_index = 0

        for i in range(1, self.size):
            if self.hits[i] < self.hits[min_index]:
                min_index = i

        return min_index