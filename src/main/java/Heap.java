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
        int lastFilledIndex = getLastFilledIndex();

        if (lastFilledIndex == -1) {
            return -1;
        }

        if (lastFilledIndex == 0) {
            HeapArray[lastFilledIndex] = -1;
            return head;
        }

        HeapArray[0] = HeapArray[lastFilledIndex];
        HeapArray[lastFilledIndex] = -1;

        int elementIndex = 0;
        int leftIndex = 1;
        int rightIndex = 2;

        while (HeapArray[elementIndex] < HeapArray[leftIndex] || HeapArray[elementIndex] < HeapArray[rightIndex]) {
            if (HeapArray[leftIndex] > HeapArray[rightIndex]) {
                swap(elementIndex, leftIndex);

                elementIndex = leftIndex;
            } else {
                swap(elementIndex, rightIndex);

                elementIndex = rightIndex;
            }

            leftIndex = elementIndex * 2 + 1;
            rightIndex = elementIndex * 2 + 2;

            if (rightIndex >= HeapArray.length) {
                return head;
            }
        }

        return head;
    }

    private void swap(int index, int otherIndex) {
        int temp = HeapArray[index];
        HeapArray[index] = HeapArray[otherIndex];
        HeapArray[otherIndex] = temp;
    }

    private int getLastFilledIndex() {
        return IntStream.range(0, HeapArray.length)
                .filter(i -> HeapArray[i] == -1)
                .findFirst()
                .orElse(HeapArray.length) - 1;
    }

    public boolean Add(int key) {
        if (key < 0) {
            return false;
        }

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