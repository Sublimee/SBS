package strong.ideas.lesson_6.task_1;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import static strong.ideas.lesson_6.task_1.Example.processArray;

public class ExampleTest {

    @Test
    void processArrayTest() {
        int[] example = new int[]{1, 2};
        Assertions.assertEquals(new Range(1, 2), processArray(example));
    }

}