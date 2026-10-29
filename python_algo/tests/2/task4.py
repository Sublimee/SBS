class BSTBasedOnArray:

    def __init__(self, depth: int):
        nodesCount: int = 2 ** (depth + 1) - 1
        self.Tree: list[int | None] = [None] * nodesCount

    # Рефлексия
    # Пробегаемся по индексам для того, чтобы найти ячейку со значением key. Значения укладываются последовательно
    # уровнями. Для перехода на следующий уровень вычисляем индекс левого или правого потомка в зависимости от
    # выполнения условия if key < self.Tree[index]. Если искомое значение найдено, то возвращаем индекс, где хранится
    # key. Иначе, если встретился None, то возвращаем для пустого корня 0, либо отрицательный индекс, чтобы различить
    # это со случаем, когда значение найдено. Если путь пройден и на нём не нашлось ни пустой ячейки, ни искомого
    # значения, то возвращаем None.

    # O(log N) / O(1)
    def FindKeyIndex(self, key: int) -> int | None:
        index = 0
        while index < len(self.Tree):
            if self.Tree[index] is None:
                return -index

            if self.Tree[index] == key:
                return index

            if key < self.Tree[index]:
                index = 2 * index + 1
            else:
                index = 2 * index + 2

        return None

    # Рефлексия
    # Ищем искомое значение с помощью FindKeyIndex. Если индекс положительный, то значение найдено и вставка не
    # требуется. Возвращаем индекс элемента key. Если index == None, то возвращаем -1, чтобы показать невозможность
    # вставки. Если index отрицательный, либо 0 и значения в корне нет, то устанавливаем туда key.

    # O(log N) / O(1)
    def AddKey(self, key: int) -> int:
        index = self.FindKeyIndex(key)
        if index is None:
            return -1

        if index <= 0 and self.Tree[-index] is None:
            index = -index
            self.Tree[index] = key

        return index
