package strong.ideas.lesson_6.task_2;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static strong.ideas.lesson_6.task_2.Example.summarize;

public class ExampleTest {

    @Test
    @DisplayName("должен сложить число из 1 разряда с нулём")
    void summarizeArrays1Test() {
        int[] arg1 = new int[]{1};
        int[] arg2 = new int[]{0};
        Assertions.assertArrayEquals(new int[]{1}, summarize(arg1, arg2));
    }
}