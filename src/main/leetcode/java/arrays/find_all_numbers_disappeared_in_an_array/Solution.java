package arrays.find_all_numbers_disappeared_in_an_array;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class Solution {
    public List<Integer> findDisappearedNumbers(int[] nums) {
        Arrays.sort(nums);
        List<Integer> result = new ArrayList<>();
        int j = 1;
        for (int i = 0; i < nums.length; i++) {
            if (j < nums[i]) {          // нашли очередной пробел
                result.add(j);          // добавили в результат

                // для сокращения разрыва... 4 7
                j++;
                // ...топчемся на месте
                i--;
            } else if (j == nums[i]) {
                j++;
            }
        }
        while (j <= nums.length) {
            result.add(j);
            j++;
        }
        return result;
    }
}