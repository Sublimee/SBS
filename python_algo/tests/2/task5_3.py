import unittest

from task5 import GenerateBBSTArray
from task5_2 import DeleteFromBBSTArray


class TestGenerateBBSTArray(unittest.TestCase):

    def test_1(self) -> None:
        result = GenerateBBSTArray([])

        self.assertEqual(result, [])

    def test_2(self) -> None:
        result = GenerateBBSTArray([5])

        self.assertEqual(result, [5])

    def test_3(self) -> None:
        result = GenerateBBSTArray([1, 2, 3])

        self.assertEqual(result, [2, 1, 3])

    def test_4(self) -> None:
        result = GenerateBBSTArray([3, 1, 2])

        self.assertEqual(result, [2, 1, 3])

    def test_5(self) -> None:
        result = GenerateBBSTArray([1, 2, 3, 4, 5, 6, 7])

        self.assertEqual(result, [4, 2, 6, 1, 3, 5, 7])

    def test_6(self) -> None:
        result = GenerateBBSTArray([7, 6, 5, 4, 3, 2, 1])

        self.assertEqual(result, [4, 2, 6, 1, 3, 5, 7])

    def test_7(self) -> None:
        result = GenerateBBSTArray([5, 1, 7, 3, 6, 2, 4])

        self.assertEqual(result, [4, 2, 6, 1, 3, 5, 7])

    def test_8(self) -> None:
        result = GenerateBBSTArray([2, -3, 0, 3, -1, 1, -2])

        self.assertEqual(result, [0, -2, 2, -3, -1, 1, 3])

    def test_9(self) -> None:
        result = GenerateBBSTArray([15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])

        self.assertEqual(result, [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15])

    def test_10(self) -> None:
        values = [3, 1, 2]

        result = GenerateBBSTArray(values)

        self.assertEqual(result, [2, 1, 3])
        self.assertEqual(values, [3, 1, 2])


class TestDeleteFromBBSTArray(unittest.TestCase):

    def test_1(self) -> None:
        tree: list[int | None] = []

        result = DeleteFromBBSTArray(tree, 1)

        self.assertEqual(result, [])

    def test_2(self) -> None:
        tree: list[int | None] = [5]

        result = DeleteFromBBSTArray(tree, 5)

        self.assertEqual(result, [None])

    def test_3(self) -> None:
        tree: list[int | None] = [4, 2, 6, 1, 3, 5, 7]

        result = DeleteFromBBSTArray(tree, 8)

        self.assertEqual(result, [4, 2, 6, 1, 3, 5, 7])
        self.assertEqual(tree, [4, 2, 6, 1, 3, 5, 7])

    def test_4(self) -> None:
        tree: list[int | None] = [4, 2, 6, 1, 3, 5, 7]

        result = DeleteFromBBSTArray(tree, 4)

        self.assertEqual(result, [5, 2, 7, 1, 3, 6, None])

    def test_5(self) -> None:
        tree: list[int | None] = [4, 2, 6, 1, 3, 5, 7]

        result = DeleteFromBBSTArray(tree, 1)

        self.assertEqual(result, [5, 3, 7, 2, 4, 6, None])

    def test_6(self) -> None:
        tree: list[int | None] = [4, 2, 6, 1, 3, 5, 7]

        result = DeleteFromBBSTArray(tree, 7)

        self.assertEqual(result, [4, 2, 6, 1, 3, 5, None])

    def test_7(self) -> None:
        tree: list[int | None] = [4, 2, 6, 1, 3, 5, 7]

        result = DeleteFromBBSTArray(tree, 2)

        self.assertEqual(result, [5, 3, 7, 1, 4, 6, None])

    def test_8(self) -> None:
        tree: list[int | None] = [3, 2, 4, 1, None, None, None]

        result = DeleteFromBBSTArray(tree, 2)

        self.assertEqual(result, [3, 1, 4, None, None, None, None])

    def test_9(self) -> None:
        tree: list[int | None] = [0, -2, 2, -3, -1, 1, 3]

        result = DeleteFromBBSTArray(tree, 0)

        self.assertEqual(result, [1, -2, 3, -3, -1, 2, None])

    def test_10(self) -> None:
        tree: list[int | None] = [2, 1, 3]

        tree = DeleteFromBBSTArray(tree, 2)
        self.assertEqual(tree, [3, 1, None])
        tree = DeleteFromBBSTArray(tree, 3)
        self.assertEqual(tree, [1, None, None])
        tree = DeleteFromBBSTArray(tree, 1)
        self.assertEqual(tree, [None, None, None])
        self.assertEqual(DeleteFromBBSTArray(tree, 1), [None, None, None])

    def test_11(self) -> None:
        tree: list[int | None] = [4, 2, 6, 1, 3, 5, 7]

        tree = DeleteFromBBSTArray(tree, 7)
        self.assertEqual(tree, [4, 2, 6, 1, 3, 5, None])
        self.assertEqual(DeleteFromBBSTArray(tree, 7), [4, 2, 6, 1, 3, 5, None])

    def test_12(self) -> None:
        tree: list[int | None] = [4, 2, 6, 1, 3, 5, 7]

        result = DeleteFromBBSTArray(tree, 4)

        self.assertIsNot(result, tree)
        self.assertEqual(tree, [4, 2, 6, 1, 3, 5, 7])
        self.assertEqual(result, [5, 2, 7, 1, 3, 6, None])

    def test_13(self) -> None:
        tree: list[int | None] = [4, 2, 6, 1, 3, 5, None]

        tree = DeleteFromBBSTArray(tree, 5)
        self.assertEqual(tree, [3, 2, 6, 1, None, 4, None])
        tree = DeleteFromBBSTArray(tree, 6)
        self.assertEqual(tree, [3, 2, 4, 1, None, None, None])
