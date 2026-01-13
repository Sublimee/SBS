class Stack:
    def __init__(self):
        self.stack = []

    def size(self):
        return len(self.stack)

    # O(1)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    # O(1)
    def push(self, value):
        self.stack.append(value)

    def peek(self):
        if self.size() > 0:
            return self.stack[self.size() - 1]
        else:
            return None