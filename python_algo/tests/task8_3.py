import unittest

from task8 import HashTable
from task8_2 import HashTable2, HashTableSalted, DoubleHashTable


class TestHashFun(unittest.TestCase):

    def test_1(self):
        ht = HashTable(5, 1)

        self.assertEqual(0, ht.hash_fun(None))

        self.assertEqual(3, ht.hash_fun("0"))
        self.assertEqual(4, ht.hash_fun("1"))
        self.assertEqual(0, ht.hash_fun("2"))
        self.assertEqual(1, ht.hash_fun("3"))
        self.assertEqual(2, ht.hash_fun("4"))

        self.assertEqual(3, ht.hash_fun("5"))
        self.assertEqual(4, ht.hash_fun("6"))
        self.assertEqual(0, ht.hash_fun("7"))
        self.assertEqual(1, ht.hash_fun("8"))
        self.assertEqual(2, ht.hash_fun("9"))

    def test_2(self):
        ht = HashTable(17, 3)

        self.assertEqual(0, ht.hash_fun(None))

        self.assertEqual(15, ht.hash_fun("abc"))
        self.assertEqual(5, ht.hash_fun("Hello"))
        self.assertEqual(11, ht.hash_fun("Привет"))
        self.assertEqual(2, ht.hash_fun("123"))
        self.assertEqual(8, ht.hash_fun("привет мир"))
        self.assertEqual(16, ht.hash_fun("!"))


class TestSeekSlot(unittest.TestCase):

    def test_1(self):
        ht = HashTable(5, 1)

        self.assertEqual(3, ht.seek_slot("0"))
        self.assertEqual(4, ht.seek_slot("1"))
        self.assertEqual(0, ht.seek_slot("2"))
        self.assertEqual(1, ht.seek_slot("3"))
        self.assertEqual(2, ht.seek_slot("4"))

        self.assertEqual(3, ht.hash_fun("5"))
        self.assertEqual(4, ht.hash_fun("6"))
        self.assertEqual(0, ht.hash_fun("7"))
        self.assertEqual(1, ht.hash_fun("8"))
        self.assertEqual(2, ht.hash_fun("9"))

    def test_2(self):
        ht = HashTable(17, 3)
        value = "abc"
        init = ht.hash_fun(value)
        self.assertIsNone(ht.slots[init])
        self.assertEqual(ht.seek_slot(value), init)

    def test_3(self):
        ht = HashTable(17, 3)
        value = "abc"
        slot = ht.put(value)
        self.assertIsNotNone(slot)
        self.assertEqual(ht.seek_slot(value), slot)

    def test_4(self):
        ht = HashTable(17, 3)
        value = "some"
        init = ht.hash_fun(value)
        ht.slots[init] = "other"
        expected = (init + ht.step) % ht.size
        self.assertEqual(ht.seek_slot(value), expected)


class TestPut(unittest.TestCase):

    def test_0(self):
        ht = HashTable(5, 1)

        self.assertEqual(3, ht.put("0"))
        self.assertEqual(4, ht.put("1"))
        self.assertEqual(0, ht.put("2"))
        self.assertEqual(1, ht.put("3"))
        self.assertEqual(2, ht.put("4"))

        self.assertEqual(None, ht.put("5"))
        self.assertEqual(None, ht.put("6"))
        self.assertEqual(None, ht.put("7"))
        self.assertEqual(None, ht.put("8"))
        self.assertEqual(None, ht.put("9"))

    def test_1(self):
        ht = HashTable(5, 1)

        self.assertEqual(3, ht.put("0"))
        self.assertEqual(4, ht.put("5"))
        self.assertEqual(0, ht.put("11"))
        self.assertEqual(1, ht.put("16"))
        self.assertEqual(2, ht.put("20"))
        self.assertEqual(None, ht.put("25"))

    def test_2(self):
        ht = HashTable(17, 3)
        value = "abc"
        slot = ht.put(value)
        self.assertIsNotNone(slot)
        self.assertEqual(ht.slots[slot], value)

    def test_3(self):
        ht = HashTable(17, 3)
        value = "abc"
        slot1 = ht.put(value)
        slot2 = ht.put(value)
        self.assertEqual(slot1, slot2)
        self.assertEqual(ht.slots[slot1], value)


