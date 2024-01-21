package oa2.task_14;

import java.io.Serializable;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;


interface Summable<T> {
    T sum(T that);
}

class Vector<T extends General & Summable<T>> extends General implements Summable<Vector<T>> {

    private final List<T> elements;

    public Vector(List<T> elements) {
        this.elements = elements;
    }

    public T get(int index) {
        return elements.get(index);
    }

    public int getSize() {
        return elements.size();
    }

    @Override
    public Vector<T> sum(Vector<T> that) {
        if (this.getSize() != that.getSize()) {
            return null;
        }

        List<T> resultElements = IntStream.range(0, this.elements.size())
                .mapToObj(i -> this.elements.get(i).sum(that.elements.get(i)))
                .collect(Collectors.toList());

        return new Vector<>(resultElements);
    }
}

class General implements Serializable {
    // ...
}

class Amount extends General implements Summable<Amount> {
    private final int value;

    public Amount(int value) {
        this.value = value;
    }

    public int getValue() {
        return value;
    }

    @Override
    public Amount sum(Amount that) {
        return new Amount(this.getValue() + that.getValue());
    }
}

public class Test {

    public static void main(String[] args) {
        // Создаем объекты типа A
        Amount a1 = new Amount(100);
        Amount a2 = new Amount(10);

        // Создаем векторы самого нижнего уровня
        Vector<Amount> vectorA1 = new Vector<>(List.of(a1));
        Vector<Amount> vectorA2 = new Vector<>(List.of(a2));

        // "Упаковываем" в векторы следующего уровня
        Vector<Vector<Amount>> vectorVectorA1 = new Vector<>(List.of(vectorA1));
        Vector<Vector<Amount>> vectorVectorA2 = new Vector<>(List.of(vectorA2));

        // "Упаковываем" векторы векторов в самые верхние векторы
        Vector<Vector<Vector<Amount>>> vectorVectorVectorA1 = new Vector<>(List.of(vectorVectorA1));
        Vector<Vector<Vector<Amount>>> vectorVectorVectorA2 = new Vector<>(List.of(vectorVectorA2));

        Vector<Vector<Vector<Amount>>> result = vectorVectorVectorA1.sum(vectorVectorVectorA2);
    }
}

