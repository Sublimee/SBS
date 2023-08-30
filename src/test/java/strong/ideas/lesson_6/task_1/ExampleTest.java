package strong.ideas.lesson_6.task_1;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static strong.ideas.lesson_6.task_1.Example.processArray;

public class ExampleTest {

    @Test
    @DisplayName("должен вернуть строго возрастающую последовательность в массиве из двух элементов")
    void processArray1Test() {
        int[] example = new int[]{1, 2};
        Assertions.assertEquals(new Range(0, 1), processArray(example));
    }

    @Test
    @DisplayName("должен вернуть строго возрастающую последовательность из 3 элементов в массиве из трех элементов")
    void processArray2Test() {
        int[] example = new int[]{1, 2, 3};
        Assertions.assertEquals(new Range(0, 2), processArray(example));
    }

    @Test
    @DisplayName("должен вернуть строго возрастающую последовательность, которая обрамлена значениями, не входящими в другие последовательности")
    void processArray3Test() {
        int[] example = new int[]{1, 1, 2, 3, 3};
        Assertions.assertEquals(new Range(1, 3), processArray(example));
    }

    @Test
    @DisplayName("должен вернуть строго убывающую последовательность в массиве из двух элементов")
    void processArray4Test() {
        int[] example = new int[]{2, 1};
        Assertions.assertEquals(new Range(0, 1), processArray(example));
    }

    @Test
    @DisplayName("должен вернуть строго убывающую последовательность из 3 элементов в массиве из трех элементов")
    void processArray5Test() {
        int[] example = new int[]{3, 2, 1};
        Assertions.assertEquals(new Range(0, 2), processArray(example));
    }
}