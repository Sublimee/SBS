package algo01.lesson01;

import org.example.algo01.lesson01.Accumulator;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class AccumulatorTest {

    @Test
    void processEmptyTest() {
        Assertions.assertEquals(TestUtils.getLinkedList(), Accumulator.process(TestUtils.getLinkedList(), TestUtils.getLinkedList()));
    }

    @Test
    void processSingleTest() {
        Assertions.assertEquals(TestUtils.getLinkedList(3), Accumulator.process(TestUtils.getLinkedList(1), TestUtils.getLinkedList(2)));
    }

    @Test
    void processPairTest() {
        Assertions.assertEquals(TestUtils.getLinkedList(3, 8), Accumulator.process(TestUtils.getLinkedList(1, 3), TestUtils.getLinkedList(2, 5)));
    }

    @Test
    void processDifferentSizeTest() {
        Assertions.assertNull(Accumulator.process(TestUtils.getLinkedList(1, 2), TestUtils.getLinkedList(1, 3, 5)));
    }

    @Test
    void processDifferentSize1Test() {
        Assertions.assertNull(Accumulator.process(TestUtils.getLinkedList(), TestUtils.getLinkedList(1, 3, 5)));
    }

    @Test
    void processDifferentSize2Test() {
        Assertions.assertNull(Accumulator.process(TestUtils.getLinkedList(1, 2), TestUtils.getLinkedList()));
    }

}