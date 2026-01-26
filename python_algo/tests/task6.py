class Node:
    def __init__(self, v):
        self.value = v
        self.prev = None
        self.next = None

class Deque:
    def __init__(self):
        self.elements_count = 0
        self.head = None
        self.tail = None

    def addTail(self, item):
        new_node = Node(item)
        if self.head is None:
            self.head = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
        self.tail = new_node
        self.elements_count += 1

    def addFront(self, item):
        new_node = Node(item)
        if self.head is None:
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
        self.head = new_node
        self.elements_count += 1

    def removeFront(self):
        if self.head is None:
            return None

        prev_head = self.head
        new_head = self.head.next
        if new_head is None:
            self.head = None
            self.tail = None
        else:
            self.head = new_head
            new_head.prev = None
        self.elements_count -= 1
        return prev_head.value

    def removeTail(self):
        if self.head is None:
            return None

        prev_tail = self.tail
        new_tail = prev_tail.prev
        if new_tail is None:
            self.head = None
            self.tail = None
        else:
            self.tail = new_tail
            new_tail.next = None
        self.elements_count -= 1
        return prev_tail.value

    def size(self):
        return self.elements_count