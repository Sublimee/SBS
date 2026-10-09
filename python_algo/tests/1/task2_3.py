import unittest
from task2 import LinkedList2, Node
from task2_2 import reverse, has_loop, sort, merge_and_sort

class TestFind(unittest.TestCase):

    def test_1(self):
        ll = LinkedList2()
        self.assertIsNone(ll.find(10))

    def test_2(self):
        ll = build_linked_list([1, 2, 3])
        self.assertIsNone(ll.find(99))

    def test_3(self):
        ll = build_linked_list([7])
        node = ll.find(7)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 7)
        self.assertIs(node, ll.head)
        self.assertIs(node, ll.tail)
        assert_order(self, ll)

    def test_4(self):
        ll = build_linked_list([7, 8, 9])
        node = ll.find(7)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 7)
        self.assertIs(node, ll.head)
        self.assertIsNot(node, ll.tail)
        assert_order(self, ll)

    def test_5(self):
        ll = build_linked_list([7, 8, 9])
        node = ll.find(9)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 9)
        self.assertIsNot(node, ll.head)
        self.assertIs(node, ll.tail)
        assert_order(self, ll)

    def test_6(self):
        ll = build_linked_list([1, 2, 3, 2, 4])
        node = ll.find(2)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 2)
        self.assertIs(node, ll.head.next)
        assert_order(self, ll)

class TestDelete(unittest.TestCase):

    # удалить элемент в списке длиной 0
    def test_1(self):
        ll = build_linked_list([])
        ll.delete(42)
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(to_array(ll), [])

    # удалить единственный подходящий элемент в списке длиной 1
    def test_2(self):
        ll = build_linked_list([42])
        ll.delete(42)
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(to_array(ll), [])
        assert_order(self, ll)

    # удалить единственный подходящий элемент в списке длиной 2, идущий первым
    def test_3(self):
        ll = build_linked_list([42, 43])
        ll.delete(42)
        self.assertEqual(ll.head.value, 43)
        self.assertEqual(ll.tail.value, 43)
        self.assertEqual(to_array(ll), [43])
        assert_order(self, ll)
    # удалить единственный подходящий элемент в списке длиной 2, идущий последним
    def test_4(self):
        ll = build_linked_list([42, 43])
        ll.delete(43)
        self.assertEqual(ll.head.value, 42)
        self.assertEqual(ll.tail.value, 42)
        self.assertEqual(to_array(ll), [42])
        assert_order(self, ll)

    # удалить один из подходящих элементов в списке длиной 3, идущих первыми
    def test_5(self):
        ll = build_linked_list([42, 42, 43])
        ll.delete(42)
        self.assertEqual(to_array(ll), [42, 43])
        self.assertEqual(ll.head.value, 42)
        self.assertEqual(ll.tail.value, 43)
        assert_order(self, ll)

    # удалить один из подходящих элементов в списке длиной 3, идущих последними
    def test_6(self):
        ll = build_linked_list([42, 43, 43])
        ll.delete(43)
        self.assertEqual(to_array(ll), [42, 43])
        self.assertEqual(ll.head.value, 42)
        self.assertEqual(ll.tail.value, 43)
        assert_order(self, ll)

    # удалить один из подходящих элементов в длинном списке, идущих не первыми и последним
    def test_7(self):
        ll = build_linked_list([1, 2, 3, 2])
        ll.delete(2)
        self.assertEqual(to_array(ll), [1, 3, 2])
        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.tail.value, 2)
        assert_order(self, ll)

    # удалить один из подходящих элементов в длинном списке, идущих первыми
    def test_8(self):
        ll = build_linked_list([2, 2, 3, 4])
        ll.delete(2)
        self.assertEqual(to_array(ll), [2, 3, 4])
        self.assertEqual(ll.head.value, 2)
        self.assertEqual(ll.tail.value, 4)
        assert_order(self, ll)

    # удалить единственный подходящий элемент в длинном списке, идущий первым
    def test_9(self):
        ll = build_linked_list([10, 20, 30])
        ll.delete(10)
        self.assertEqual(to_array(ll), [20, 30])
        self.assertEqual(ll.head.value, 20)
        self.assertEqual(ll.tail.value, 30)
        assert_order(self, ll)

    # удалить единственный подходящий элемент в длинном списке, идущий последним
    def test_10(self):
        ll = build_linked_list([10, 20, 30])
        ll.delete(30)
        self.assertEqual(to_array(ll), [10, 20])
        self.assertEqual(ll.head.value, 10)
        self.assertEqual(ll.tail.value, 20)
        assert_order(self, ll)

    # удалить неподходящий элемент в длинном списке
    def test_11(self):
        ll = build_linked_list([1, 2, 3])
        ll.delete(99)
        self.assertEqual(to_array(ll), [1, 2, 3])
        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.tail.value, 3)
        assert_order(self, ll)

    # удалить все подходящие элементы в длинном списке, идущие не последними/первыми
    def test_12(self):
        ll = build_linked_list([1, 2, 3, 2, 2, 4])
        ll.delete(2, all=True)
        self.assertEqual(to_array(ll), [1, 3, 4])
        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.tail.value, 4)
        assert_order(self, ll)

    # удалить все подходящие элементы в длинном списке, идущие последними/первыми
    def test_13(self):
        ll = build_linked_list([2, 2, 3, 2, 2, 3, 2, 2])
        ll.delete(2, all=True)
        self.assertEqual(to_array(ll), [3, 3])
        self.assertEqual(ll.head.value, 3)
        self.assertEqual(ll.tail.value, 3)
        assert_order(self, ll)

    # удалить все подходящие элементы в длинном списке, идущие первым и не последними
    def test_14(self):
        ll = build_linked_list([2, 3, 2, 3, 2, 3])
        ll.delete(2, all=True)
        self.assertEqual(to_array(ll), [3, 3, 3])
        self.assertEqual(ll.head.value, 3)
        self.assertEqual(ll.tail.value, 3)
        assert_order(self, ll)

    # удалить все подходящие элементы в длинном списке, идущие последними и не первыми
    def test_15(self):
        ll = build_linked_list([3, 2, 3, 2, 3, 2])
        ll.delete(2, all=True)
        self.assertEqual(to_array(ll), [3, 3, 3])
        self.assertEqual(ll.head.value, 3)
        self.assertEqual(ll.tail.value, 3)
        assert_order(self, ll)

    # удалить все подходящие элементы в длинном списке
    def test_16(self):
        ll = build_linked_list([5, 5, 5])
        ll.delete(5, all=True)
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(to_array(ll), [])
        assert_order(self, ll)

