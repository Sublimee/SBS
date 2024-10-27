package arrays.move_zeros;

public class Solution1 {
    public static void moveZeroes(int[] nums) {
        int n = nums.length;
        for (int i = 0; i < n; i++) {
            if (nums[i] == 0) {
                // Найден нулевой элемент, смещаем оставшиеся элементы на 1 позицию влево
                System.arraycopy(nums, i + 1, nums, i, n - i - 1);
                // Помещаем 0 в конец массива
                nums[n - 1] = 0;
                // Уменьшаем n для предотвращения повторного сдвига уже перемещённых нулей
                n--;
                // Откатываем указатель i на одну позицию назад, чтобы проверить текущий элемент
                i--;
            }
        }
    }
}
