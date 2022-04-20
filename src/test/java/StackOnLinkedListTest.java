import org.example.lesson04.StackOnLinkedList;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.*;
import java.util.stream.IntStream;

public class StackOnLinkedListTest {

    @Test
    void pushTest() {
        StackOnLinkedList<Integer> actual = new StackOnLinkedList<>();
        IntStream.range(1, 5).forEach(actual::push);

        Assertions.assertEquals(Arrays.asList(4, 3, 2, 1), actual.elements);
    }

    @Test
    void popTest() {
        StackOnLinkedList<Integer> source = new StackOnLinkedList<>();
        IntStream.range(1, 5).forEach(source::push);

        StackOnLinkedList<Integer> destination = new StackOnLinkedList<>();
        IntStream.range(1, 5).forEach(it -> destination.push(source.pop()));

        Assertions.assertEquals(0, source.size());
        Assertions.assertEquals(Arrays.asList(1, 2,3, 4), destination.elements);
    }

    @Test
    void popEmptyTest() {
        Assertions.assertNull(new StackOnLinkedList<Integer>().pop());
    }

    @Test
    void peekTest() {
        StackOnLinkedList<Integer> source = new StackOnLinkedList<>();
        IntStream.range(1, 5).forEach(source::push);

        StackOnLinkedList<Integer> destination = new StackOnLinkedList<>();
        IntStream.range(1, 5).forEach(it -> destination.push(source.peek()));

        Assertions.assertEquals(Arrays.asList(4, 3, 2, 1), source.elements);
        Assertions.assertEquals(Arrays.asList(4, 4, 4, 4), destination.elements);
    }

    @Test
    void peekEmptyTest() {
        Assertions.assertNull(new StackOnLinkedList<Integer>().peek());
    }
}
