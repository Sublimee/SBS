import unittest
from linked_list import build_linked_list, to_array, LinkedList, Node, sum_linked_lists

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

    # удалить единственный подходящий элемент в списке длиной 2, идущий первым
    def test_3(self):
        ll = build_linked_list([42, 43])
        ll.delete(42)
        self.assertEqual(ll.head.value, 43)
        self.assertEqual(ll.tail.value, 43)
        self.assertEqual(to_array(ll), [43])

    # удалить единственный подходящий элемент в списке длиной 2, идущий последним
    def test_4(self):
        ll = build_linked_list([42, 43])
        ll.delete(43)
        self.assertEqual(ll.head.value, 42)
        self.assertEqual(ll.tail.value, 42)
        self.assertEqual(to_array(ll), [42])

    # удалить один из подходящих элементов в списке длиной 3, идущих первыми
    def test_5(self):
        ll = build_linked_list([42, 42, 43])
        ll.delete(42)
        self.assertEqual(to_array(ll), [42, 43])
        self.assertEqual(ll.head.value, 42)
        self.assertEqual(ll.tail.value, 43)

    # удалить один из подходящих элементов в списке длиной 3, идущих последними
    def test_6(self):
        ll = build_linked_list([42, 43, 43])
        ll.delete(43)
        self.assertEqual(to_array(ll), [42, 43])
        self.assertEqual(ll.head.value, 42)
        self.assertEqual(ll.tail.value, 43)

    # удалить один из подходящих элементов в длинном списке, идущих не первыми и последним
    def test_7(self):
        ll = build_linked_list([1, 2, 3, 2])
        ll.delete(2)
        self.assertEqual(to_array(ll), [1, 3, 2])
        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.tail.value, 2)

    # удалить один из подходящих элементов в длинном списке, идущих первыми
    def test_8(self):
        ll = build_linked_list([2, 2, 3, 4])
        ll.delete(2)
        self.assertEqual(to_array(ll), [2, 3, 4])
        self.assertEqual(ll.head.value, 2)
        self.assertEqual(ll.tail.value, 4)

    # удалить единственный подходящий элемент в длинном списке, идущий первым
    def test_9(self):
        ll = build_linked_list([10, 20, 30])
        ll.delete(10)
        self.assertEqual(to_array(ll), [20, 30])
        self.assertEqual(ll.head.value, 20)
        self.assertEqual(ll.tail.value, 30)

    # удалить единственный подходящий элемент в длинном списке, идущий последним
    def test_10(self):
        ll = build_linked_list([10, 20, 30])
        ll.delete(30)
        self.assertEqual(to_array(ll), [10, 20])
        self.assertEqual(ll.head.value, 10)
        self.assertEqual(ll.tail.value, 20)

    # удалить неподходящий элемент в длинном списке
    def test_11(self):
        ll = build_linked_list([1, 2, 3])
        ll.delete(99)
        self.assertEqual(to_array(ll), [1, 2, 3])
        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.tail.value, 3)

    # удалить все подходящие элементы в длинном списке, идущие не последними/первыми
    def test_12(self):
        ll = build_linked_list([1, 2, 3, 2, 2, 4])
        ll.delete(2, all=True)
        self.assertEqual(to_array(ll), [1, 3, 4])
        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.tail.value, 4)

    # удалить все подходящие элементы в длинном списке, идущие последними/первыми
    def test_13(self):
        ll = build_linked_list([2, 2, 3, 2, 2, 3, 2, 2])
        ll.delete(2, all=True)
        self.assertEqual(to_array(ll), [3, 3])
        self.assertEqual(ll.head.value, 3)
        self.assertEqual(ll.tail.value, 3)

    # удалить все подходящие элементы в длинном списке, идущие первым и не последними
    def test_14(self):
        ll = build_linked_list([2, 3, 2, 3, 2, 3])
        ll.delete(2, all=True)
        self.assertEqual(to_array(ll), [3, 3, 3])
        self.assertEqual(ll.head.value, 3)
        self.assertEqual(ll.tail.value, 3)

    # удалить все подходящие элементы в длинном списке, идущие последними и не первыми
    def test_15(self):
        ll = build_linked_list([3, 2, 3, 2, 3, 2])
        ll.delete(2, all=True)
        self.assertEqual(to_array(ll), [3, 3, 3])
        self.assertEqual(ll.head.value, 3)
        self.assertEqual(ll.tail.value, 3)

    # удалить все подходящие элементы в длинном списке
    def test_16(self):
        ll = build_linked_list([5, 5, 5])
        ll.delete(5, all=True)
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(to_array(ll), [])

class TestClean(unittest.TestCase):

    # очистить непустой список
    def test_1(self):
        ll = build_linked_list([1, 2, 3])
        ll.clean()
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(to_array(ll), [])
        self.assertEqual(ll.len(), 0)

    # очистить список из одного элемента
    def test_2(self):
        ll = build_linked_list([1])
        ll.clean()
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(to_array(ll), [])
        self.assertEqual(ll.len(), 0)


    # очистить список из двух элементов
    def test_3(self):
        ll = build_linked_list([1, 2])
        ll.clean()
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(to_array(ll), [])
        self.assertEqual(ll.len(), 0)

    # очистить пустой список
    def test_4(self):
        ll = LinkedList()
        ll.clean()
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(ll.len(), 0)

