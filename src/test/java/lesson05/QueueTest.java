package lesson05;

import org.example.algo.lesson05.Queue;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.stream.IntStream;

public class QueueTest {

    @Test
    void enqueueDequeueTest() {
        Queue<Integer> queue = new Queue<>();
        IntStream.range(1, 5).forEach(queue::enqueue);
        Assertions.assertEquals(4, queue.size());
        IntStream.range(1, 5).forEach(x -> Assertions.assertEquals(x, queue.dequeue()));
    }

    @Test
    void removeEmptyTest() {
        Queue<Integer> queue = new Queue<>();
        Assertions.assertNull(queue.dequeue());
    }
}
