import unittest

from task4 import Stack
from task4_2 import MinStack
from task4_2 import AvgStack
from task4_2 import Stack2
from task4_2 import validate, validate2, process


def make_stack(n: int):
    a = Stack()
    for i in range(n):
        a.push(i)
    return a


def make_stack2(n: int):
    a = Stack2()
    for i in range(n):
        a.push(i)
    return a


def make_min_stack(n: int):
    a = MinStack()
    for i in range(n):
        a.push(i)
    return a

def make_avg_stack(n: int):
    a = AvgStack()
    for i in range(n):
        a.push(i)
    return a

class TestStackSize(unittest.TestCase):

    def test_1(self):
        a = Stack()
        self.assertEqual(a.size(), 0)

    def test_2(self):
        a = make_stack(10)
        self.assertEqual(a.size(), 10)

    def test_3(self):
        a = Stack()
        a.push(1)
        a.push(1)
        a.push(1)
        self.assertEqual(a.size(), 3)

    def test_4(self):
        a = Stack()
        a.push(1)
        a.push(1)
        a.push(1)
        a.pop()
        a.pop()
        a.pop()
        self.assertEqual(a.size(), 0)

    def test_5(self):
        a = Stack()
        a.push(1)
        a.push(2)
        a.push(3)
        a.pop()
        a.pop()
        self.assertEqual(a.size(), 1)

    def test_6(self):
        a = Stack()
        a.pop()
        a.pop()
        self.assertEqual(a.size(), 0)


class TestStackPopPush(unittest.TestCase):

    def test_1(self):
        a = Stack()
        self.assertEqual(a.pop(), None)

    def test_2(self):
        a = Stack()
        self.assertEqual(a.pop(), None)
        self.assertEqual(a.pop(), None)

    def test_3(self):
        a = Stack()
        a.push(1)
        self.assertEqual(a.pop(), 1)

    def test_4(self):
        a = Stack()
        self.assertEqual(a.pop(), None)
        a.push(2)
        a.push(1)
        self.assertEqual(a.pop(), 1)
        self.assertEqual(a.pop(), 2)
        self.assertEqual(a.pop(), None)


class TestStackPeek(unittest.TestCase):

    def test_1(self):
        a = make_stack(10)
        self.assertEqual(a.peek(), 9)
        self.assertEqual(a.peek(), 9)

    def test_2(self):
        a = Stack()
        self.assertEqual(a.peek(), None)
        self.assertEqual(a.peek(), None)

    def test_3(self):
        a = Stack()
        self.assertEqual(a.pop(), None)
        self.assertEqual(a.peek(), None)
        a.push(2)
        a.push(1)
        self.assertEqual(a.peek(), 1)
        self.assertEqual(a.pop(), 1)
        self.assertEqual(a.peek(), 2)
        self.assertEqual(a.pop(), 2)
        self.assertEqual(a.peek(), None)
        self.assertEqual(a.pop(), None)


class TestStackSize2(unittest.TestCase):

    def test_1(self):
        a = Stack2()
        self.assertEqual(a.size(), 0)

    def test_2(self):
        a = make_stack2(10)
        self.assertEqual(a.size(), 10)

    def test_3(self):
        a = Stack2()
        a.push(1)
        a.push(1)
        a.push(1)
        self.assertEqual(a.size(), 3)

    def test_4(self):
        a = Stack2()
        a.push(1)
        a.push(1)
        a.push(1)
        a.pop()
        a.pop()
        a.pop()
        self.assertEqual(a.size(), 0)

    def test_5(self):
        a = Stack2()
        a.push(1)
        a.push(2)
        a.push(3)
        a.pop()
        a.pop()
        self.assertEqual(a.size(), 1)

    def test_6(self):
        a = Stack2()
        a.pop()
        a.pop()
        self.assertEqual(a.size(), 0)


class TestStackPopPush2(unittest.TestCase):

    def test_1(self):
        a = Stack2()
        self.assertEqual(a.pop(), None)

    def test_2(self):
        a = Stack2()
        self.assertEqual(a.pop(), None)
        self.assertEqual(a.pop(), None)

    def test_3(self):
        a = Stack2()
        a.push(1)
        self.assertEqual(a.pop(), 1)

    def test_4(self):
        a = Stack2()
        self.assertEqual(a.pop(), None)
        a.push(2)
        a.push(1)
        self.assertEqual(a.pop(), 1)
        self.assertEqual(a.pop(), 2)
        self.assertEqual(a.pop(), None)


