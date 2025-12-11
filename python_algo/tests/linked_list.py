class Node:

    def __init__(self, v):
        self.value = v
        self.next = None

class LinkedList:

    def __init__(self):
        self.head = None
        self.tail = None

    def add_in_tail(self, item):
        if self.head is None:
            self.head = item
        else:
            self.tail.next = item
        self.tail = item

    def print_all_nodes(self):
        node = self.head
        while node != None:
            print(node.value)
            node = node.next

    def find(self, val):
        node = self.head
        while node is not None:
            if node.value == val:
                return node
            node = node.next
        return None

    def find_all(self, val):
        result = []
        node = self.head
        while node is not None:
            if node.value == val:
                result.append(node)
            node = node.next
        return result

    def delete(self, val, all=False):
        prev = None
        current = self.head

        while current is not None:
            if current.value == val:
                if prev is None:
                    if current.next is not None:
                        self.head = current.next
                        current = current.next
                    else:
                        self.head = None
                        self.tail = None
                        return
                else:
                    if current.next is not None:
                        prev.next = current.next
                        current = current.next
                    else:
                        current = None
                        prev.next = current
                        self.tail = prev
                if not all:
                    return
            else:
                prev = current
                current = current.next

    def clean(self):
        self.head = None
        self.tail = None

    def len(self):
        result = 0
        node = self.head
        while node is not None:
            result += 1
            node = node.next
        return result

    def insert(self, afterNode, newNode):
        if (afterNode is None):
            newNode.next = self.head
            if newNode.next is None:
                self.tail = newNode
            self.head = newNode
            return
        current = self.head

        while current is not afterNode and current is not None:
            current = current.next

        if current is not None:
            next = current.next
            if next is None:
                self.tail = newNode
            current.next = newNode
            newNode.next = next

def build_linked_list(values):
    ll = LinkedList()
    for v in values:
        ll.add_in_tail(Node(v))
    return ll


def to_array(ll: LinkedList):
    result = []
    node = ll.head
    while node is not None:
        result.append(node.value)
        node = node.next
    return result

def sum_linked_lists(ll1: LinkedList, ll2: LinkedList) -> LinkedList | None:
    if ll1 is None or ll2 is None or ll1.len() != ll2.len():
        return None

    result = LinkedList()
    current1 = ll1.head
    current2 = ll2.head

    while current1 is not None:
        result.add_in_tail(Node(current1.value + current2.value))
        current1 = current1.next
        current2 = current2.next

    return result