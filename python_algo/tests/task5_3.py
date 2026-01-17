import unittest

from task5 import Queue
from task5_2 import Queue2, Queue3, Queue4


def make_queue(n: int):
    q = Queue()
    for i in range(n):
        q.enqueue(i)
    return q


def make_queue2(n: int):
    q = Queue2()
    for i in range(n):
        q.enqueue(i)
    return q


def make_queue3(n: int):
    q = Queue3()
    for i in range(n):
        q.enqueue(i)
    return q


def make_queue4(n: int):
    q = Queue4(n)
    for i in range(n):
        q.enqueue(i)
    return q


class TestQueueSize(unittest.TestCase):

    def test_1(self):
        q = Queue()
        self.assertEqual(q.size(), 0)

    def test_2(self):
        q = make_queue(10)
        self.assertEqual(q.size(), 10)

    def test_3(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(1)
        q.enqueue(1)
        self.assertEqual(q.size(), 3)

    def test_4(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(1)
        q.enqueue(1)
        q.dequeue()
        q.dequeue()
        q.dequeue()
        self.assertEqual(q.size(), 0)

    def test_5(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        q.dequeue()
        q.dequeue()
        self.assertEqual(q.size(), 1)

    def test_6(self):
        q = Queue()
        q.dequeue()
        q.dequeue()
        self.assertEqual(q.size(), 0)


class TestQueueEnqueueDequeue(unittest.TestCase):

    def test_1(self):
        q = Queue()
        self.assertEqual(q.dequeue(), None)

    def test_2(self):
        q = Queue()
        self.assertEqual(q.dequeue(), None)
        self.assertEqual(q.dequeue(), None)

    def test_3(self):
        q = Queue()
        q.enqueue(1)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), None)

    def test_4(self):
        q = Queue()
        self.assertEqual(q.dequeue(), None)
        q.enqueue(2)
        q.enqueue(1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), None)


class TestQueue2Rotate(unittest.TestCase):

    def test_1(self):
        q = Queue2()
        q.rotate(1)
        self.assertEqual(q.dequeue(), None)

    def test_2(self):
        q = make_queue2(1)
        q.rotate(1)
        self.assertEqual(q.dequeue(), 0)
        self.assertEqual(q.dequeue(), None)

    def test_3(self):
        q = make_queue2(2)
        q.rotate(1)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 0)
        self.assertEqual(q.dequeue(), None)

    def test_4(self):
        q = make_queue2(3)
        q.rotate(1)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 0)
        self.assertEqual(q.dequeue(), None)

    def test_5(self):
        q = make_queue2(3)
        q.rotate(3)
        self.assertEqual(q.dequeue(), 0)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), None)


class TestQueue3Size(unittest.TestCase):

    def test_1(self):
        q = Queue3()
        self.assertEqual(q.size(), 0)

    def test_2(self):
        q = make_queue3(10)
        self.assertEqual(q.size(), 10)

    def test_3(self):
        q = Queue3()
        q.enqueue(1)
        q.enqueue(1)
        q.enqueue(1)
        self.assertEqual(q.size(), 3)

    def test_4(self):
        q = Queue3()
        q.enqueue(1)
        q.enqueue(1)
        q.enqueue(1)
        q.dequeue()
        q.dequeue()
        q.dequeue()
        self.assertEqual(q.size(), 0)

    def test_5(self):
        q = Queue3()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        q.dequeue()
        q.dequeue()
        self.assertEqual(q.size(), 1)

    def test_6(self):
        q = Queue3()
        q.dequeue()
        q.dequeue()
        self.assertEqual(q.size(), 0)


class TestQueue3EnqueueDequeue(unittest.TestCase):

    def test_1(self):
        q = Queue3()
        self.assertEqual(q.dequeue(), None)

    def test_2(self):
        q = Queue3()
        self.assertEqual(q.dequeue(), None)
        self.assertEqual(q.dequeue(), None)

    def test_3(self):
        q = Queue3()
        q.enqueue(1)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), None)

    def test_4(self):
        q = Queue3()
        self.assertEqual(q.dequeue(), None)
        q.enqueue(2)
        q.enqueue(1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), None)


