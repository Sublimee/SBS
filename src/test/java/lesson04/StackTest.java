package lesson04;

import org.example.algo01.lesson04.Stack;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.*;
import java.util.stream.IntStream;

public class StackTest {

    @Test
    void pushTest() {
        Stack<Integer> actual = new Stack<>();
        IntStream.range(1, 5).forEach(actual::push);

        Assertions.assertEquals(Arrays.asList(1, 2, 3, 4), actual.elements);
    }

    @Test
    void popTest() {
        Stack<Integer> source = new Stack<>();
        IntStream.range(1, 5).forEach(source::push);

        Stack<Integer> destination = new Stack<>();
        IntStream.range(1, 5).forEach(it -> destination.push(source.pop()));

        Assertions.assertEquals(0, source.size());
        Assertions.assertEquals(Arrays.asList(4, 3, 2, 1), destination.elements);
    }

    @Test
    void popEmptyTest() {
        Assertions.assertNull(new Stack<Integer>().pop());
    }

    @Test
    void peekTest() {
        Stack<Integer> source = new Stack<>();
        IntStream.range(1, 5).forEach(source::push);

        Stack<Integer> destination = new Stack<>();
        IntStream.range(1, 5).forEach(it -> destination.push(source.peek()));

        Assertions.assertEquals(Arrays.asList(1, 2, 3, 4), source.elements);
        Assertions.assertEquals(Arrays.asList(4, 4, 4, 4), destination.elements);
    }

    @Test
    void peekEmptyTest() {
        Assertions.assertNull(new Stack<Integer>().peek());
    }
}
