package lesson06;

import org.example.algo.lesson06.Deque;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.*;
import java.util.stream.IntStream;

public class DequeTest {

    @Test
    void addFrontTest() {
        Deque<Integer> deque = new Deque<>();
        IntStream.range(1, 5).forEach(deque::addFront);

        Assertions.assertArrayEquals(Arrays.asList(4, 3, 2, 1).toArray(), deque.list.toArray(new Integer[0]));
        Assertions.assertEquals(4, deque.size());
    }

    @Test
    void addTailTest() {
        Deque<Integer> deque = new Deque<>();
        IntStream.range(1, 5).forEach(deque::addTail);

        Assertions.assertArrayEquals(Arrays.asList(1, 2, 3, 4).toArray(), deque.list.toArray(new Integer[0]));
        Assertions.assertEquals(4, deque.size());
    }

    @Test
    void removeTailTest() {
        Deque<Integer> deque = new Deque<>();
        IntStream.range(1, 10).forEach(deque::addTail);
        IntStream.range(5, 10).forEach(x -> deque.removeTail());
        Assertions.assertArrayEquals(Arrays.asList(1, 2, 3, 4).toArray(), deque.list.toArray(new Integer[0]));
        Assertions.assertEquals(4, deque.size());
    }

    @Test
    void removeFrontTest() {
        Deque<Integer> deque = new Deque<>();
        IntStream.range(1, 10).forEach(deque::addTail);
        IntStream.range(1, 5).forEach(x -> deque.removeFront());
        Assertions.assertArrayEquals(Arrays.asList(5, 6, 7, 8, 9).toArray(), deque.list.toArray(new Integer[0]));
        Assertions.assertEquals(5, deque.size());
    }

    @Test
    void complexTest() {
        Deque<Integer> deque = new Deque<>();
        deque.addTail(2);
        deque.addFront(1);
        deque.addTail(3);
        deque.addFront(0);
        Assertions.assertArrayEquals(Arrays.asList(0, 1, 2, 3).toArray(), deque.list.toArray(new Integer[0]));
        Assertions.assertEquals(4, deque.size());
    }
}