class TestStackPeek2(unittest.TestCase):

    def test_1(self):
        a = make_stack2(10)
        self.assertEqual(a.peek(), 9)
        self.assertEqual(a.peek(), 9)

    def test_2(self):
        a = Stack2()
        self.assertEqual(a.peek(), None)
        self.assertEqual(a.peek(), None)

    def test_3(self):
        a = Stack2()
        self.assertEqual(a.pop(), None)
        self.assertEqual(a.peek(), None)
        a.push(2)
        a.push(1)
        self.assertEqual(a.peek(), 1)
        self.assertEqual(a.pop(), 1)
        self.assertEqual(a.peek(), 2)
        self.assertEqual(a.pop(), 2)
        self.assertEqual(a.peek(), None)
        self.assertEqual(a.pop(), None)


class TestValidate(unittest.TestCase):

    def test(self):
        self.assertEqual(validate(""), True)
        self.assertEqual(validate("((("), False)
        self.assertEqual(validate("((())"), False)
        self.assertEqual(validate("((()))"), True)
        self.assertEqual(validate("(()"), False)
        self.assertEqual(validate("(()((())()))"), True)
        self.assertEqual(validate("(()()(()"), False)
        self.assertEqual(validate("()"), True)
        self.assertEqual(validate("())"), False)
        self.assertEqual(validate("())("), False)
        self.assertEqual(validate(")"), False)
        self.assertEqual(validate("))(("), False)


class TestValidate2(unittest.TestCase):

    def test(self):
        self.assertEqual(validate2(""), True)
        self.assertEqual(validate2("((("), False)
        self.assertEqual(validate2("((())"), False)
        self.assertEqual(validate2("((()))"), True)
        self.assertEqual(validate2("(()"), False)
        self.assertEqual(validate2("(()((())()))"), True)
        self.assertEqual(validate2("(()()(()"), False)
        self.assertEqual(validate2("()"), True)
        self.assertEqual(validate2("())"), False)
        self.assertEqual(validate2("())("), False)
        self.assertEqual(validate2("()[]{}"), True)
        self.assertEqual(validate2("([)]"), False)
        self.assertEqual(validate2("([]){}"), True)
        self.assertEqual(validate2("(}"), False)
        self.assertEqual(validate2(")"), False)
        self.assertEqual(validate2("))(("), False)
        self.assertEqual(validate2("[]"), True)
        self.assertEqual(validate2("[]]"), False)
        self.assertEqual(validate2("]"), False)
        self.assertEqual(validate2("{[()()]}"), True)
        self.assertEqual(validate2("{[]"), False)
        self.assertEqual(validate2("{[}]"), False)
        self.assertEqual(validate2("{}"), True)
        self.assertEqual(validate2("}"), False)
        self.assertEqual(validate2("}}"), False)


class TestMinStackSize(unittest.TestCase):

    def test_1(self):
        a = MinStack()
        self.assertEqual(a.size(), 0)

    def test_2(self):
        a = make_min_stack(10)
        self.assertEqual(a.size(), 10)

    def test_3(self):
        a = MinStack()
        a.push(1)
        a.push(1)
        a.push(1)
        self.assertEqual(a.size(), 3)

    def test_4(self):
        a = MinStack()
        a.push(1)
        a.push(1)
        a.push(1)
        a.pop()
        a.pop()
        a.pop()
        self.assertEqual(a.size(), 0)

    def test_5(self):
        a = MinStack()
        a.push(1)
        a.push(2)
        a.push(3)
        a.pop()
        a.pop()
        self.assertEqual(a.size(), 1)

    def test_6(self):
        a = MinStack()
        a.pop()
        a.pop()
        self.assertEqual(a.size(), 0)


class TestMinStackPopPush(unittest.TestCase):

    def test_1(self):
        a = MinStack()
        self.assertEqual(a.pop(), None)

    def test_2(self):
        a = MinStack()
        self.assertEqual(a.pop(), None)
        self.assertEqual(a.pop(), None)

    def test_3(self):
        a = MinStack()
        a.push(1)
        self.assertEqual(a.pop(), 1)

    def test_4(self):
        a = Stack2()
        self.assertEqual(a.pop(), None)
        a.push(2)
        a.push(1)
        self.assertEqual(a.pop(), 1)
        self.assertEqual(a.pop(), 2)
        self.assertEqual(a.pop(), None)


