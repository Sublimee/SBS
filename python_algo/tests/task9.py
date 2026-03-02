class NativeDictionary:
    def __init__(self, sz):
        self.size = sz
        self.slots = [None] * self.size
        self.values = [None] * self.size

    def hash_fun(self, key):
        if not key:
            return 0
        h = 0
        for ch in key:
            h = (31 * h + ord(ch)) & 0xFFFFFFFF
        return h % self.size

    def is_key(self, key):
        slot = self._seek_slot(key)
        if slot is not None and self.slots[slot] == key:
            return True
        return False

    def put(self, key, value):
        slot = self._seek_slot(key)
        self.slots[slot] = key
        self.values[slot] = value

    def get(self, key):
        slot = self._seek_slot(key)
        if slot is None:
            return None
        return self.values[slot]

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