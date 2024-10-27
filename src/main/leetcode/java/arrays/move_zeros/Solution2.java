package arrays.move_zeros;


class Solution2 {
    public static void moveZeroes(int[] nums) {
        int lastNonNegativeIndex = 0;
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] != 0) {
                nums[lastNonNegativeIndex] = nums[i];
                lastNonNegativeIndex++;
            }
        }

        for (int i = lastNonNegativeIndex; i < nums.length; i++) {
            nums[i] = 0;
        }
    }
}

