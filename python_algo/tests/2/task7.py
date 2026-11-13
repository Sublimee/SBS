class Heap:

    def __init__(self):
        self.HeapArray: list[int | None] = []
        self.Size: int = 0

    # 7.1. Строим бинарную пирамиду

    # Рефлексия

    # Так как ограничений на порядок элементов входящего массива нет, то восстановим "правильный" порядок элементов,
    # если вдруг пришёл "неупорядоченный" массив.
    #
    # Сначала посмотрел своё решение на Java и подумал, что я просто копировал элементы входящего массива. Но потом
    # увидел, что использовал Add для построения кучи. Ловко! В этот раз попробуем сделать то же с помощью просеивания
    # сразу.
    #
    # Находим в массиве последний узел с потомками (делаем это арифметически аналогично тому, как делали это в прошлых
    # заданиях). У него находим большего из потомков. Если он не больше родителя, то переходим к следующему
    # арифметически вычисленному узлу того же уровня или "поднимаемся" выше. Иначе -- меняем узлы местами и проделываем
    # ту же операцию с переехавшим узлом.
    #
    # Отказ от рекурсии позволяет сэкономить память, так как не приходится "помнить" стек вызовов, а также работать с
    # более глубокими деревьями.

    # O(N) / O(N)
    def MakeHeap(self, a: list[int], depth: int) -> None:
        heapSize = 2 ** (depth + 1) - 1

        self.HeapArray = [None] * heapSize
        self.Size = len(a)
        for index, key in enumerate(a):
            self.HeapArray[index] = key

        for index in range(self.Size // 2 - 1, -1, -1):
            self.Reorder(index)

    def Reorder(self, parentIndex: int) -> None:
        while 2 * parentIndex + 1 < self.Size:
            leftIndex = 2 * parentIndex + 1
            rightIndex = 2 * parentIndex + 2

            maxIndex = leftIndex
            if rightIndex < self.Size and self.HeapArray[rightIndex] > self.HeapArray[leftIndex]:
                maxIndex = rightIndex

            if self.HeapArray[parentIndex] >= self.HeapArray[maxIndex]:
                return

            self.HeapArray[parentIndex], self.HeapArray[maxIndex] = self.HeapArray[maxIndex], self.HeapArray[
                parentIndex]
            parentIndex = maxIndex

    # 7.2. Удаление максимально приоритетного элемента и вставка нового элемента

    # Рефлексия

    # Удаляем корень, а на его место ставим последний непустой элемент массива. Если брать элемент из середины, то
    # придётся делать лишние телодвижения по восстановлению порядка из-за образовавшейся дырки. Далее выправляем дефекты
    # пирамиды аналогично MakeHeap, только для оптимизации указываем конкретный узел через аргумент Reorder напрямую.

    # O(log N) / O(1)
    def GetMax(self) -> int:
        if self.Size == 0:
            return -1

        result = self.HeapArray[0]
        self.Size -= 1
        self.HeapArray[0] = self.HeapArray[self.Size]
        self.HeapArray[self.Size] = None
        self.Reorder(0)
        return result

    # Рефлексия

    # Добавляем новый ключ в первую свободную ячейку. Зная потенциально дефектный элемент, идём к корню и выполняем
    # действия аналогичные Reorder, пока не упрёмся в правильную комбинацию родителя с потомками.

    # O(log N) / O(1)
    def Add(self, key: int) -> bool:
        if self.Size == len(self.HeapArray):
            return False

        index = self.Size
        self.HeapArray[index] = key
        self.Size += 1

        while index > 0:
            parentIndex = (index - 1) // 2

            if self.HeapArray[parentIndex] >= self.HeapArray[index]:
                break

            self.HeapArray[parentIndex], self.HeapArray[index] = (
                self.HeapArray[index], self.HeapArray[parentIndex]
            )
            index = parentIndex

        return True

    # 7.3. Проверка корректности кучи

    # Рефлексия

    # Если не использовать рекурсию, то у меня получались либо вложенные if, либо несколько проходов по массиву, поэтому
    # остановился на таком варианте. В остальном повторяем аналогичную логику обхода pre-order из прошлых заданий.

    # O(N) / O(log N)
    def IsHeap(self) -> bool:
        if self.Size < 0 or self.Size > len(self.HeapArray):
            return False

        for index in range(self.Size, len(self.HeapArray)):
            if self.HeapArray[index] is not None:
                return False

        return self.IsHeapRecursive(0)

    def IsHeapRecursive(self, index: int) -> bool:
        if index >= self.Size:
            return True

        if self.HeapArray[index] is None:
            return False

        if index > 0 and self.HeapArray[(index - 1) // 2] < self.HeapArray[index]:
            return False

        return self.IsHeapRecursive(2 * index + 1) and self.IsHeapRecursive(2 * index + 2)
