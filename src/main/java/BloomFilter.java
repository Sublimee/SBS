public class BloomFilter {
    public int filter_len;
    public int bitArray;

    public BloomFilter(int f_len) {
        filter_len = f_len;
        bitArray = 0;
    }

    public int hash1(String str1) {
        return hash(str1, 17);
    }

    public int hash2(String str1) {
        return hash(str1, 223);
    }

    private int hash(String str1, int random) {
        int result = 0;
        for (int i = 0; i < str1.length(); i++) {
            result = (result * random + str1.charAt(i)) % filter_len;
        }
        return result;
    }

    public void add(String str1) {
        updateBitArray(hash1(str1));
        updateBitArray(hash2(str1));
    }

    private void updateBitArray(int bit) {
        bitArray |= 1 << bit;
    }

    public boolean isValue(String str1) {
        return checkBit(bitArray, hash1(str1)) && checkBit(bitArray, hash2(str1));
    }

    private boolean checkBit(int bitArray, int bit) {
        return (bitArray >> bit & 1) == 1;
    }
}
