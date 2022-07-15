package org.example.algo.lesson04;

import java.math.BigInteger;
import java.util.*;
import java.util.function.BiFunction;

public class OperandStack {

    private Stack<Object> accumulator;

    public BigInteger process(List<Object> sequence) {
        Stack<Object> operands = new Stack<>();
        accumulator = new Stack<>();

        for (int i = sequence.size() - 1; i >= 0; i--) {
            operands.push(sequence.get(i));
        }

        Object value;
        while ((value = operands.pop()) != null) {
            if (value instanceof Number) {
                accumulator.push(BigInteger.valueOf((Integer) value));
            } else {
                switch ((String) value) {
                    case "+" -> sumOperands();
                    case "*" -> multiplyOperands();
                    case "/" -> divideOperands();
                    case "-" -> subtractOperands();
                    case "=" -> {
                        return (BigInteger) accumulator.pop();
                    }
                }
            }
        }
        return null;
    }

    private void sumOperands() {
        processOperands(BigInteger::add);
    }

    private void multiplyOperands() {
        processOperands(BigInteger::multiply);
    }

    private void divideOperands() {
        processOperands(BigInteger::divide);
    }

    private void subtractOperands() {
        processOperands(BigInteger::subtract);
    }

    private void processOperands(BiFunction<BigInteger, BigInteger, BigInteger> operator) {
        BigInteger secondOperand = (BigInteger) accumulator.pop();
        BigInteger firstOperand = (BigInteger) accumulator.pop();
        accumulator.push(operator.apply(firstOperand, secondOperand));
    }

}
