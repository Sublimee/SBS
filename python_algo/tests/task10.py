from __future__ import annotations
from typing import Any

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
            if value is not None and value is not self.hashtable.PASS and set2.get(value):
                result.put(value)

        return result

    def union(self, set2: PowerSet) -> PowerSet:

        result = PowerSet()

        for value in self.hashtable.slots:
            if value is not None and value is not self.hashtable.PASS and value is not self.hashtable.PASS:
                result.put(value)

        for value in set2.hashtable.slots:
            if value is not None and value is not self.hashtable.PASS and value is not self.hashtable.PASS:
                result.put(value)

        return result


    def difference(self, set2: PowerSet) -> PowerSet:
        result = PowerSet()

        for value in self.hashtable.slots:
            if value is not None and value is not self.hashtable.PASS and set2.get(value) is False:
                result.put(value)

        return result

    def issubset(self, set2: PowerSet) -> bool:
        for value in set2.hashtable.slots:
            if value is not None and value is not set2.hashtable.PASS and self.get(value) is False:
                return False

        return True

    def equals(self, set2: PowerSet) -> bool:
        for value in self.hashtable.slots:
            if value is not None and value is not self.hashtable.PASS and set2.get(value) is False:
                return False

        for value in set2.hashtable.slots:
            if value is not None and value is not set2.hashtable.PASS and self.get(value) is False:
                return False

        return True


class HashTable:

    PASS = object()

    def __init__(self, sz, stp):
        self.size = sz
        self.step = stp
        self.slots = [None] * self.size
        self._count = 0

    def count(self):
        return self._count

    def hash_fun(self, value):
        return hash(value) % self.size

    def _seek_slot(self, key):
        index = self.hash_fun(key)
        start = index

        while True:
            if self.slots[index] is None or self.slots[index] == key:
                return index

            index = (index + self.step) % self.size
            if index == start:
                return None

    def _seek_candidate_slot_(self, key):
        index = self.hash_fun(key)
        start = index
        first_pass_index = None

        while True:
            if first_pass_index is None and self.slots[index] is self.PASS:
                first_pass_index = index

            if self.slots[index] == key:
                return index

            if self.slots[index] is None:
                return first_pass_index if first_pass_index is not None else index

            index = (index + self.step) % self.size
            if index == start:
                return first_pass_index

    def put(self, value):
        slot = self._seek_candidate_slot_(value)
        if slot is None:
            return

        if self.slots[slot] is None or self.slots[slot] is self.PASS:
            self._count += 1

        self.slots[slot] = value

    def find(self, value):
        slot = self._seek_slot(value)
        if slot is None or self.slots[slot] != value:
            return None
        return slot

    def remove(self, value) -> bool:
        slot = self._seek_slot(value)
        if slot is not None and self.slots[slot] == value:
            self.slots[slot] = self.PASS
            self._count -= 1
            return True
        return False