class TestFind(unittest.TestCase):

    def test_1(self):
        ht = HashTable(5, 1)

        self.assertEqual(3, ht.put("0"))
        self.assertEqual(3, ht.find("0"))

        self.assertEqual(4, ht.put("1"))
        self.assertEqual(4, ht.find("1"))
        self.assertEqual(0, ht.put("2"))
        self.assertEqual(0, ht.find("2"))
        self.assertEqual(1, ht.put("3"))
        self.assertEqual(1, ht.find("3"))
        self.assertEqual(2, ht.put("4"))
        self.assertEqual(2, ht.find("4"))

        self.assertEqual(None, ht.put("5"))
        self.assertEqual(None, ht.find("5"))
        self.assertEqual(None, ht.put("6"))
        self.assertEqual(None, ht.find("6"))
        self.assertEqual(None, ht.put("7"))
        self.assertEqual(None, ht.find("7"))
        self.assertEqual(None, ht.put("8"))
        self.assertEqual(None, ht.find("8"))
        self.assertEqual(None, ht.put("9"))
        self.assertEqual(None, ht.find("9"))

    def test_2(self):
        ht = HashTable(5, 2)

        self.assertEqual(3, ht.put("0"))
        self.assertEqual(3, ht.find("0"))

        self.assertEqual(4, ht.put("1"))
        self.assertEqual(4, ht.find("1"))
        self.assertEqual(0, ht.put("2"))
        self.assertEqual(0, ht.find("2"))
        self.assertEqual(1, ht.put("3"))
        self.assertEqual(1, ht.find("3"))
        self.assertEqual(2, ht.put("4"))
        self.assertEqual(2, ht.find("4"))

        self.assertEqual(None, ht.put("5"))
        self.assertEqual(None, ht.find("5"))
        self.assertEqual(None, ht.put("6"))
        self.assertEqual(None, ht.find("6"))
        self.assertEqual(None, ht.put("7"))
        self.assertEqual(None, ht.find("7"))
        self.assertEqual(None, ht.put("8"))
        self.assertEqual(None, ht.find("8"))
        self.assertEqual(None, ht.put("9"))
        self.assertEqual(None, ht.find("9"))

    def test_3(self):
        ht = HashTable(17, 3)
        value = "abc"
        slot = ht.put(value)
        self.assertEqual(ht.find(value), slot)

    def test_4(self):
        ht = HashTable(17, 3)
        self.assertIsNone(ht.find("0"))

    def test_5(self):
        ht = HashTable(7, 3)
        ht.put("0")
        ht.put("1")
        ht.put("2")
        ht.put("3")
        ht.put("4")
        ht.put("5")
        ht.put("6")
        self.assertIsNone(ht.find("7"))

    def test_6(self):
        ht = HashTable(7, 3)

        a = "2"
        b = "19"

        self.assertEqual(ht.hash_fun(a), ht.hash_fun(b))

        sa = ht.put(a)
        sb = ht.put(b)

        self.assertIsNotNone(sa)
        self.assertIsNotNone(sb)
        self.assertNotEqual(sa, sb)

        self.assertEqual(ht.find(a), sa)
        self.assertEqual(ht.find(b), sb)


class TestHashTable2Resize(unittest.TestCase):

    def test_1(self):
        ht = HashTable2(17, 3)
        ht.put("0")
        ht.put("13")
        ht.put("16")
        ht.put("9")
        ht.put("2")
        ht.put("3")
        ht.put("12")
        ht.put("5")
        ht.put("6")
        ht.put("11")
        ht.put("7")
        ht.put("15")
        ht.put("10")
        ht.put("8")
        ht.put("4")
        ht.put("1")
        ht.put("14")

        ht2 = HashTable2(17, 3)

        for x in ht.slots:
            if x is not None:
                ht2.put(x)

        for i in range(len(ht.slots)):
            self.assertEqual(ht.slots[i], ht2.slots[i])
        self.assertEqual(ht.size, ht2.size)
        self.assertEqual(ht.step, ht2.step)
        self.assertEqual(ht.count, ht2.count)

    def test_2(self):
        ht = HashTable2(3, 2)
        ht.put("0")
        ht.put("13")
        ht.put("16")
        ht.put("9")
        ht.put("2")
        ht.put("3")
        ht.put("12")
        ht.put("5")
        ht.put("6")
        ht.put("11")
        ht.put("7")
        ht.put("15")
        ht.put("10")
        ht.put("8")
        ht.put("4")
        ht.put("1")
        ht.put("14")

        ht2 = HashTable2(24, 3)

        for x in ht.slots:
            if x is not None:
                ht2.put(x)

        for i in range(len(ht.slots)):
            self.assertEqual(ht.slots[i], ht2.slots[i])
        self.assertEqual(ht.size, ht2.size)
        self.assertEqual(ht.step, ht2.step)
        self.assertEqual(ht.count, ht2.count)


