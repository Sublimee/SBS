package lesson03;

import org.example.lesson03.DynArray;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Array;
import java.util.stream.IntStream;

import static org.example.lesson03.DynArray.MIN_CAPACITY;

public class DynArrayTest {

    @Test
    void constructorTest() {
        DynArray<Integer> actual = new DynArray<>(Integer.class);

        Assertions.assertEquals(getExpectedArray(MIN_CAPACITY, 0), actual);
    }

    @Test
    void makeArrayLegalPositiveCapacityTest() {
        DynArray<Integer> actual = new DynArray<>(Integer.class);
        actual.makeArray(MIN_CAPACITY + 1);

        Assertions.assertEquals(getExpectedArray(MIN_CAPACITY + 1, 0), actual);
    }

    @Test
    void makeArrayIllegalPositiveCapacityTest() {
        DynArray<Integer> actual = new DynArray<>(Integer.class);
        actual.makeArray(MIN_CAPACITY - 1);

        Assertions.assertEquals(getExpectedArray(MIN_CAPACITY, 0), actual);
    }

    @Test
    void makeArrayIllegalNegativeCapacityTest() {
        DynArray<Integer> actual = new DynArray<>(Integer.class);
        actual.makeArray(-1);

        Assertions.assertEquals(getExpectedArray(MIN_CAPACITY, 0), actual);
    }

    @Test
    void makeArrayIllegalZeroCapacityTest() {
        DynArray<Integer> actual = new DynArray<>(Integer.class);
        actual.makeArray(0);

        Assertions.assertEquals(getExpectedArray(MIN_CAPACITY, 0), actual);
    }

    @Test
    void getItemLessThanLeftBoundTest() {
        DynArray<Integer> array = new DynArray<>(Integer.class);
        Assertions.assertThrows(ArrayIndexOutOfBoundsException.class, () -> array.getItem(-1));
    }

    @Test
    void getItemMoreThanRightBoundTest() {
        DynArray<Integer> array = new DynArray<>(Integer.class);
        Assertions.assertThrows(ArrayIndexOutOfBoundsException.class, () -> array.getItem(MIN_CAPACITY));
    }

    @Test
    void getItemLegalIndexTest() {
        DynArray<Integer> array = new DynArray<>(Integer.class);
        IntStream.range(0, MIN_CAPACITY).forEach(array::append);
        IntStream.range(0, MIN_CAPACITY).forEach(it -> Assertions.assertEquals(it, array.getItem(it)));
    }

    @Test
    void getItemFirstElementFromEmptyTest() {
        DynArray<Integer> array = new DynArray<>(Integer.class);
        Assertions.assertNull(array.getItem(0));
    }

    @Test
    void getItemLastElementFromEmptyTest() {
        DynArray<Integer> array = new DynArray<>(Integer.class);
        Assertions.assertNull(array.getItem(MIN_CAPACITY - 1));
    }

    @Test
    void appendWithNoResizeTest() {
        DynArray<Integer> actual = new DynArray<>(Integer.class);
        IntStream.range(0, MIN_CAPACITY).forEach(actual::append);

        Assertions.assertEquals(getExpectedArray(MIN_CAPACITY, MIN_CAPACITY), actual);
    }

    @Test
    void appendWithResizeTest() {
        DynArray<Integer> actual = new DynArray<>(Integer.class);
        IntStream.range(0, MIN_CAPACITY + 1).forEach(actual::append);

        Assertions.assertEquals(getExpectedArray(2 * MIN_CAPACITY, MIN_CAPACITY + 1), actual);
    }

    @Test
    void appendWithManyResizeTest() {
        DynArray<Integer> actual = new DynArray<>(Integer.class);
        IntStream.range(0, 2 * MIN_CAPACITY + 1).forEach(actual::append);

        Assertions.assertEquals(getExpectedArray(4 * MIN_CAPACITY, 2 * MIN_CAPACITY + 1), actual);
    }

    @Test
    void insertToEmptyTest() {
        DynArray<Integer> actual = new DynArray<>(Integer.class);
        actual.insert(0, 0);

        Assertions.assertEquals(getExpectedArray(MIN_CAPACITY, 1), actual);
    }