class TestMinStackPeek(unittest.TestCase):

    def test_1(self):
        a = make_min_stack(10)
        self.assertEqual(a.peek(), 9)
        self.assertEqual(a.peek(), 9)

    def test_2(self):
        a = MinStack()
        self.assertEqual(a.peek(), None)
        self.assertEqual(a.peek(), None)

    def test_3(self):
        a = MinStack()
        self.assertEqual(a.pop(), None)
        self.assertEqual(a.peek(), None)
        a.push(2)
        a.push(1)
        self.assertEqual(a.peek(), 1)
        self.assertEqual(a.pop(), 1)
        self.assertEqual(a.peek(), 2)
        self.assertEqual(a.pop(), 2)
        self.assertEqual(a.peek(), None)
        self.assertEqual(a.pop(), None)


class TestMinStackMin(unittest.TestCase):

    def test_1(self):
        a = MinStack()
        self.assertEqual(a.min(), None)

    def test_2(self):
        a = make_min_stack(10)
        self.assertEqual(a.min(), 0)
        a.pop()
        self.assertEqual(a.min(), 0)

    def test_3(self):
        a = MinStack()
        a.push(2)
        self.assertEqual(a.min(), 2)
        a.push(1)
        self.assertEqual(a.min(), 1)
        a.pop()
        self.assertEqual(a.min(), 2)
        a.pop()
        self.assertEqual(a.min(), None)

    def test_4(self):
        a = MinStack()
        a.push(2)
        self.assertEqual(a.min(), 2)
        a.push(0)
        self.assertEqual(a.min(), 0)
        a.push(1)
        self.assertEqual(a.min(), 0)
        a.push(2)
        self.assertEqual(a.min(), 0)
        a.pop()
        self.assertEqual(a.min(), 0)
        a.pop()
        self.assertEqual(a.min(), 0)
        a.pop()
        self.assertEqual(a.min(), 2)

class TestAvgStackSize(unittest.TestCase):

    def test_1(self):
        a = AvgStack()
        self.assertEqual(a.size(), 0)

    def test_2(self):
        a = make_avg_stack(10)
        self.assertEqual(a.size(), 10)

    def test_3(self):
        a = AvgStack()
        a.push(1)
        a.push(1)
        a.push(1)
        self.assertEqual(a.size(), 3)

    def test_4(self):
        a = AvgStack()
        a.push(1)
        a.push(1)
        a.push(1)
        a.pop()
        a.pop()
        a.pop()
        self.assertEqual(a.size(), 0)

    def test_5(self):
        a = AvgStack()
        a.push(1)
        a.push(2)
        a.push(3)
        a.pop()
        a.pop()
        self.assertEqual(a.size(), 1)

    def test_6(self):
        a = AvgStack()
        a.pop()
        a.pop()
        self.assertEqual(a.size(), 0)


class TestAvgStackPopPush(unittest.TestCase):

    def test_1(self):
        a = AvgStack()
        self.assertEqual(a.pop(), None)

    def test_2(self):
        a = AvgStack()
        self.assertEqual(a.pop(), None)
        self.assertEqual(a.pop(), None)

    def test_3(self):
        a = AvgStack()
        a.push(1)
        self.assertEqual(a.pop(), 1)

    def test_4(self):
        a = AvgStack()
        self.assertEqual(a.pop(), None)
        a.push(2)
        a.push(1)
        self.assertEqual(a.pop(), 1)
        self.assertEqual(a.pop(), 2)
        self.assertEqual(a.pop(), None)


class TestAvgStackPeek(unittest.TestCase):

    def test_1(self):
        a = make_avg_stack(10)
        self.assertEqual(a.peek(), 9)
        self.assertEqual(a.peek(), 9)

    def test_2(self):
        a = AvgStack()
        self.assertEqual(a.peek(), None)
        self.assertEqual(a.peek(), None)

    def test_3(self):
        a = AvgStack()
        self.assertEqual(a.pop(), None)
        self.assertEqual(a.peek(), None)
        a.push(2)
        a.push(1)
        self.assertEqual(a.peek(), 1)
        self.assertEqual(a.pop(), 1)
        self.assertEqual(a.peek(), 2)
        self.assertEqual(a.pop(), 2)
        self.assertEqual(a.peek(), None)
        self.assertEqual(a.pop(), None)

class TestAvgStackAvg(unittest.TestCase):

    def test_1(self):
        a = AvgStack()
        self.assertEqual(a.avg(), None)

    def test_2(self):
        a = make_avg_stack(10)
        self.assertEqual(a.avg(), 4.5)

    def test_3(self):
        a = AvgStack()
        a.push(2)
        self.assertEqual(a.avg(), 2)
        a.push(4)
        self.assertEqual(a.avg(), 3)
        a.pop()
        self.assertEqual(a.avg(), 2)
        a.pop()
        self.assertEqual(a.avg(), None)

class TestProcess(unittest.TestCase):

    def test(self):
        self.assertEqual(process("8 2 + 5 * 9 + ="), 59)