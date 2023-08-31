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
            int resultIndex = arg1.length - 1 - i;
            int secondArgumentIndex = arg2.length - 1 - i;

            if (secondArgumentIndex >= 0) {
                result[resultIndex] = arg1[resultIndex] + arg2[secondArgumentIndex];
            } else {
                result[resultIndex] = arg1[resultIndex];
            }
        }

        return result;
    }
}
