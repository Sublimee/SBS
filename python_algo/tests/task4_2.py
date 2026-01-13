# 2. Работаем с головой.

class Stack2:
    def __init__(self):
        self.stack = []

    def size(self):
        return len(self.stack)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop(0)
        else:
            return None

    def push(self, value):
        self.stack.insert(0, value)

    def peek(self):
        if self.size() > 0:
            return self.stack[0]
        else:
            return None

# 3. Как отработает?
# while stack.size() > 0:
#     print(stack.pop())
#     print(stack.pop())

# Возможны три варианта: ничего не выведется на экран, выведется только одно значение (верхушка стека, будучи единственным элементом), выведутся два значения (верхушка стека и следующее за ним значение).

# 4. Оцените меру сложности для операций pop и push.

# O(N) и O(N)

# 5. Проверка сбаласированности скобок ( и )

def validate(s):
    stack = Stack2()
    for ch in s:
        if ch == '(':
            stack.push('(')
        else:
            popped = stack.pop()
            if popped is None:
                return False
    if stack.size() > 0:
        return False
    return True

# 6. Проверка сбаласированности скобок (), {}, [].

def validate2(s):
    stack = Stack2()

    for ch in s:
        if ch == '(' or ch == '{' or ch == '[':
            stack.push(ch)
        elif ch == ')':
            popped = stack.pop()
            if popped is None or popped != '(':
                return False
        elif ch == '}':
            popped = stack.pop()
            if popped is None or popped != '{':
                return False
        elif ch == ']':
            popped = stack.pop()
            if popped is None or popped != '[':
                return False

    if stack.size() > 0:
        return False
    return True

# 7. Возвращать текущий минимальный элемент за O(1).

# Идею решения позаимствовал.

class MinStack:
    def __init__(self):
        self.stack = []
        self.mins = []

    def size(self):
        return len(self.stack)

    def pop(self):
        if self.size() > 0:
            self.mins.pop()
            return self.stack.pop()
        else:
            return None

    def min(self):
        if len(self.mins) > 0:
            return self.mins[len(self.mins) - 1]
        else:
            return None

    def push(self, value):
        self.stack.append(value)
        if (self.min() is not None) and (value > self.min()):
            self.mins.append(self.min())
        else:
            self.mins.append(value)

    def peek(self):
        if self.size() > 0:
            return self.stack[self.size() - 1]
        else:
            return None

# 8. Возвращать среднее значение всех элементов в стеке за O(1).

class AvgStack:
    def __init__(self):
        self.stack = []
        self.sum = 0

    def size(self):
        return len(self.stack)

    def pop(self):
        if self.size() > 0:
            self.sum = self.sum - self.peek()
            return self.stack.pop()
        else:
            return None

    def push(self, value):
        self.sum = self.sum + value
        self.stack.append(value)

    def avg(self):
        if self.size() > 0:
            return self.sum / self.size()
        else:
            return None

    def peek(self):
        if self.size() > 0:
            return self.stack[self.size() - 1]
        else:
            return None

# 9 Разбор арифметических выражений.

def process(s):
    s1 = Stack2()
    s2 = Stack2()

    vars = s.split()
    i = len(vars) - 1
    while i >= 0:
        s1.push(vars[i])
        i -= 1


    while s1.size() > 0:
        next = s1.pop()

        if next == "=":
            return s2.pop()
        elif next is "+":
            b = s2.pop()
            a = s2.pop()
            s2.push(int(a) + int(b))
        elif next is "*":
            b = s2.pop()
            a = s2.pop()
            s2.push(int(a) * int(b))
        else:
            s2.push(next)