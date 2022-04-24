package lesson04;

import org.example.lesson04.OperandStack;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import java.math.BigInteger;
import java.util.*;
import java.util.stream.Stream;

public class OperandStackTest {

    private final OperandStack operandStack = new OperandStack();

    @ParameterizedTest
    @MethodSource("provideValuesForProcessTest")
    void processTest(Integer expected, List<Object> input) {
        Assertions.assertEquals(BigInteger.valueOf(expected), operandStack.process(input));
    }

    private static Stream<Arguments> provideValuesForProcessTest() {
        return Stream.of(
                Arguments.of(59, Arrays.asList(8, 2, "+", 5, "*", 9, "+", "=")),
                Arguments.of(9, Arrays.asList(1, 2, "+", 3, "*", "=")),
                Arguments.of(6, Arrays.asList(19, 2, "/", 3, "-", "=")),
                Arguments.of(6, Arrays.asList(10, 2, "*", 3, "/", "="))
        );
    }
}
