package greedy.best_time_to_buy_and_sell_stock;

class Solution {
    public int singleNumber(int[] nums) {
        int result = 0;
        for (int num: nums){
            result = result ^ num;
        }
        return result;
    }
}
