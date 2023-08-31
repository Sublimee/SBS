package strong.ideas.lesson_6.task_2;

/**
 * Выполните поразрядное сложение неотрицательных чисел, представленных в виде массивов. В качестве результата должен
 * быть массив. Результат может содержать лидирующие нули, слагаемые -- нет. Слагаемые передаются в порядке убывания
 * значений и содержат хотя бы 1 разряд.
 */

public class Example {

    public static int[] summarize(int[] arg1, int[] arg2) {
        int length1 = arg1.length;
        int length2 = arg2.length;

        int resultLength = Math.max(length1, length2) + 1;
        int[] result = new int[resultLength];

        int carry = 0;
        for (int i = 0; i < result.length; i++) {
            int digit1 = i < length1 ? arg1[length1 - 1 - i] : 0;
            int digit2 = i < length2 ? arg2[length2 - 1 - i] : 0;

            int digitsSum = digit1 + digit2 + carry;
            carry = digitsSum / 10;
            result[result.length - 1 - i] = digitsSum % 10;
        }

        return result;
    }
}
