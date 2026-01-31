class Node:
    def __init__(self, v):
        self.value = v
        self.prev = None
        self.next = None


class OrderedList:
    def __init__(self, asc):
        self.head = None
        self.tail = None
        self.__ascending = asc
        self.count = 0

    def is_ascending(self):
        return self.__ascending

    def compare(self, v1, v2):
        if v1 < v2:
            result = -1
        elif v1 == v2:
            result = 0
        else:
            result = 1
        return result


    def add(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.count += 1
            return


        current = self.head

        if self.__ascending:
            direction = -1
        else:
            direction = 1

        while current is not None and self.compare(current.value, value) == direction:
            current = current.next

        if current is None:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        elif current.prev is None:
            new_node.next = current
            current.prev = new_node
            self.head = new_node
        else:
            new_node.next = current
            new_node.prev = current.prev
            new_node.next.prev = new_node
            new_node.prev.next = new_node

        self.count += 1


    def find(self, val):
        if self.__ascending:
            direction = -1
        else:
            direction = 1

        current = self.head
        while current is not None:
            if current.value == val or self.compare(val, current.value) == direction:
                break
            current = current.next

        if current and current.value == val:
            return current
        return None

    def delete(self, val):
        to_delete = self.find(val)
        if to_delete is None:
            return

        next_node = to_delete.next
        prev_node = to_delete.prev

        if prev_node is None:
            self.head = next_node
        else:
            prev_node.next = next_node

        if next_node is None:
            self.tail = prev_node
        else:
            next_node.prev = prev_node

        self.count -= 1

    def clean(self, asc):
        self.head = None
        self.tail = None
        self.count = 0
        self.__ascending = asc

    def len(self):
        return self.count

    def get_all(self):
        r = []
        node = self.head
        while node is not None:
            r.append(node)
            node = node.next
        return r

    # 8 *. Метод удаления всех дубликатов из упорядоченного списка.

    # Рефлексия:
    # Метод делаем внутри класса, чтобы эффективно проходиться по его элементам и работать с размером. Сравниваем
    # текущий и следующий элементы. Если их значения совпали, то переопределяем ссылки текущего и следующего за
    # удаленным элемента (если он есть).

    def deduplicate(self):
        current = self.head
        while current and current.next:
            if current.value != current.next.value:
                current = current.next
                continue

            duplicate = current.next
            current.next = duplicate.next

            if duplicate.next:
                duplicate.next.prev = current
            else:
                self.tail = current

            self.count -= 1


class OrderedStringList(OrderedList):
    def __init__(self, asc):
        super(OrderedStringList, self).__init__(asc)

    def compare(self, v1, v2):
        v1_normalized = v1.strip()
        v2_normalized = v2.strip()
        if v1_normalized < v2_normalized:
            result = -1
        elif v1_normalized == v2_normalized:
            result = 0
        else:
            result = 1
        return result