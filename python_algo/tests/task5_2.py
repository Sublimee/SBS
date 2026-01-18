from task4 import Stack
import ctypes

# 3. Вращаем очередь по кругу на N элементов.

# Рефлексия: добавлен метод rotate, который берет элементы из головы очереди и кладет их в конец очереди. Таким образом
# достигается круговой сдвиг на N элементов.

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

    def rotate(self, N):
        for _ in range(N):
            self.enqueue(self.dequeue())

# 4. Очередь на двух стеках.

# Рефлексия: один стек используем для того, чтобы добавлять элементы, а второй -- для того, чтобы извлекать элементы.
# Только один из стеков может быть заполнен элементами. Какую операцию можем выполнять определятся is_pushable. При
# перетекании элементов из стека в стек при смене is_pushable они меняются порядком.

class Queue3:
    def __init__(self):
        self.stack1 = Stack()
        self.stack2 = Stack()
        self.is_pushable = True

    def enqueue(self, item):
        if self.is_pushable:
            self.stack1.push(item)
        else:
            self.is_pushable = not self.is_pushable
            while self.stack2.size() != 0:
                self.stack1.push(self.stack2.pop())
            self.stack1.push(item)

    def dequeue(self):
        if self.is_pushable:
            self.is_pushable = not self.is_pushable
            while self.stack1.size() > 1:
                self.stack2.push(self.stack1.pop())
            return self.stack1.pop()
        else:
            return self.stack2.pop()

    # 5. Обращает все элементы в очереди в обратном порядке.

    # Рефлексия:
    # При использовании двух стеков они должны поменяться ролями: стек из которого забирали -- в него пушим, а в который
    # пушили -- теперь из него забираем. Для этого также нужно инвертировать is_pushable.
    def reverse(self):
        self.is_pushable = not self.is_pushable
        temp = self.stack1
        self.stack1 = self.stack2
        self.stack2 = temp

    def size(self):
        if self.is_pushable:
            return self.stack1.size()
        else:
            return self.stack2.size()

# 6. Круговая очередь.

# Рефлексия:
# Добавляем и удаляем элементы используя сдвиг относительно pointer. При переходе через границу массива нужна операция
# (self.pointer + self.count) % self.capacity
# для возвращения к началу массива.
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