    @Test
    void insertToLessThanLeftBoundTest() {
        DynArray<Integer> array = new DynArray<>(Integer.class);
        Assertions.assertThrows(ArrayIndexOutOfBoundsException.class, () -> array.insert(1, -1));
    }

    @Test
    void insertToTailTest() {
        DynArray<Integer> actual = new DynArray<>(Integer.class);
        actual.append(0);
        actual.insert(1, 1);

        Assertions.assertEquals(getExpectedArray(MIN_CAPACITY, 2), actual);
    }

    @Test
    void insertMoreThanRightBoundTest() {
        DynArray<Integer> array = new DynArray<>(Integer.class);
        array.append(0);
        Assertions.assertThrows(ArrayIndexOutOfBoundsException.class, () -> array.insert(1, 2));
    }

    @Test
    void insertWithResizeTest() {
        DynArray<Integer> actual = new DynArray<>(Integer.class);
        IntStream.range(0, MIN_CAPACITY + 1).forEach(x -> actual.insert(x, x));

        Assertions.assertEquals(getExpectedArray(2 * MIN_CAPACITY, MIN_CAPACITY + 1), actual);
    }

    @Test
    void insertWithManyResizeTest() {
        DynArray<Integer> actual = new DynArray<>(Integer.class);
        IntStream.range(0, 2 * MIN_CAPACITY + 1).forEach(x -> actual.insert(x, x));

        Assertions.assertEquals(getExpectedArray(4 * MIN_CAPACITY, 2 * MIN_CAPACITY + 1), actual);
    }

    @Test
    void removeWithNoResizeTest() {
        DynArray<Integer> actual = new DynArray<>(Integer.class);
        IntStream.range(0, 2 * MIN_CAPACITY + 1).forEach(x -> actual.insert(x, x));
        actual.remove(2 * MIN_CAPACITY);

        Assertions.assertEquals(getExpectedArray(4 * MIN_CAPACITY, 2 * MIN_CAPACITY), actual);
    }

    @Test
    void removeWithManyResizeTest() {
        DynArray<Integer> actual = new DynArray<>(Integer.class);
        IntStream.range(0, 2 * MIN_CAPACITY + 10).forEach(x -> actual.insert(x, x));
        IntStream.range(0, 2 * MIN_CAPACITY + 1).forEach(x -> actual.remove(2 * MIN_CAPACITY + 10 - 1 - x));

        Assertions.assertEquals(getExpectedArray(18, 9), actual);
    }

    // TODO refactor above
    @Test
    void complexAppendTest() {
        DynArray<Integer> array = new DynArray<>(Integer.class);
        IntStream.range(0, 33).forEach(array::append);
        Assertions.assertEquals(array.capacity, 64);
        Assertions.assertEquals(array.count, 33);

        Integer[] expected = (Integer[]) Array.newInstance(Integer.class, 64);
        System.arraycopy(IntStream.range(0, 33).boxed().toArray(), 0, expected, 0, 33);

        Assertions.assertArrayEquals(expected, array.array);

        Assertions.assertThrows(ArrayIndexOutOfBoundsException.class, () -> array.getItem(-1));
        Assertions.assertEquals(0, array.getItem(0));
        Assertions.assertEquals(32, array.getItem(32));
        Assertions.assertThrows(ArrayIndexOutOfBoundsException.class, () -> array.getItem(64));
    }

    @Test
    void complexInsertAsAppendTest() {
        DynArray<Integer> array = new DynArray<>(Integer.class);
        IntStream.range(0, 33).forEach(x -> array.insert(x, x));
        Assertions.assertEquals(array.capacity, 64);
        Assertions.assertEquals(array.count, 33);

        Integer[] expected = (Integer[]) Array.newInstance(Integer.class, 64);
        System.arraycopy(IntStream.range(0, 33).boxed().toArray(), 0, expected, 0, 33);

        Assertions.assertArrayEquals(expected, array.array);

        Assertions.assertThrows(ArrayIndexOutOfBoundsException.class, () -> array.getItem(-1));
        Assertions.assertEquals(0, array.getItem(0));
        Assertions.assertEquals(32, array.getItem(32));
        Assertions.assertThrows(ArrayIndexOutOfBoundsException.class, () -> array.getItem(64));
    }

