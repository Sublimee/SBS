package strong.ideas.lesson_6.task_2;

/**
 * Выполните поразрядное сложение неотрицательных чисел, представленных в виде массивов. В качестве результата должен
 * быть массив. Результат может содержать лидирующие нули, слагаемые -- нет. Слагаемые передаются в порядке убывания
 * значений и содержат хотя бы 1 разряд.
 */

public class Example {

    public static int[] summarize(int[] arg1, int[] arg2) {
        int[] result = new int[arg1.length];

        for (int i = 0; i < arg1.length; i++) {
            result[i] = arg1[i] + arg2[i];
        }

        return result;
    }
}
