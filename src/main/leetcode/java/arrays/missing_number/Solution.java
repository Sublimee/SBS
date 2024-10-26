package arrays.missing_number;

class Solution {
    public int missingNumber(int[] nums) {
        int realSum = 0;
        for (int i : nums) {
            realSum += i;
        }
        int calculatedSum = (nums.length * (nums.length + 1)) / 2;

        return calculatedSum - realSum;
    }
}