class TestHashTable2HashFun(unittest.TestCase):

    def test_1(self):
        ht = HashTable2(5, 1)

        self.assertEqual(0, ht.hash_fun(None))

        self.assertEqual(3, ht.hash_fun("0"))
        self.assertEqual(4, ht.hash_fun("1"))
        self.assertEqual(0, ht.hash_fun("2"))
        self.assertEqual(1, ht.hash_fun("3"))
        self.assertEqual(2, ht.hash_fun("4"))

        self.assertEqual(3, ht.hash_fun("5"))
        self.assertEqual(4, ht.hash_fun("6"))
        self.assertEqual(0, ht.hash_fun("7"))
        self.assertEqual(1, ht.hash_fun("8"))
        self.assertEqual(2, ht.hash_fun("9"))

    def test_2(self):
        ht = HashTable2(17, 3)

        self.assertEqual(0, ht.hash_fun(None))

        self.assertEqual(15, ht.hash_fun("abc"))
        self.assertEqual(5, ht.hash_fun("Hello"))
        self.assertEqual(11, ht.hash_fun("Привет"))
        self.assertEqual(2, ht.hash_fun("123"))
        self.assertEqual(8, ht.hash_fun("привет мир"))
        self.assertEqual(16, ht.hash_fun("!"))


class TestHashTable2SeekSlot(unittest.TestCase):

    def test_1(self):
        ht = HashTable2(5, 1)

        self.assertEqual(3, ht.seek_slot("0"))
        self.assertEqual(4, ht.seek_slot("1"))
        self.assertEqual(0, ht.seek_slot("2"))
        self.assertEqual(1, ht.seek_slot("3"))
        self.assertEqual(2, ht.seek_slot("4"))

        self.assertEqual(3, ht.hash_fun("5"))
        self.assertEqual(4, ht.hash_fun("6"))
        self.assertEqual(0, ht.hash_fun("7"))
        self.assertEqual(1, ht.hash_fun("8"))
        self.assertEqual(2, ht.hash_fun("9"))

    def test_2(self):
        ht = HashTable2(17, 3)
        value = "abc"
        init = ht.hash_fun(value)
        self.assertIsNone(ht.slots[init])
        self.assertEqual(ht.seek_slot(value), init)

    def test_3(self):
        ht = HashTable2(17, 3)
        value = "abc"
        slot = ht.put(value)
        self.assertIsNotNone(slot)
        self.assertEqual(ht.seek_slot(value), slot)

    def test_4(self):
        ht = HashTable2(17, 3)
        value = "some"
        init = ht.hash_fun(value)
        ht.slots[init] = "other"
        expected = (init + ht.step) % ht.size
        self.assertEqual(ht.seek_slot(value), expected)


class TestHashTable2Put(unittest.TestCase):

    def test_0(self):
        ht = HashTable2(5, 1)

        self.assertEqual(3, ht.put("0"))
        self.assertEqual(4, ht.put("1"))
        self.assertEqual(0, ht.put("2"))
        self.assertEqual(1, ht.put("3"))
        self.assertEqual(2, ht.put("4"))

        self.assertEqual(3, ht.put("5"))
        self.assertEqual(4, ht.put("6"))
        self.assertEqual(15, ht.put("7"))
        self.assertEqual(16, ht.put("8"))
        self.assertEqual(17, ht.put("9"))

    def test_1(self):
        ht = HashTable2(5, 1)

        self.assertEqual(3, ht.put("0"))
        self.assertEqual(4, ht.put("5"))
        self.assertEqual(0, ht.put("11"))
        self.assertEqual(4, ht.put("16"))
        self.assertEqual(0, ht.put("20"))
        self.assertEqual(5, ht.put("25"))

    def test_2(self):
        ht = HashTable2(17, 3)
        value = "abc"
        slot = ht.put(value)
        self.assertIsNotNone(slot)
        self.assertEqual(ht.slots[slot], value)

    def test_3(self):
        ht = HashTable2(17, 3)
        value = "abc"
        slot1 = ht.put(value)
        slot2 = ht.put(value)
        self.assertEqual(slot1, slot2)
        self.assertEqual(ht.slots[slot1], value)


