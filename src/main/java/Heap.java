import java.util.*;
import java.util.stream.IntStream;

class Heap {
    public int[] HeapArray; // хранит неотрицательные числа-ключи

    public Heap() {
        HeapArray = null;
    }

    public void MakeHeap(int[] a, int depth) {
        if (a == null || depth < 0) {
            return;
        }

        int heapArrayLength = (int) Math.pow(2, depth + 1) - 1;
        if (a.length > heapArrayLength) {
            return;
        }

        HeapArray = new int[heapArrayLength];
        Arrays.fill(HeapArray, -1);

        Arrays.stream(a).forEach(this::Add);
    }

    public int GetMax() {
        if (HeapArray == null || HeapArray.length == 0) {
            return -1;
        }

        int head = HeapArray[0];
        if (head == -1) {
            return -1;
        }

        int lastFilledIndex = getLastFilledIndex();

        if (lastFilledIndex == 0) {
            HeapArray[0] = -1;
            return head;
        }

        HeapArray[0] = HeapArray[lastFilledIndex];
        HeapArray[lastFilledIndex] = -1;

        int elementIndex = 0;
        int leftIndex = elementIndex * 2 + 1;
        int rightIndex = elementIndex * 2 + 2;

        int element = HeapArray[0];
        int left = HeapArray[leftIndex];
        int right = HeapArray[rightIndex];

        while (element < left || element < right) {
            if (left > right && left > element) {
                int temp = HeapArray[elementIndex];
                HeapArray[elementIndex] = left;
                HeapArray[leftIndex] = temp;

                elementIndex = leftIndex;
                leftIndex = elementIndex * 2 + 1;
                rightIndex = elementIndex * 2 + 2;
            } else if (right > left && right > element) {
                int temp = HeapArray[elementIndex];
                HeapArray[elementIndex] = right;
                HeapArray[rightIndex] = temp;

                elementIndex = rightIndex;
                leftIndex = elementIndex * 2 + 1;
                rightIndex = elementIndex * 2 + 2;
            }

            if (leftIndex > HeapArray.length || rightIndex > HeapArray.length) {
                return head;
            }
            left = HeapArray[leftIndex];
            right = HeapArray[rightIndex];
        }

        return head;
    }

    private int getLastFilledIndex() {
        return IntStream.range(0, HeapArray.length)
                .filter(i -> HeapArray[i] == -1)
                .findFirst()
                .orElse(HeapArray.length) - 1;
    }

    public boolean Add(int key) {
        int vacantIndex = getVacantIndex();

        if (vacantIndex == -1) {
            return false;
        }

        HeapArray[vacantIndex] = key;

        int parentIndex = getParentIndex(vacantIndex);
        while (parentIndex >= 0 && HeapArray[parentIndex] < key) {
            HeapArray[vacantIndex] = HeapArray[parentIndex];
            HeapArray[parentIndex] = key;

            vacantIndex = parentIndex;
            parentIndex = getParentIndex(vacantIndex);
        }

        return true;
    }

    private int getVacantIndex() {
        return IntStream.range(0, HeapArray.length)
                .filter(i -> HeapArray[i] == -1)
                .findFirst()
                .orElse(-1);
    }

    private int getParentIndex(int vacantIndex) {
        if (vacantIndex == -1 || vacantIndex == 0) {
            return -1;
        }
        if (vacantIndex % 2 == 0) {
            vacantIndex -= 2;
        }
        return vacantIndex / 2;
    }
}