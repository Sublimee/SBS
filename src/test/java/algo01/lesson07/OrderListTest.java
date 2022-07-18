package algo01.lesson07;

import org.example.algo01.lesson07.Node;
import org.example.algo01.lesson07.OrderedList;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.*;
import java.util.stream.Stream;

public class OrderListTest {

    @ParameterizedTest
    @MethodSource("provideIntegerValues")
    void compareIntegersTest(Integer expected, Integer some, Integer another) {
        OrderedList<Integer> list = new OrderedList<>(true);
        Assertions.assertEquals(expected, list.compare(some, another));
    }

    @ParameterizedTest
    @MethodSource("provideStringValues")
    void compareStringTest(Integer expected, String some, String another) {
        OrderedList<String> list = new OrderedList<>(true);
        Assertions.assertEquals(expected, list.compare(some, another));
    }

    @Test
    void compareUnsupportedTest() {
        OrderedList<Object> list = new OrderedList<>(true);
        Assertions.assertThrows(ClassCastException.class, () -> list.compare(new Object(), new Object()));
    }

    @Test
    void manyMixedAscendingTest() {
        Integer[] expected = Arrays.asList(1, 1, 3, 5, 6).toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(true, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(true, 1, 5, 3, 1, 6);

        assertOrderedListEquals(expectedOrderedList, expected, 5, actualOrderedList);
    }

    @Test
    void manyMixedDescendingTest() {
        Integer[] expected = Arrays.asList(6, 5, 3, 1, 1).toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(false, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false, 1, 5, 3, 1, 6);

        assertOrderedListEquals(expectedOrderedList, expected, 5, actualOrderedList);
    }

    @Test
    void singleAscendingTest() {
        Integer[] expected = List.of(1).toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(true, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(true, 1);

        assertOrderedListEquals(expectedOrderedList, expected, 1, actualOrderedList);
    }

    @Test
    void singleDescendingTest() {
        Integer[] expected = List.of(1).toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(false, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false, 1);

        assertOrderedListEquals(expectedOrderedList, expected, 1, actualOrderedList);
    }

    @Test
    void pairAscendingTest() {
        Integer[] expected = Arrays.asList(1, 2).toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(true, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(true, 1, 2);

        assertOrderedListEquals(expectedOrderedList, expected, 2, actualOrderedList);
    }

    @Test
    void pairDescendingTest() {
        Integer[] expected = Arrays.asList(2, 1).toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(false, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false, 1, 2);

        assertOrderedListEquals(expectedOrderedList, expected, 2, actualOrderedList);
    }

    @Test
    void manyReverseOrderedAscendingTest() {
        Integer[] expected = Arrays.asList(1, 2, 3).toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(true, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(true, 3, 2, 1);

        assertOrderedListEquals(expectedOrderedList, expected, 3, actualOrderedList);
    }

    @Test
    void manyStraightOrderedAscendingTest() {
        Integer[] expected = Arrays.asList(1, 2, 3).toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(true, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(true, 1, 2, 3);

        assertOrderedListEquals(expectedOrderedList, expected, 3, actualOrderedList);
    }

    @Test
    void manyReverseOrderedDescendingTest() {
        Integer[] expected = Arrays.asList(3, 2, 1).toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(false, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false, 1, 2, 3);

        assertOrderedListEquals(expectedOrderedList, expected, 3, actualOrderedList);
    }

    @Test
    void manyStraightOrderedDescendingTest() {
        Integer[] expected = Arrays.asList(3, 2, 1).toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(false, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false, 3, 2, 1);

        assertOrderedListEquals(expectedOrderedList, expected, 3, actualOrderedList);
    }

    @Test
    void complexAscendingWithDuplicatesTest() {
        Integer[] expected = Arrays.asList(0, 1, 1, 2, 2, 3, 3, 4).toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(true, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(true, 4, 0, 1, 2, 3, 3, 2, 1);

        assertOrderedListEquals(expectedOrderedList, expected, 8, actualOrderedList);
    }

    @Test
    void complexDescendingWithDuplicatesTest() {
        Integer[] expected = Arrays.asList(4, 3, 3, 2, 2, 1, 1, 0).toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(false, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false, 4, 0, 1, 2, 3, 3, 2, 1);

        assertOrderedListEquals(expectedOrderedList, expected, 8, actualOrderedList);
    }

    @Test
    void clearTest() {
        Integer[] expected = List.of().toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(true, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false, 4, 0, 1, 2, 3, 3, 2, 1);
        actualOrderedList.clear(true);

        assertOrderedListEquals(expectedOrderedList, expected, 0, actualOrderedList);
    }

    @Test
    void deleteFromEmptyTest() {
        Integer[] expected = List.of().toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(false, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false);
        actualOrderedList.delete(4);
        actualOrderedList.delete(2);
        actualOrderedList.delete(0);

        assertOrderedListEquals(expectedOrderedList, expected, 0, actualOrderedList);
    }

    @Test
    void deleteFromSingleTest() {
        Integer[] expected = List.of().toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(false, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false);
        actualOrderedList.delete(4);

        assertOrderedListEquals(expectedOrderedList, expected, 0, actualOrderedList);
    }

    @Test
    void deleteFromPairTest() {
        Integer[] expected = List.of(3).toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(false, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false, 3, 3);
        actualOrderedList.delete(3);

        assertOrderedListEquals(expectedOrderedList, expected, 1, actualOrderedList);
    }

    @Test
    void deleteFromManyTest() {
        Integer[] expected = List.of(3, 3, 2, 1, 1).toArray(Integer[]::new);

        OrderedList<Integer> expectedOrderedList = getExpectedOrderedList(false, expected);
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false, 4, 0, 1, 2, 3, 3, 2, 1);
        actualOrderedList.delete(4);
        actualOrderedList.delete(2);
        actualOrderedList.delete(0);

        assertOrderedListEquals(expectedOrderedList, expected, 5, actualOrderedList);
    }

    @Test
    void findFromEmptyAscendingTest() {
        OrderedList<Integer> actualOrderedList = getActualOrderedList(true);

        Assertions.assertNull(actualOrderedList.find(4));
    }

    @Test
    void findFromEmptyDescendingTest() {
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false);

        Assertions.assertNull(actualOrderedList.find(4));
    }

    @Test
    void findFromSingleAscendingTest() {
        OrderedList<Integer> actualOrderedList = getActualOrderedList(true, 4);

        Assertions.assertEquals(4, actualOrderedList.find(4).value);
    }

    @Test
    void findFromSingleDescendingTest() {
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false, 4);

        Assertions.assertEquals(4, actualOrderedList.find(4).value);
    }

    @Test
    void findFromPairFirstAscendingTest() {
        OrderedList<Integer> actualOrderedList = getActualOrderedList(true, 4, 3);

        Assertions.assertEquals(3, actualOrderedList.find(3).value);
    }

    @Test
    void findFromPairLastAscendingTest() {
        OrderedList<Integer> actualOrderedList = getActualOrderedList(true, 4, 3);

        Assertions.assertEquals(4, actualOrderedList.find(4).value);
    }

    @Test
    void findFromPairFirstDescendingTest() {
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false, 4, 3);

        Assertions.assertEquals(4, actualOrderedList.find(4).value);
    }

    @Test
    void findFromPairLastDescendingTest() {
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false, 4, 3);

        Assertions.assertEquals(3, actualOrderedList.find(3).value);
    }

    @Test
    void findFromManyAscendingTest() {
        OrderedList<Integer> actualOrderedList = getActualOrderedList(true, 4, 1, 2, 3, 3, 2, 1);

        Assertions.assertEquals(4, actualOrderedList.find(4).value);
        Assertions.assertEquals(2, actualOrderedList.find(2).value);
        Assertions.assertEquals(1, actualOrderedList.find(1).value);
        Assertions.assertNull(actualOrderedList.find(0));
    }

    @Test
    void findFromManyDescendingTest() {
        OrderedList<Integer> actualOrderedList = getActualOrderedList(false, 4, 0, 1, 2, 3, 3, 2, 1);

        Assertions.assertEquals(4, actualOrderedList.find(4).value);
        Assertions.assertEquals(2, actualOrderedList.find(2).value);
        Assertions.assertEquals(0, actualOrderedList.find(0).value);
        Assertions.assertNull(actualOrderedList.find(5));
    }


    private void assertOrderedListEquals(
            OrderedList<Integer> expectedOrderedList,
            Integer[] expectedOrderedElements,
            int expectedSize,
            OrderedList<Integer> actualOrderedList
    ) {
        Assertions.assertEquals(expectedOrderedList, actualOrderedList);
        Assertions.assertEquals(expectedSize, actualOrderedList.count());
        Assertions.assertArrayEquals(expectedOrderedElements, actualOrderedList.getAll().stream().map(x -> x.value).toArray());
    }


    private static Stream<Arguments> provideIntegerValues() {
        return Stream.of(
                Arguments.of(-1, 1, 2),
                Arguments.of(0, 1, 1),
                Arguments.of(1, 2, 1)
        );
    }

    private static Stream<Arguments> provideStringValues() {
        return Stream.of(
                Arguments.of(-1, "aa", "ab"),
                Arguments.of(0, "aa", "aa"),
                Arguments.of(0, "aa", "aa "),
                Arguments.of(0, "aa", " aa"),
                Arguments.of(0, "aa", " aa "),
                Arguments.of(0, "aa ", "aa"),
                Arguments.of(0, "aa ", "aa "),
                Arguments.of(0, "aa ", " aa "),
                Arguments.of(0, "aa ", " aa "),
                Arguments.of(0, " aa", "aa"),
                Arguments.of(0, " aa", "aa "),
                Arguments.of(0, " aa", " aa"),
                Arguments.of(0, " aa", " aa "),
                Arguments.of(0, " aa ", "aa"),
                Arguments.of(0, " aa ", "aa "),
                Arguments.of(0, " aa ", " aa"),
                Arguments.of(0, " aa ", " aa "),
                Arguments.of(1, "ab", "aa")
        );
    }

    private OrderedList<Integer> getActualOrderedList(boolean ascending, int... values) {
        OrderedList orderedList = new OrderedList(ascending);
        for (Integer value : values) {
            orderedList.add(value);
        }
        return orderedList;
    }

    private OrderedList<Integer> getExpectedOrderedList(boolean ascending, Integer[] values) {
        OrderedList orderedList = new OrderedList(ascending);

        Node<Integer> prev = null;
        for (Integer value : values) {
            Node<Integer> current = new Node<>(value);
            if (orderedList.head == null) {
                orderedList.head = current;
            } else {
                prev.next = current;
                current.prev = prev;
            }
            prev = current;
        }
        orderedList.tail = prev;
        return orderedList;
    }
}
