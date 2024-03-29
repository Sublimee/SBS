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
        Assertions.assertArrayEquals(new int[]{0, 1}, summarize(arg1, arg2));
    }

    @Test
    @DisplayName("должен сложить 2 числа с одним разрядом без переноса")
    void summarizeArrays2Test() {
        int[] arg1 = new int[]{7};
        int[] arg2 = new int[]{2};
        Assertions.assertArrayEquals(new int[]{0, 9}, summarize(arg1, arg2));
    }

    @Test
    @DisplayName("должен сложить двухразрядные числа без переноса")
    void summarizeArrays3Test() {
        int[] arg1 = new int[]{7, 1};
        int[] arg2 = new int[]{2, 3};
        Assertions.assertArrayEquals(new int[]{0, 9, 4}, summarize(arg1, arg2));
    }

    @Test
    @DisplayName("должен сложить двухразрядное число с одноразрядным без переноса")
    void summarizeArrays4Test() {
        int[] arg1 = new int[]{1, 2};
        int[] arg2 = new int[]{3};
        Assertions.assertArrayEquals(new int[]{0, 1, 5}, summarize(arg1, arg2));
    }

    @Test
    @DisplayName("должен сложить двухразрядное число с одноразрядным c переносом")
    void summarizeArrays5Test() {
        int[] arg1 = new int[]{1, 2};
        int[] arg2 = new int[]{9};
        Assertions.assertArrayEquals(new int[]{0, 2, 1}, summarize(arg1, arg2));
    }

    @Test
    @DisplayName("должен сложить двухразрядное число с двухразрядным c переносом")
    void summarizeArrays6Test() {
        int[] arg1 = new int[]{1, 9};
        int[] arg2 = new int[]{1, 8};
        Assertions.assertArrayEquals(new int[]{0, 3, 7}, summarize(arg1, arg2));
    }

    @Test
    @DisplayName("должен сложить двухразрядное число с двухразрядным c двумя переносами")
    void summarizeArrays7Test() {
        int[] arg1 = new int[]{9, 9};
        int[] arg2 = new int[]{9, 9};
        Assertions.assertArrayEquals(new int[]{1, 9, 8}, summarize(arg1, arg2));
    }

    @Test
    @DisplayName("должен сложить два числа с отличающимся количеством разрядов с переносами через несколько позиций")
    void summarizeArrays8Test() {
        int[] arg2 = new int[]{9, 9, 9, 9};
        int[] arg1 = new int[]{9, 9};
        Assertions.assertArrayEquals(new int[]{1, 0, 0, 9, 8}, summarize(arg1, arg2));
    }
}