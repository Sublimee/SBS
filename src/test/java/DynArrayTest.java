import org.example.lesson03.DynArray;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Array;
import java.util.stream.IntStream;

public class DynArrayTest {

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
}
