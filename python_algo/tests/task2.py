class Node:
    def __init__(self, v):
        self.value = v
        self.prev = None
        self.next = None

class LinkedList2:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_in_tail(self, item):
        if self.head is None:
            self.head = item
            item.prev = None
            item.next = None
        else:
            self.tail.next = item
            item.prev = self.tail
        self.tail = item

    def add_in_head(self, newNode):
        if self.head is None:
            self.tail = newNode
            newNode.next = None
        else:
            newNode.next = self.head
            self.head.prev = newNode

        newNode.prev = None
        self.head = newNode

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
        current_node = self.head

        while current_node is not None:
            if current_node.value == val:
                next_node = current_node.next
                prev_node = current_node.prev

                if prev_node is None:
                    self.head = next_node
                else:
                    prev_node.next = next_node

                if next_node is None:
                    self.tail = prev_node
                else:
                    next_node.prev = prev_node

                if not all:
                    return
                current_node = next_node
            else:
                current_node = current_node.next

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
        if afterNode is None:
            self.add_in_tail(newNode)
            return

        current_node = self.head
        while current_node is not afterNode and current_node is not None:
            current_node = current_node.next

        if current_node is None:
            return

        newNode.next = current_node.next
        newNode.prev = current_node

        if current_node.next is None:
            self.tail = newNode
        else:
            current_node.next.prev = newNode

        current_node.next = newNode

