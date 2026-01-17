from task4 import Stack
import ctypes

class Queue2:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)

    # 3. Ввращаем очередь по кругу на N элементов.
    def rotate(self, N):
        for _ in range(N):
            self.enqueue(self.dequeue())

# 4.Очередь на двух стеках.
class Queue3:
    def __init__(self):
        self.stack1 = Stack()
        self.stack2 = Stack()
        self.isNaturalOrder = True

    def enqueue(self, item):
        if self.isNaturalOrder:
            self.stack1.push(item)
        else:
            self.isNaturalOrder = not self.isNaturalOrder
            while self.stack2.size() != 0:
                self.stack1.push(self.stack2.pop())
            self.stack1.push(item)

    def dequeue(self):
        if self.isNaturalOrder:
            self.isNaturalOrder = not self.isNaturalOrder
            while self.stack1.size() > 1:
                self.stack2.push(self.stack1.pop())
            return self.stack1.pop()
        else:
            return self.stack2.pop()

    # 5. Обращает все элементы в очереди в обратном порядке.
    def reverse(self):
        self.isNaturalOrder = not self.isNaturalOrder
        temp = self.stack1
        self.stack1 = self.stack2
        self.stack2 = temp

    def size(self):
        if self.isNaturalOrder:
            return self.stack1.size()
        else:
            return self.stack2.size()

# 6. Круговая очередь.
class Queue4:

    def __init__(self, new_capacity):
        self.count = 0
        self.capacity = new_capacity
        self.array = (new_capacity * ctypes.py_object)()
        self.pointer = 0

    def enqueue(self, item):
        if self.count != self.capacity:
            index = (self.pointer + self.count) % self.capacity
            self.array[index] = item
            self.count += 1

    def dequeue(self):
        if self.count == 0:
            return None
        result = self.array[self.pointer]
        self.array[self.pointer] = None
        self.pointer = (self.pointer + 1) % self.capacity
        self.count -= 1
        return result

    def size(self):
        return self.count
