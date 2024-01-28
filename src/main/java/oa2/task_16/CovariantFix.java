package oa2.task_16;

import java.util.ArrayList;
import java.util.List;

class Expression {
    @Override
    public String toString() {
        return "some expression";
    }
}

class SimpleExpression extends Expression {
    @Override
    public String toString() {
        return "some simple expression";
    }
}

class ComplexExpression extends SimpleExpression {
    @Override
    public String toString() {
        return "some complex expression";
    }
}


class Calculator {
    // В Java не только массивы ковариантны, можно использовать и обобщенные коллекции со следующим типом:
    public <T> void covariantMethod(List<? extends T> values) {
        for (T value : values) {
            System.out.println(value.toString());
        }
    }
}

class EngineeringCalculator extends Calculator {
    @Override
    public <T> void covariantMethod(List<? extends T> values) {
        super.covariantMethod(values);
        System.out.println(values.size());
    }
}

public class CovariantFix {
    public static void main(String[] args) {
        Calculator calculator = new EngineeringCalculator();
        List<Expression> expressions = new ArrayList<>();
        expressions.add(new SimpleExpression());
        expressions.add(new ComplexExpression());

        // пример вызовы ковариантного метода (как видим, ковариантность в Java работает НЕ только для массивов)
        calculator.covariantMethod(expressions);
    }
}