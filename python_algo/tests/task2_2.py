from task2 import LinkedList2, Node

# 2.10.* Перевернуть список.
# Сложность временная: O(n)
# Сложность по памяти: O(1)
def reverse(ll: LinkedList2):
    current_node = ll.tail
    ll.head = current_node
    saved = None
    while current_node is not None:
        current_node.next = current_node.prev
        current_node.prev = saved

        saved = current_node
        current_node = current_node.next
    ll.tail = saved

# 2.11.* Есть ли в списке циклы?
# Сложность временная: O(n)
# Сложность по памяти: O(1)
def has_loop(ll: LinkedList2):
    if ll.head is None:
        return False

    slow = ll.head
    fast = ll.head
    while slow is not None and fast is not None:
        slow = slow.next
        if fast.next is None:
            return False
        fast = fast.next.next

        if slow is fast:
            return True
    return False

# 2.12.* Сортировка.
# Сложность временная: O(n^2)
# Сложность по памяти: O(1)
def sort(ll: LinkedList2):
    if ll.head is None or ll.head.next is None:
        return

    is_swapped = True
    while is_swapped:
        is_swapped = False
        current = ll.head
        while current.next is not None:
            if current.value > current.next.value:
                temp = current.next.value
                current.next.value = current.value
                current.value = temp
                is_swapped = True
            current = current.next

# 2.13.* Слияние и сортировка двух списко.
# Сложность временная: O(n^2)
# Сложность по памяти: O(n)
def merge_and_sort(ll1: LinkedList2, ll2: LinkedList2):
    sort(ll1)
    sort(ll2)

    result = LinkedList2()
    next1 = ll1.head
    next2 = ll2.head
    next = get_next(next1, next2)

    while next is not None:
        if next is next1:
            next1 = next1.next
        else:
            next2 = next2.next

        result.add_in_tail(Node(next.value))
        next = get_next(next1, next2)

    return result

def get_next(node1: Node, node2: Node):
    if node1 is None:
        return node2
    if node2 is None:
        return node1
    if node1.value <= node2.value:
        return node1
    else:
        return node2

