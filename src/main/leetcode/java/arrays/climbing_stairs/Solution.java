package arrays.climbing_stairs;

class Solution {
    public static int climbStairs(int n) {
        return climbStairsTailRecursive(n, 1, 1);
    }

    private static int climbStairsTailRecursive(int n, int a, int b) {
        if (n == 0) {
            return a;
        }
        return climbStairsTailRecursive(n - 1, b, a + b);
    }
}