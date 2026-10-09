from task7 import OrderedList, Node


# 6. Учитывать упорядоченность в функции поиска

# Сложность операции поиска не изменилась -- O(N), но на практике будет просмотрено меньшее количество элементов,
# если не найден искомый.

# 8 *. Метод удаления всех дубликатов из упорядоченного списка.

# Реализовано в task7.py

# 9.* Напишите алгоритм слияния двух упорядоченных списков в один, сохраняя порядок элементов. Подумайте, как это
# сделать наиболее эффективно.

# Рефлексия:

# Формируем новый лист. На каждой итерации выбираем, чью голову будем использовать для вставки: первого или второго
# списка. append идеоматически некорректен, но используем такую реализацию для вставки без сравнения.
#
# После каждой вставки сдвигаем соответствующий указатель. Как только один из указателей "закончился" --
# переходим к последовательному сдвигу оставшегося указателя.

def merge(first: OrderedList, second: OrderedList):
    def take_from_first(pointer_first, pointer_second):
        cmp = first.compare(pointer_first.value, pointer_second.value)
        return cmp <= 0 if first.is_ascending() else cmp >= 0

    def append(ol: OrderedList, new_value):
        new_node = Node(new_value)

        if not ol.head:
            ol.head = new_node
            ol.tail = new_node
            ol.count += 1
            return

        ol.tail.next = new_node
        new_node.prev = ol.tail
        ol.tail = new_node
        ol.count += 1
        return

    if not first and not second:
        return None

    if not first:
        return second

    if not second:
        return first

    if first.is_ascending() != second.is_ascending():
        return None

    result = OrderedList(first.is_ascending())
    pointer_first = first.head
    pointer_second = second.head

    while pointer_first and pointer_second:
        if take_from_first(pointer_first, pointer_second):
            append(result, pointer_first.value)
            pointer_first = pointer_first.next
        else:
            append(result, pointer_second.value)
            pointer_second = pointer_second.next

    tail = pointer_first if pointer_first else pointer_second
    while tail:
        append(result, tail.value)
        tail = tail.next

    return result


# 10.* Напишите метод проверки наличия заданного упорядоченного под-списка (параметр метода) в текущем списке.

# Рефлексия:

# Сначала сделал такое решение:
# проходимся по каждому элементу основного списка и проверяем, не начинается ли с него последовательность. Если
# указатели совпали по хранимым значениям, то проверяем следующие len(sublist) элементов. Если совпадение не найдено, то
# переходим к следующему элементу основного списка.
#
# Первое решение актуально для неотсортированных списков. Для отсортированных списков ищем первое вхождение головы
# sublist с помощью find. Проверяем подпоследовательность в основном списке до тех пор, пока голова sublist совпадает
# с элементами основного списка (while ol_pointer and ol_pointer.value == sublist.head.value).

def contains_sublist(ol: OrderedList, sublist: OrderedList):

    def contains(main) -> bool:
        out_pointer = main
        in_pointer = sublist.head

        while out_pointer and in_pointer and out_pointer.value == in_pointer.value:
            out_pointer = out_pointer.next
            in_pointer = in_pointer.next

        return in_pointer is None

    if not ol or not sublist or ol.len() == 0 or sublist.len() == 0 or sublist.len() > ol.len() or ol.is_ascending() != sublist.is_ascending():
        return False

    ol_pointer = ol.find(sublist.head.value)

    while ol_pointer and ol_pointer.value == sublist.head.value:
        if contains(ol_pointer):
            return True
        ol_pointer = ol_pointer.next

    return False


# 11.* Добавьте метод, который находит наиболее часто встречающееся значение в списке.

# Рефлексия:

# Обходим каждый элемент по 1 разу, считая длину локальной последовательности одинаковых чисел. Если последовательность
# нарушается, то проверяем, не превышен ли глобальный максимум.

def max_duplicates(ol: OrderedList):
    if not ol or ol.len() == 0:
        return None

    result = 1
    local_max = 1
    current = ol.head
    next = current.next

    while next:
        if current.value == next.value:
            local_max += 1
        else:
            result = max(local_max, result)
            local_max = 1

        current = next
        next = current.next

    return result

# 12.* Добавьте в упорядоченный список возможность найти индекс элемента (параметр) в списке, которая должна работать за
# o(log N).

# Не реализовал.