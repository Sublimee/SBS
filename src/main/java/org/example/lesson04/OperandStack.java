package org.example.lesson04;

import java.util.*;

public class OperandStack {

    public Integer process(List<Object> sequence) {
        Stack<Object> stack1 = new Stack<>();
        Stack<Object> stack2 = new Stack<>();

        for (int i = sequence.size() - 1; i >= 0; i--) {
            stack1.push(sequence.get(i));
        }

        Object value;
        while ((value = stack1.pop()) != null) {
            if (value instanceof Number) {
                stack2.push(value);
            } else {
                switch ((String) value) {
                    case "+" -> stack2.push(((Integer) stack2.pop()) + ((Integer) stack2.pop()));
                    case "*" -> stack2.push(((Integer) stack2.pop()) * ((Integer) stack2.pop()));
                    case "=" -> {
                        return (Integer) stack2.pop();
                    }
                }
            }
        }
        return null;
    }
}
