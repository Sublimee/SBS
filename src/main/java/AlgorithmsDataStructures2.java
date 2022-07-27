import java.util.*;

public class AlgorithmsDataStructures2 {
    public static int[] GenerateBBSTArray(int[] a) {
        if (a == null) {
            return null;
        }

        int[] result = new int[a.length];

        if (a.length == 0){
            return result;
        }

        Arrays.sort(a);
        GenerateBBSTArray(a, 0, result);
        return result;
    }

    public static void GenerateBBSTArray(int[] a, int i, int[] result) {
        int aLength = a.length;
        int middle = aLength / 2;

        result[i] = a[middle];

        if (aLength != 1) {
            GenerateBBSTArray(Arrays.copyOfRange(a, 0, middle), i * 2 + 1, result);
            GenerateBBSTArray(Arrays.copyOfRange(a, middle + 1, aLength), i * 2 + 2, result);
        }
    }
}