class TestAddInHead(unittest.TestCase):

    def test_1(self):
        ll = LinkedList2()
        new_node = Node(10)
        ll.add_in_head(new_node)
        self.assertIs(ll.head, new_node)
        self.assertIs(ll.tail, new_node)
        self.assertEqual(to_array(ll), [10])
        assert_order(self, ll)

    def test_2(self):
        ll = build_linked_list([1, 2, 3])
        new_node = Node(99)
        ll.add_in_head(new_node)
        self.assertEqual(to_array(ll), [99, 1, 2, 3])
        self.assertIs(ll.head, new_node)
        self.assertEqual(ll.tail.value, 3)
        self.assertIsNone(ll.head.prev)
        assert_order(self, ll)

    def test_3(self):
        ll = build_linked_list([1, 2, 3])
        new_node = Node(99)
        another_new_node = Node(98)
        ll.add_in_head(new_node)
        ll.add_in_head(another_new_node)
        self.assertEqual(to_array(ll), [98, 99, 1, 2, 3])
        self.assertIs(ll.head, another_new_node)
        self.assertEqual(ll.tail.value, 3)
        self.assertIsNone(ll.head.prev)
        assert_order(self, ll)

class TestClean(unittest.TestCase):

    # очистить непустой список
    def test_1(self):
        ll = build_linked_list([1, 2, 3])
        ll.clean()
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(ll.len(), 0)
        assert_order(self, ll)

    # очистить список из одного элемента
    def test_2(self):
        ll = build_linked_list([1])
        ll.clean()
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(ll.len(), 0)
        assert_order(self, ll)


    # очистить список из двух элементов
    def test_3(self):
        ll = build_linked_list([1, 2])
        ll.clean()
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(ll.len(), 0)
        assert_order(self, ll)

    # очистить пустой список
    def test_4(self):
        ll = LinkedList2()
        ll.clean()
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(ll.len(), 0)
        assert_order(self, ll)

