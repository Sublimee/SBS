package org.example.algo01.lesson05;

import java.util.stream.IntStream;

public class Rotator {

    public <T> void rotate(Queue<T> queue, int shift) {
        IntStream.range(0, shift).forEach(x -> queue.enqueue(queue.dequeue()));
    }

}
