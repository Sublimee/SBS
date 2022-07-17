package lesson01;

import org.example.algo01.lesson01.Accumulator;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import static lesson01.TestUtils.getLinkedList;

public class AccumulatorTest {

    @Test
    void processEmptyTest() {
        Assertions.assertEquals(getLinkedList(), Accumulator.process(getLinkedList(), getLinkedList()));
    }

    @Test
    void processSingleTest() {
        Assertions.assertEquals(getLinkedList(3), Accumulator.process(getLinkedList(1), getLinkedList(2)));
    }

    @Test
    void processPairTest() {
        Assertions.assertEquals(getLinkedList(3, 8), Accumulator.process(getLinkedList(1, 3), getLinkedList(2, 5)));
    }

    @Test
    void processDifferentSizeTest() {
        Assertions.assertNull(Accumulator.process(getLinkedList(1, 2), getLinkedList(1, 3, 5)));
    }

    @Test
    void processDifferentSize1Test() {
        Assertions.assertNull(Accumulator.process(getLinkedList(), getLinkedList(1, 3, 5)));
    }

    @Test
    void processDifferentSize2Test() {
        Assertions.assertNull(Accumulator.process(getLinkedList(1, 2), getLinkedList()));
    }

}