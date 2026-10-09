import ctypes

# 5.* Динамический массив на основе банковского метода.
class DynArrayBank:

    MIN_CAPACITY = 16

    def __init__(self):
        self.count = 0
        self.capacity = self.MIN_CAPACITY
        self.array = self.make_array(self.capacity)
        self._credits = 0


    def get_credits(self):
        return self._credits

    def _charge(self):
        self._credits += 3

    def _pay(self, cost: int):
        self._credits -= cost
        if self._credits < 0:
            raise Exception("Negative balance")

    def _next_power_of_two(self, x):
        return 1 if x == 0 else 2**(x - 1).bit_length()

    def __len__(self):
        return self.count

    def make_array(self, new_capacity):
        return (new_capacity * ctypes.py_object)()

    def __getitem__(self,i):
        if i < 0 or i >= self.count:
            raise IndexError('Index is out of bounds')
        return self.array[i]

    def resize(self, new_capacity):
        new_array = self.make_array(new_capacity)
        for i in range(self.count):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity

        self._pay(self.count)

    def append(self, itm):
        self._charge()
        if self.count == self.capacity:
            needed = self.count + 1
            new_capacity = self._next_power_of_two(needed)
            self.resize(new_capacity)
        self.array[self.count] = itm
        self.count += 1

    def insert(self, i, itm):
        if i < 0 or i > self.count:
            raise IndexError('Index is out of bounds')

        self._charge()

        if self.count == self.capacity:
            needed = self.count + 1
            new_capacity = self._next_power_of_two(needed)
            self.resize(new_capacity)
        for j in range(self.count, i, -1):
            self.array[j] = self.array[j-1]
        self.array[i] = itm
        self.count += 1

    def delete(self, i):
        if i < 0 or i >= self.count:
            raise IndexError('Index is out of bounds')

        self._charge()

        for j in range(i, self.count - 1):
            self.array[j] = self.array[j + 1]
        self.array[self.count - 1] = None
        self.count -= 1
        if self.capacity > self.MIN_CAPACITY and (2 * self.count < self.capacity):
            self.resize(max(self.MIN_CAPACITY, int(self.capacity / 1.5)))

# 6.* Многомерный динамический массив.

class DynArray2:

    def __init__(self, capacity):
        if capacity < 0:
            raise Exception('Incorrect capacity')
        self.count = 0
        self.capacity = capacity
        self.array = self.make_array(self.capacity)

    def __len__(self):
        return self.count

    def make_array(self, new_capacity):
        return (new_capacity * ctypes.py_object)()

    def __getitem__(self,i):
        if i < 0 or i >= self.count:
            raise IndexError('Index is out of bounds')
        return self.array[i]

    def resize(self, new_capacity):
        new_array = self.make_array(new_capacity)
        for i in range(self.count):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity

    def append(self, itm):
        if self.count == self.capacity:
            self.resize(2 * self.capacity)
        self.array[self.count] = itm
        self.count += 1

    def insert(self, i, itm):
        if i < 0 or i > self.count:
            raise IndexError('Index is out of bounds')
        if self.count == self.capacity:
            self.resize(2*self.capacity)
        for j in range(self.count, i, -1):
            self.array[j] = self.array[j-1]
        self.array[i] = itm
        self.count += 1

    def delete(self, i):
        if i < 0 or i >= self.count:
            raise IndexError('Index is out of bounds')
        for j in range(i, self.count - 1):
            self.array[j] = self.array[j + 1]
        self.array[self.count - 1] = None
        self.count -= 1

class MultiDynArray:

    def __init__(self, sizes):
        if len(sizes) < 1:
            raise Exception('Incorrect dimensions count')
        if any(size <= 0 for size in sizes):
            raise Exception('Incorrect dimension size')

        self.dimensions = len(sizes)
        self._root = DynArray2(sizes[0])
        self._init_level(self._root, 0, sizes)

    def _init_level(self, arr: DynArray2, level: int, sizes):
        if level == self.dimensions - 1:
            return

        current_dimension_capacity = sizes[level]
        next_dimension_capacity = sizes[level + 1]

        for _ in range(current_dimension_capacity):
            child = DynArray2(next_dimension_capacity)
            self._init_level(child, level + 1, sizes)
            arr.append(child)


    def __getitem__(self, indices):
        normalized_indices = self.normalize_indices(indices)

        try:
            arr = self._root

            for level in range(self.dimensions):
                index = normalized_indices[level]
                if level < self.dimensions - 1:
                    arr = arr[index]
                else:
                    return arr[index]

        except Exception as e:
            raise IndexError('Index is out of bounds') from e

    def append(self, indices, itm):
        try:
            normalized_indices = self.normalize_indices(indices)
            self.check_itm(itm, normalized_indices)

            arr = self._root
            position = len(normalized_indices)

            for level in range(position):
                i = normalized_indices[level]
                arr = arr[i]

            arr.append(itm)

        except Exception as e:
            raise IndexError('Index is out of bounds') from e

    def insert(self, indices, itm):
        try:
            normalized_indices = self.normalize_indices(indices)
            self.check_itm(itm, normalized_indices)

            arr = self._root

            for level in range(len(normalized_indices) - 1):
                i = normalized_indices[level]
                arr = arr[i]

            arr.insert(normalized_indices[-1], itm)

        except Exception as e:
            raise IndexError('Index is out of bounds') from e


    def delete(self, indices):
        try:
            normalized_indices = self.normalize_indices(indices)

            arr = self._root

            for level in range(len(normalized_indices) - 1):
                i = normalized_indices[level]
                arr = arr[i]

            arr.delete(normalized_indices[-1])

        except Exception as e:
            raise IndexError('Index is out of bounds') from e

    def normalize_indices(self, indices) -> tuple:
        if isinstance(indices, tuple):
            return indices
        else:
            return (indices,)

    def check_itm(self, itm, normalized_indices: tuple):
        if len(normalized_indices) < (self.dimensions - 1) and not isinstance(itm, DynArray2):
            raise Exception('Incorrect value type')
