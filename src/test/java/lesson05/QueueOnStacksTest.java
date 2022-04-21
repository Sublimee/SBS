package lesson05;

import org.example.lesson05.QueueOnStacks;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class QueueOnStacksTest {

    @Test
    void addTwoTest() {
        QueueOnStacks<Integer> queue = new QueueOnStacks();

        queue.enqueue(1);
        queue.enqueue(2);
        queue.enqueue(3);
        queue.enqueue(4);

        Assertions.assertEquals(1, queue.dequeue());

        Assertions.assertEquals(2, queue.dequeue());

        queue.enqueue(5);

        Assertions.assertEquals(3, queue.dequeue());

        queue.enqueue(6);

        Assertions.assertEquals(4, queue.dequeue());

        queue.enqueue(7);
        queue.enqueue(8);

        Assertions.assertEquals(5, queue.dequeue());
        Assertions.assertEquals(6, queue.dequeue());
    }
}