class TestFindAll(unittest.TestCase):

    # не должен найти значение в пустом списке
    def test_1(self):
        ll = LinkedList2()
        result = ll.find_all(10)
        self.assertEqual(result, [])

    # не должен найти значение в непустом списке
    def test_2(self):
        ll = build_linked_list([1, 2, 3])
        result = ll.find_all(99)
        self.assertEqual(result, [])
        assert_order(self, ll)

    # должен найти все значения в непустом списке
    def test_4(self):
        ll = build_linked_list([2, 2])
        result = ll.find_all(2)
        self.assertEqual(len(result), 2)
        self.assertIs(result[0], ll.head)
        self.assertIs(result[1], ll.tail)
        assert_order(self, ll)

    # должен найти значения в непустом списке
    def test_3(self):
        ll = build_linked_list([1, 2, 3, 2, 4, 2])
        result = ll.find_all(2)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(n.value == 2 for n in result))
        self.assertIs(result[0], ll.head.next)
        self.assertIs(result[1], ll.head.next.next.next)
        self.assertIs(result[2], ll.tail)

class TestLen(unittest.TestCase):

    # получить длину пустого списка
    def test_1(self):
        ll = LinkedList2()
        self.assertEqual(ll.len(), 0)

    # получить длину непустого списка
    def test_2(self):
        ll = build_linked_list([1, 2, 3])
        self.assertEqual(ll.len(), 3)

    # получить длину списка после модификации списка
    def test_len_after_ops(self):
        ll = build_linked_list([1, 2, 3])
        self.assertEqual(ll.len(), 3)
        ll.delete(2)
        self.assertEqual(ll.len(), 2)
        ll.add_in_head(Node(10))
        self.assertEqual(ll.len(), 3)
        ll.clean()
        self.assertEqual(ll.len(), 0)

class TestInsert(unittest.TestCase):

    # вставить в пустой список, когда afterNode = None
    def test_1(self):
        ll = LinkedList2()
        new_node = Node(10)
        ll.insert(None, new_node)
        self.assertEqual(to_array(ll), [10])
        self.assertIs(ll.head, new_node)
        self.assertIs(ll.tail, new_node)
        assert_order(self, ll)

    # вставить в непустой список, когда afterNode = None
    def test_2(self):
        ll = build_linked_list([1, 2, 3])
        new_node = Node(99)
        ll.insert(None, new_node)
        self.assertEqual(to_array(ll), [1, 2, 3, 99])
        self.assertIs(ll.tail, new_node)
        self.assertEqual(ll.tail.value, 99)
        assert_order(self, ll)

    # вставить в непустой список, когда задан существующий нехвостовой afterNode
    def test_3(self):
        ll = build_linked_list([1, 2, 3, 4])
        after = ll.find(2)
        new_node = Node(99)
        ll.insert(after, new_node)
        self.assertEqual(to_array(ll), [1, 2, 99, 3, 4])
        self.assertIs(new_node.prev, after)
        self.assertEqual(new_node.next.value, 3)
        assert_order(self, ll)

    # вставить в непустой список, когда задан существующий хвостовой afterNode
    def test_4(self):
        ll = build_linked_list([1, 2, 3])
        after = ll.tail
        new_node = Node(99)
        ll.insert(after, new_node)
        self.assertEqual(to_array(ll), [1, 2, 3, 99])
        self.assertIs(ll.tail, new_node)
        self.assertIs(new_node.prev, after)
        self.assertIsNone(new_node.next)
        assert_order(self, ll)

    # вставить в непустой список, когда задан несуществующий afterNode
    def test_5(self):
        ll = build_linked_list([1, 2, 3])
        foreign_node = Node(777)
        new_node = Node(99)
        ll.insert(foreign_node, new_node)
        self.assertEqual(to_array(ll), [1, 2, 3])
        assert_order(self, ll)