class TestFindAll(unittest.TestCase):

    # не должен найти значение в пустом списке
    def test_1(self):
        ll = LinkedList()
        result = ll.find_all(10)
        self.assertEqual(result, [])

    # не должен найти значение в непустом списке
    def test_2(self):
        ll = build_linked_list([1, 2, 3])
        result = ll.find_all(99)
        self.assertEqual(result, [])

    # должен найти все значения в непустом списке
    def test_4(self):
        ll = build_linked_list([2, 2])
        result = ll.find_all(2)
        self.assertEqual(len(result), 2)
        self.assertIs(result[0], ll.head)
        self.assertIs(result[1], ll.tail)

    # должен найти значения в непустом списке
    def test_3(self):
        ll = build_linked_list([1, 2, 3, 2, 4, 2])
        result = ll.find_all(2)
        self.assertEqual(len(result), 3)
        self.assertIs(result[0], ll.head.next)
        self.assertIs(result[1], ll.head.next.next.next)
        self.assertIs(result[2], ll.tail)

class TestLen(unittest.TestCase):

    # получить длину пустого списка
    def test_1(self):
        ll = LinkedList()
        self.assertEqual(ll.len(), 0)

    # получить длину непустого списка
    def test_2(self):
        ll = LinkedList()
        ll.add_in_tail(Node(1))
        ll.add_in_tail(Node(2))
        ll.add_in_tail(Node(3))
        self.assertEqual(ll.len(), 3)

    # получить длину списка после удаления элементов
    def test_3(self):
        ll = build_linked_list([1, 2, 3, 2])
        self.assertEqual(ll.len(), 4)
        ll.delete(2)
        self.assertEqual(ll.len(), 3)
        ll.delete(2, all=True)
        self.assertEqual(ll.len(), 2)

class TestInsert(unittest.TestCase):

    # вставить в пустой список, когда afterNode = None
    def test_1(self):
        ll = LinkedList()
        new_node = Node(10)
        ll.insert(None, new_node)
        self.assertEqual(to_array(ll), [10])
        self.assertIs(ll.head, new_node)
        self.assertIs(ll.tail, new_node)

    # вставить в непустой список, когда afterNode = None
    def test_2(self):
        ll = build_linked_list([1, 2, 3])
        new_node = Node(99)
        ll.insert(None, new_node)
        self.assertEqual(to_array(ll), [99, 1, 2, 3])
        self.assertIs(ll.head, new_node)
        self.assertEqual(ll.tail.value, 3)

    # вставить в непустой список, когда задан существующий нехвостовой afterNode
    def test_3(self):
        ll = build_linked_list([1, 2, 3, 4])
        after = ll.find(2)
        new_node = Node(99)
        ll.insert(after, new_node)
        self.assertEqual(to_array(ll), [1, 2, 99, 3, 4])

    # вставить в непустой список, когда задан существующий хвостовой afterNode
    def test_4(self):
        ll = build_linked_list([1, 2, 3])
        after = ll.tail
        new_node = Node(99)
        ll.insert(after, new_node)
        self.assertEqual(to_array(ll), [1, 2, 3, 99])
        self.assertIs(ll.tail, new_node)

    # вставить в непустой список, когда задан несуществующий afterNode
    def test_5(self):
        ll = build_linked_list([1, 2, 3])
        foreign_node = Node(777)
        new_node = Node(99)
        ll.insert(foreign_node, new_node)
        self.assertEqual(to_array(ll), [1, 2, 3])
        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.tail.value, 3)

class TestSumLinkedLists(unittest.TestCase):

    # должен просуммировать два листа одинаковой длины 6
    def test_1(self):
        list1 = build_linked_list([1, 2, 3, 0, -2, 5])
        list2 = build_linked_list([4, 5, 6, 3, 2, -5])

        result = sum_linked_lists(list1, list2)

        self.assertIsInstance(result, LinkedList)
        self.assertEqual(to_array(result), [5, 7, 9, 3, 0, 0])

    # должен просуммировать два листа одинаковой длины 1
    def test_2(self):
        list1 = build_linked_list([10])
        list2 = build_linked_list([-3])

        result = sum_linked_lists(list1, list2)

        self.assertEqual(to_array(result), [7])

    # должен просуммировать два пустых лста
    def test_4(self):
        list1 = build_linked_list([])
        list2 = build_linked_list([])

        result = sum_linked_lists(list1, list2)

        self.assertIsInstance(result, LinkedList)
        self.assertIsNone(result.head)
        self.assertIsNone(result.tail)
        self.assertEqual(to_array(result), [])

    # не должен просуммировать два листа, где первый лист длиннее
    def test_5(self):
        list1 = build_linked_list([1, 2, 3])
        list2 = build_linked_list([4, 5])

        result = sum_linked_lists(list1, list2)

        self.assertIsNone(result)

    # не должен просуммировать два листа, где второй лист длиннее первого
    def test_6(self):
        list1 = build_linked_list([1, 2])
        list2 = build_linked_list([4, 5, 6])

        result = sum_linked_lists(list1, list2)

        self.assertIsNone(result)