class TestHashTable2Find(unittest.TestCase):

    def test_1(self):
        ht = HashTable2(5, 1)

        self.assertEqual(3, ht.put("0"))
        self.assertEqual(3, ht.find("0"))

        self.assertEqual(4, ht.put("1"))
        self.assertEqual(4, ht.find("1"))
        self.assertEqual(0, ht.put("2"))
        self.assertEqual(0, ht.find("2"))
        self.assertEqual(1, ht.put("3"))
        self.assertEqual(1, ht.find("3"))
        self.assertEqual(2, ht.put("4"))
        self.assertEqual(2, ht.find("4"))

        self.assertEqual(3, ht.put("5"))
        self.assertEqual(3, ht.find("5"))
        self.assertEqual(4, ht.put("6"))
        self.assertEqual(4, ht.find("6"))
        self.assertEqual(15, ht.put("7"))
        self.assertEqual(15, ht.find("7"))
        self.assertEqual(16, ht.put("8"))
        self.assertEqual(16, ht.find("8"))
        self.assertEqual(17, ht.put("9"))
        self.assertEqual(17, ht.find("9"))

    def test_2(self):
        ht = HashTable2(17, 3)
        value = "abc"
        slot = ht.put(value)
        self.assertEqual(ht.find(value), slot)

    def test_3(self):
        ht = HashTable2(17, 3)
        self.assertIsNone(ht.find("0"))

    def test_4(self):
        ht = HashTable2(7, 3)
        ht.put("0")
        ht.put("1")
        ht.put("2")
        ht.put("3")
        ht.put("4")
        ht.put("5")
        ht.put("6")
        self.assertIsNone(ht.find("7"))

    def test_5(self):
        ht = HashTable2(7, 3)

        a = "2"
        b = "19"

        self.assertEqual(ht.hash_fun(a), ht.hash_fun(b))

        sa = ht.put(a)
        sb = ht.put(b)

        self.assertIsNotNone(sa)
        self.assertIsNotNone(sb)
        self.assertNotEqual(sa, sb)

        self.assertEqual(ht.find(a), sa)
        self.assertEqual(ht.find(b), sb)

class TestDoubleHashTable(unittest.TestCase):

    def test(self):
        ht = HashTable(7, 3)
        self.assertEqual(6, ht.seek_slot("0"))
        self.assertEqual(6, ht.seek_slot("7"))
        self.assertEqual(6, ht.seek_slot("17"))
        self.assertEqual(6, ht.seek_slot("24"))
        self.assertEqual(6, ht.seek_slot("31"))

        htd = DoubleHashTable(7)
        self.assertEqual(6, htd.seek_slot("0"))
        self.assertEqual(6, htd.hash_fun("0"))
        self.assertEqual(5, htd.hash_fun2("0"))

        self.assertEqual(6, htd.seek_slot("7"))
        self.assertEqual(6, htd.hash_fun("7"))
        self.assertEqual(6, htd.hash_fun2("7"))

        self.assertEqual(6, htd.seek_slot("17"))
        self.assertEqual(6, htd.hash_fun("17"))
        self.assertEqual(1, htd.hash_fun2("17"))

        self.assertEqual(6, htd.seek_slot("24"))
        self.assertEqual(6, htd.hash_fun("24"))
        self.assertEqual(5, htd.hash_fun2("24"))

        self.assertEqual(6, htd.seek_slot("31"))
        self.assertEqual(6, htd.hash_fun("31"))
        self.assertEqual(3, htd.hash_fun2("31"))

        self.assertEqual(6, htd.seek_slot("0"))
        self.assertEqual(6, htd.put("0"))
        self.assertEqual(0, htd.seek_slot("7"))
        self.assertEqual(0, htd.put("7"))
        self.assertEqual(1, htd.seek_slot("17"))
        self.assertEqual(1, htd.put("17"))
        self.assertEqual(5, htd.seek_slot("24"))
        self.assertEqual(5, htd.put("24"))
        self.assertEqual(3, htd.seek_slot("31"))
        self.assertEqual(3, htd.put("31"))



class TestHashTableSalted(unittest.TestCase):

    def test(self):
        ht = HashTable(7, 3)
        self.assertEqual(6, ht.hash_fun("0"))
        self.assertEqual(6, ht.hash_fun("7"))
        self.assertEqual(6, ht.hash_fun("17"))
        self.assertEqual(6, ht.hash_fun("24"))
        self.assertEqual(6, ht.hash_fun("31"))

        hts = HashTableSalted(17, 3, 0x12345678)
        self.assertEqual(0, hts.hash_fun("0"))
        self.assertEqual(7, hts.hash_fun("7"))
        self.assertEqual(12, hts.hash_fun("17"))
        self.assertEqual(6, hts.hash_fun("24"))
        self.assertEqual(0, hts.hash_fun("31"))

        hts2 = HashTableSalted(17, 3, 0x12345670)
        self.assertEqual(7, hts2.hash_fun("0"))
        self.assertEqual(14, hts2.hash_fun("7"))
        self.assertEqual(8, hts2.hash_fun("17"))
        self.assertEqual(2, hts2.hash_fun("24"))
        self.assertEqual(13, hts2.hash_fun("31"))