class TestReverse(unittest.TestCase):

    def test_1(self):
        ll = LinkedList2()
        reverse(ll)
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        assert_order(self, ll)

    def test_2(self):
        ll = build_linked_list([7])
        old_head = ll.head
        old_tail = ll.tail

        reverse(ll)

        self.assertIs(ll.head, old_head)
        self.assertIs(ll.tail, old_tail)
        self.assertEqual(to_array(ll), [7])
        assert_order(self, ll)

    def test_3(self):
        ll = build_linked_list([1, 2])
        old_head = ll.head
        old_tail = ll.tail

        reverse(ll)

        self.assertEqual(to_array(ll), [2, 1])
        self.assertIs(ll.head, old_tail)
        self.assertIs(ll.tail, old_head)
        assert_order(self, ll)

    def test_4(self):
        ll = build_linked_list([1, 2, 3, 4, 5])
        old_head = ll.head
        old_tail = ll.tail

        reverse(ll)

        self.assertEqual(to_array(ll), [5, 4, 3, 2, 1])
        self.assertIs(ll.head, old_tail)
        self.assertIs(ll.tail, old_head)
        assert_order(self, ll)

    def test_5(self):
        values = [10, 20, 30, 40]
        ll = build_linked_list(values)

        reverse(ll)
        reverse(ll)

        self.assertEqual(to_array(ll), values)
        assert_order(self, ll)

class TestHasCycle(unittest.TestCase):

    def test_1(self):
        ll = LinkedList2()
        self.assertFalse(has_loop(ll))

    def test_2(self):
        ll = build_linked_list([1])
        self.assertFalse(has_loop(ll))

    def test_3(self):
        ll = build_linked_list([1])
        ll.head.next = ll.head
        ll.tail = ll.head
        self.assertTrue(has_loop(ll))

    def test_4(self):
        ll = build_linked_list([1, 2])
        self.assertFalse(has_loop(ll))

    def test_5(self):
        ll = build_linked_list([1, 2])
        ll.head.next.next = ll.head
        ll.tail = ll.head.next
        self.assertTrue(has_loop(ll))

    def test_6(self):
        ll = build_linked_list([1, 2, 3, 4, 5])
        ll.head.next.next.next.next = ll.head.next.next
        ll.tail = ll.head.next.next.next.next
        self.assertTrue(has_loop(ll))

    def test_7(self):
        ll = build_linked_list([1, 2, 3])
        ll.head.next = ll.head
        self.assertTrue(has_loop(ll))

    def test_8(self):
        ll = build_linked_list(list(range(1, 101)))
        self.assertFalse(has_loop(ll))

class TestBubbleSort(unittest.TestCase):

    def test_1(self):
        ll = LinkedList2()
        sort(ll)
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(to_array(ll), [])
        assert_order(self, ll)

    def test_2(self):
        ll = build_linked_list([10])
        head = ll.head
        tail = ll.tail

        sort(ll)

        self.assertEqual(to_array(ll), [10])
        self.assertIs(ll.head, head)
        self.assertIs(ll.tail, tail)
        assert_order(self, ll)

    def test_3(self):
        ll = build_linked_list([1, 2, 3, 4, 5])
        sort(ll)
        self.assertEqual(to_array(ll), [1, 2, 3, 4, 5])
        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.tail.value, 5)
        assert_order(self, ll)

    def test_4(self):
        ll = build_linked_list([5, 4, 3, 2, 1])
        sort(ll)
        self.assertEqual(to_array(ll), [1, 2, 3, 4, 5])
        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.tail.value, 5)
        assert_order(self, ll)

    def test_5(self):
        ll = build_linked_list([3, 1, 2, 3, 2, 1])
        sort(ll)
        self.assertEqual(to_array(ll), [1, 1, 2, 2, 3, 3])
        assert_order(self, ll)

    def test_6(self):
        ll = build_linked_list([0, -10, 5, -3, 2])
        sort(ll)
        self.assertEqual(to_array(ll), [-10, -3, 0, 2, 5])
        self.assertEqual(to_array_reversed(ll), [5, 2, 0, -3, -10])
        assert_order(self, ll)

    def test_7(self):
        ll = build_linked_list([2, 1])
        sort(ll)
        self.assertEqual(to_array(ll), [1, 2])
        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.tail.value, 2)
        assert_order(self, ll)

    def test_8(self):
        ll = build_linked_list([7, 3, 9, 1, 7, 2, 0, 5])
        sort(ll)
        self.assertEqual(to_array(ll), sorted([7, 3, 9, 1, 7, 2, 0, 5]))
        assert_order(self, ll)

