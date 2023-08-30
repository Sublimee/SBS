package strong.ideas.lesson_6.task_2;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import static strong.ideas.lesson_6.task_2.Example.summarize;

public class ExampleTest {

    @Test
    void summarizeArraysTest() {
        int[] arg1 = new int[]{};
        int[] arg2 = new int[]{};
        Assertions.assertNull(summarize(arg1, arg2));
    }
}