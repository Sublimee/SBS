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

}