class TestQueue3Reverse(unittest.TestCase):

    def test_1(self):
        q = Queue3()
        self.assertEqual(q.dequeue(), None)
        self.assertEqual(q.dequeue(), None)

    def test_2(self):
        q = Queue3()
        q.enqueue(1)
        q.reverse()
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), None)

    def test_3(self):
        q = Queue3()
        self.assertEqual(q.dequeue(), None)
        q.enqueue(2)
        q.enqueue(1)
        q.reverse()
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), None)

    def test_4(self):
        q = Queue3()
        self.assertEqual(q.dequeue(), None)
        q.enqueue(3)
        q.enqueue(2)
        q.enqueue(1)
        q.reverse()
        q.reverse()
        self.assertEqual(q.dequeue(), 3)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), None)

    def test_5(self):
        q = Queue3()
        self.assertEqual(q.dequeue(), None)
        q.enqueue(3)
        q.enqueue(2)
        q.enqueue(1)
        q.reverse()
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)
        self.assertEqual(q.dequeue(), None)


class TestQueue4Size(unittest.TestCase):

    def test_1(self):
        q = Queue4(3)
        self.assertEqual(q.size(), 0)

    def test_2(self):
        q = make_queue4(3)
        self.assertEqual(q.size(), 3)

    def test_3(self):
        q = Queue4(3)
        q.enqueue(1)
        q.enqueue(1)
        q.enqueue(1)
        self.assertEqual(q.size(), 3)

    def test_4(self):
        q = Queue4(3)
        q.enqueue(1)
        q.enqueue(1)
        q.enqueue(1)
        q.dequeue()
        q.dequeue()
        q.dequeue()
        self.assertEqual(q.size(), 0)

    def test_5(self):
        q = Queue4(3)
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        q.dequeue()
        q.dequeue()
        self.assertEqual(q.size(), 1)

    def test_6(self):
        q = Queue4(5)
        q.dequeue()
        q.dequeue()
        self.assertEqual(q.size(), 0)

    def test_7(self):
        q = Queue4(2)
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual(q.size(), 2)

    def test_8(self):
        q = Queue4(2)
        q.enqueue(1)
        q.enqueue(2)
        q.dequeue()
        self.assertEqual(q.size(), 1)

class TestQueue4EnqueueDequeue(unittest.TestCase):

    def test_1(self):
        q = Queue4(1)
        self.assertEqual(q.dequeue(), None)

    def test_2(self):
        q = Queue4(1)
        self.assertEqual(q.dequeue(), None)
        self.assertEqual(q.dequeue(), None)

    def test_3(self):
        q = Queue4(1)
        q.enqueue(1)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), None)

    def test_4(self):
        q = Queue4(2)
        self.assertEqual(q.dequeue(), None)
        q.enqueue(2)
        q.enqueue(1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), None)

    def test_5(self):
        q = Queue4(3)
        self.assertEqual(q.dequeue(), None)
        q.enqueue(3)
        q.enqueue(2)
        q.enqueue(1)
        self.assertEqual(q.dequeue(), 3)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), None)
        q.enqueue(3)
        q.enqueue(2)
        q.enqueue(1)
        self.assertEqual(q.dequeue(), 3)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), None)

    def test_6(self):
        q = Queue4(3)
        self.assertEqual(q.dequeue(), None)
        q.enqueue(3)
        q.enqueue(2)
        q.enqueue(1)
        self.assertEqual(q.dequeue(), 3)
        self.assertEqual(q.dequeue(), 2)
        q.enqueue(4)
        q.enqueue(5)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 4)
        q.enqueue(6)
        q.enqueue(7)
        self.assertEqual(q.dequeue(), 5)
        self.assertEqual(q.dequeue(), 6)
        self.assertEqual(q.dequeue(), 7)
        self.assertEqual(q.dequeue(), None)

