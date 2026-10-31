# 5.1. Строим BST

# Рефлексия

# Отсортированный массив идеально подходит для того, чтобы создать дерево "правильной формы". Для этого на каждом шаге
# рекурсивного алгоритма мы устанавливаем очередной центральный узел и "отрезаем" от исходного отсортированного массива
# по два его поддерева. В итоге в результирующий массив значения расположены последовательно по уровням, что и требует
# представление BST в виде массива.

# O(N log N) / O(N)
def GenerateBBSTArray(a: list[int]) -> list[int]:
    sortedValues: list[int] = sorted(a)
    result: list[int] = [0] * len(sortedValues)
    BuildArrayRecursive(sortedValues, result, 0, len(sortedValues), 0)
    return result


def BuildArrayRecursive(sortedValues: list[int], result: list[int | None], left: int, right: int, index: int) -> None:
    if left >= right:
        return

    middle = (left + right) // 2
    result[index] = sortedValues[middle]

    BuildArrayRecursive(sortedValues, result, left, middle, 2 * index + 1)
    BuildArrayRecursive(sortedValues, result, middle + 1, right, 2 * index + 2)