import org.example.lesson04.OperandStack;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.*;

public class OperandStackTest {

    private final OperandStack operandStack = new OperandStack();

    @Test
    void process1Test() {
        Assertions.assertEquals(59, operandStack.process(Arrays.asList(8, 2, "+", 5, "*", 9, "+", "=")));
    }

    @Test
    void process2Test() {
        Assertions.assertEquals(9, operandStack.process(Arrays.asList(1, 2, "+", 3, "*", "=")));
    }
}
