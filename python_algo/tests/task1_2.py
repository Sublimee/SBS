from task1 import LinkedList, Node

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

