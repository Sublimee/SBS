from typing import Any
from __future__ import annotations

class PowerSet:

    def __init__(self) -> None:
        self.hashtable = HashTable(100000, 1)

    def size(self) -> int:
        return self.hashtable.count()

    def put(self, value: Any) -> None:
        self.hashtable.put(value)

    def get(self, value: Any) -> bool:
        found = self.hashtable.find(value)
        if found is not None:
            return True
        return False

    def remove(self, value: Any) -> bool:
        return self.hashtable.remove(value)

    def intersection(self, set2: PowerSet) -> PowerSet:
        result = PowerSet()

        for value in self.hashtable.slots:
            if value is not None and set2.get(value):
                result.put(value)

        return result

    def union(self, set2: PowerSet) -> PowerSet:

        result = PowerSet()

        for value in self.hashtable.slots:
            if value is not None:
                result.put(value)

        for value in set2.hashtable.slots:
            if value is not None:
                result.put(value)

        return result


    def difference(self, set2: PowerSet) -> PowerSet:
        result = PowerSet()

        for value in self.hashtable.slots:
            if value is not None and set2.get(value) is False:
                result.put(value)

        return result

    def issubset(self, set2: PowerSet) -> bool:
        for value in set2.hashtable.slots:
            if value is not None and self.get(value) is False:
                return False

        return True

    def equals(self, set2: PowerSet) -> bool:
        for value in self.hashtable.slots:
            if value is not None and set2.get(value) is False:
                return False

        for value in set2.hashtable.slots:
            if value is not None and self.get(value) is False:
                return False

        return True


class HashTable:
    def __init__(self, sz, stp):
        self.size = sz
        self.step = stp
        self.slots = [None] * self.size
        self._count = 0

    def count(self):
        return self._count

    def hash_fun(self, value):
        return hash(value) % self.size

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
            pass

        if self.slots[slot] is None:
            self._count += 1

        self.slots[slot] = value

    def find(self, value):
        slot = self.seek_slot(value)
        if slot is None or self.slots[slot] != value:
            return None
        return slot

    def remove(self, value) -> bool:
        slot = self.seek_slot(value)
        if slot is not None and self.slots[slot] == value:
            self.slots[slot] = None
            self._count -= 1
            return True
        return False
