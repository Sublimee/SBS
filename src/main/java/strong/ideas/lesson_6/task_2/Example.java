package strong.ideas.lesson_6.task_2;

/**
 * Выполните поразрядное сложение неотрицательных чисел, представленных в виде массивов. В качестве результата должен
 * быть массив. Результат может содержать лидирующие нули, слагаемые -- нет. Слагаемые передаются в порядке убывания
 * значений и содержат хотя бы 1 разряд.
 */

public class Example {

    public static int[] summarize(int[] arg1, int[] arg2) {
        int[] result = new int[arg1.length + 1];

        int carry = 0;
        for (int i = 0; i < arg1.length; i++) {
            int arg1Index = arg1.length - 1 - i;
            int arg2Index = arg2.length - 1 - i;
            int resultIndex = result.length - 1 - i;

            int digitsSum = arg1[arg1Index] + carry;
            if (arg2Index >= 0) {
                digitsSum = digitsSum + arg2[arg2Index];
            }
            carry = digitsSum / 10;
            result[resultIndex] = digitsSum % 10;
        }

        if (carry != 0) {
            result[0] = result[0] + carry;
        }

        return result;
    }
}
