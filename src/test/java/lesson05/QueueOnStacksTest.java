package lesson05;

import org.example.lesson05.QueueOnStacks;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class QueueOnStacksTest {

    @Test
    void addOneTest() {
        QueueOnStacks<Integer> queue = new QueueOnStacks<>();

        queue.enqueue(1);


        Assertions.assertEquals(1, queue.dequeue());
    }

    @Test
    void addTwoTest() {
        QueueOnStacks<Integer> queue = new QueueOnStacks<>();

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


    @Test
    void dequeueFromEmptyTest() {
        QueueOnStacks<Integer> queue = new QueueOnStacks<>();
        Assertions.assertNull(queue.dequeue());
    }

    @Test
    void addSomeTest() {
        QueueOnStacks<Integer> queue = new QueueOnStacks<>();

        Assertions.assertNull(queue.dequeue());

        queue.enqueue(1);

        Assertions.assertEquals(1, queue.dequeue());

        queue.enqueue(2);
        queue.enqueue(3);

        Assertions.assertEquals(2, queue.dequeue());
        Assertions.assertEquals(3, queue.dequeue());

        Assertions.assertNull(queue.dequeue());

        queue.enqueue(4);
        queue.enqueue(5);
        queue.enqueue(6);

        Assertions.assertEquals(4, queue.dequeue());
    }
}