class TestMergeSorted(unittest.TestCase):

    def test_1(self):
        a = build_linked_list([])
        b = build_linked_list([])

        c = merge_and_sort(a, b)

        self.assertEqual(to_array(c), [])
        assert_order(self, c)

    def test_2(self):
        a = build_linked_list([])
        b = build_linked_list([3, 1, 2])

        c = merge_and_sort(a, b)

        self.assertEqual(to_array(c), [1, 2, 3])
        assert_order(self, c)

    def test_3(self):
        a = build_linked_list([5, 4, 6])
        b = build_linked_list([])

        c = merge_and_sort(a, b)

        self.assertEqual(to_array(c), [4, 5, 6])
        assert_order(self, c)

    def test_4(self):
        a_vals = [7]
        b_vals = [2, 6, 5]

        a = build_linked_list(a_vals)
        b = build_linked_list(b_vals)

        c = merge_and_sort(a, b)

        out = to_array(c)
        self.assertEqual(out, sorted(a_vals + b_vals))
        self.assertEqual(out, sorted(out))
        assert_order(self, c)

    def test_5(self):
        a_vals = [3, 1, 2, 2]
        b_vals = [2, 3, 1]

        a = build_linked_list(a_vals)
        b = build_linked_list(b_vals)

        c = merge_and_sort(a, b)

        out = to_array(c)
        self.assertEqual(out, sorted(a_vals + b_vals))
        assert_order(self, c)

    def test_6(self):
        a_vals = [0, -10, 5]
        b_vals = [-3, 2]

        a = build_linked_list(a_vals)
        b = build_linked_list(b_vals)

        c = merge_and_sort(a, b)

        out = to_array(c)
        self.assertEqual(out, sorted(a_vals + b_vals))
        assert_order(self, c)

    def test_7(self):
        a_vals = [10, 1, 7, 3]
        b_vals = [2]

        a = build_linked_list(a_vals)
        b = build_linked_list(b_vals)

        c = merge_and_sort(a, b)

        out = to_array(c)
        self.assertEqual(out, sorted(a_vals + b_vals))
        assert_order(self, c)

def build_linked_list(values):
    ll = LinkedList2()
    for v in values:
        ll.add_in_tail(Node(v))
    return ll


def to_array(ll: LinkedList2):
    result = []
    node = ll.head
    while node is not None:
        result.append(node.value)
        node = node.next
    return result


def to_array_reversed(ll: LinkedList2):
    result = []
    node = ll.tail
    while node is not None:
        result.append(node.value)
        node = node.prev
    return result


def assert_order(testcase: unittest.TestCase, ll: LinkedList2):
    if ll.head is None:
        testcase.assertIsNone(ll.tail)
        return

    testcase.assertIsNone(ll.head.prev)
    testcase.assertIsNone(ll.tail.next)

    natural_order = []
    node = ll.head
    prev = None
    while node is not None:
        natural_order.append(node.value)
        testcase.assertIs(node.prev, prev)
        if node.next is not None:
            testcase.assertIs(node.next.prev, node)
        prev = node
        node = node.next

    reversed_order = []
    node = ll.tail
    nxt = None
    while node is not None:
        reversed_order.append(node.value)
        testcase.assertIs(node.next, nxt)
        if node.prev is not None:
            testcase.assertIs(node.prev.next, node)
        nxt = node
        node = node.prev

    testcase.assertEqual(reversed_order, list(reversed(natural_order)))