    @Test
    void complexInsertTest() {
        DynArray<Integer> array = new DynArray<>(Integer.class);
        IntStream.range(0, 16).forEach(array::append);

        Assertions.assertEquals(16, array.capacity);
        Assertions.assertEquals(16, array.count);
        IntStream.range(0, 16).forEach(x -> array.insert(x, x * 2 + 1));
        Assertions.assertEquals(32, array.capacity);
        Assertions.assertEquals(32, array.count);

        array.insert(100500, 0);
        array.insert(100500, 32);

        Assertions.assertEquals(64, array.capacity);
        Assertions.assertEquals(34, array.count);

        Assertions.assertThrows(ArrayIndexOutOfBoundsException.class, () -> array.insert(1, -1));
        Assertions.assertEquals(100500, array.getItem(0));
        Assertions.assertEquals(100500, array.getItem(32));
        Assertions.assertEquals(15, array.getItem(33));
        Assertions.assertThrows(ArrayIndexOutOfBoundsException.class, () -> array.insert(1, 64));
    }

    @Test
    void complexInsertTailTest() {
        DynArray<Integer> array = new DynArray<>(Integer.class);
        IntStream.range(0, 16).forEach(x -> array.insert(x, array.count));

        Assertions.assertEquals(16, array.capacity);
        Assertions.assertEquals(16, array.count);

        array.insert(100500, 5);
        array.insert(100500, array.count);

        Assertions.assertEquals(32, array.capacity);
        Assertions.assertEquals(18, array.count);
        Assertions.assertEquals(100500, array.getItem(5));


        Assertions.assertThrows(ArrayIndexOutOfBoundsException.class, () -> array.insert(1, -1));
        Assertions.assertEquals(0, array.getItem(0));
        Assertions.assertEquals(15, array.getItem(16));
        Assertions.assertEquals(100500, array.getItem(17));
        Assertions.assertNull(array.getItem(18));
        Assertions.assertThrows(ArrayIndexOutOfBoundsException.class, () -> array.insert(1, 19));
    }

    @Test
    void complexRemoveTest() {
        DynArray<Integer> array = new DynArray<>(Integer.class);
        IntStream.range(0, 16).forEach(x -> array.insert(x, array.count));

        Assertions.assertEquals(16, array.capacity);
        Assertions.assertEquals(16, array.count);

        IntStream.range(0, 16).forEach(x -> array.remove(0));

        Assertions.assertEquals(16, array.capacity);
        Assertions.assertEquals(0, array.count);
    }

    @Test
    void complexRemoveWithDecreaseSizeTest() {
        DynArray<Integer> array = new DynArray<>(Integer.class);
        IntStream.range(0, 16).forEach(x -> array.insert(x, array.count));

        Assertions.assertEquals(16, array.capacity);
        Assertions.assertEquals(16, array.count);

        array.insert(100500, array.count);

        Assertions.assertEquals(32, array.capacity);
        Assertions.assertEquals(17, array.count);

        array.remove(0);

        Assertions.assertEquals(32, array.capacity);
        Assertions.assertEquals(16, array.count);

        array.remove(0);

        Assertions.assertEquals(21, array.capacity);
        Assertions.assertEquals(15, array.count);

        IntStream.range(0, 5).forEach(x -> array.remove(0));

        Assertions.assertEquals(16, array.capacity);
        Assertions.assertEquals(10, array.count);
    }

    private DynArray<Integer> getExpectedArray(int capacity, int count) {
        DynArray<Integer> array = new DynArray<>(Integer.class);

        Integer[] expected = (Integer[]) Array.newInstance(Integer.class, capacity);
        System.arraycopy(IntStream.range(0, count).boxed().toArray(), 0, expected, 0, count);

        array.array = expected;
        array.capacity = capacity;
        array.count = count;

        return array;
    }
}
