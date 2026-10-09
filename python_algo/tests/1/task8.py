class HashTable:
    def __init__(self, sz, stp):
        self.size = sz
        self.step = stp
        self.slots = [None] * self.size

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