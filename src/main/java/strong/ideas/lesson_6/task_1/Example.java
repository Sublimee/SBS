package strong.ideas.lesson_6.task_1;

// Найдите самую длинную строго возрастающую или строго убывающую последовательность чисел в массиве (в ответе требуется
// вернуть 2 индекса -- границы диапазона). Гарантируется, что хотя бы одна такая последовательность есть. Если
// последовательностей несколько, то требуется в качестве результата вернуть первую из них.
public class Example {

    public static Range processArray(int[] array) {
        int indexFrom = 0;
        int indexTo = 0;

        // true  -> исследуемая подпоследовательность строго возрастающая
        // false -> исследуемая подпоследовательность строго убывающая
        // null  -> исследуемая подпоследовательность не относится к ранее описанным
        Boolean subSequenceDirection = null;

        int subSequenceIndexFrom = 0;
        int subSequenceIndexTo = 0;

        // Так как наличие искомой последовательности гарантируется контрактом, то в массиве есть хотя бы 2 элемента.
        for (int i = 1; i < array.length; i++) {
            Boolean currentDirection = null;
            if (array[i] > array[i - 1]) {
                currentDirection = true;
            }

            if (currentDirection != subSequenceDirection && currentDirection == true) {
                subSequenceIndexFrom = array[i - 1];
                subSequenceIndexTo = array[i];
            }

            if ((subSequenceIndexTo - subSequenceIndexFrom) > (indexTo - indexFrom)) {
                indexFrom = subSequenceIndexFrom;
                indexTo = subSequenceIndexTo;
            }
        }

        return new Range(indexFrom, indexTo);
    }
}