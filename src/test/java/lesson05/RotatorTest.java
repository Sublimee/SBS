package lesson05;

import org.example.algo.lesson05.Queue;
import org.example.algo.lesson05.Rotator;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.*;
import java.util.stream.IntStream;

public class RotatorTest {

    @Test
    void rotateManyTimesTest() {
        Rotator rotator = new Rotator();
        Queue<Integer> queue = new Queue<>();
        IntStream.range(1, 5).forEach(queue::enqueue);
        rotator.rotate(queue, 7);
        Assertions.assertArrayEquals(Arrays.asList(4, 1, 2, 3).toArray(), queue.queue.toArray());
    }

    @Test
    void rotateOneTimeTest() {
        Rotator rotator = new Rotator();
        Queue<Integer> queue = new Queue<>();
        IntStream.range(1, 5).forEach(queue::enqueue);
        rotator.rotate(queue, 1);
        Assertions.assertArrayEquals(Arrays.asList(2, 3, 4, 1).toArray(), queue.queue.toArray());
    }
}
