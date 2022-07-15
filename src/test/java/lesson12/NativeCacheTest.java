package lesson12;

import org.example.algo.lesson12.NativeCache;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.stream.IntStream;

public class NativeCacheTest {

    @Test
    public void hashFunTest() {
        int size = 4;
        NativeCache<String> cache = new NativeCache<>(size, String.class);
        IntStream.range(1, 10)
                .boxed()
                .forEach(x -> Assertions.assertEquals(x % size, cache.hashFun(String.valueOf(x))));
    }

    @Test
    public void hashFunBigValueTest() {
        int size = 4;
        NativeCache<String> cache = new NativeCache<>(size, String.class);
        Assertions.assertEquals(3, cache.hashFun("10000000000"));
    }

    @Test
    public void hashFunNullValueTest() {
        int size = 4;
        NativeCache<String> cache = new NativeCache<>(size, String.class);
        Assertions.assertEquals(-1, cache.hashFun(null));
    }

    @Test
    public void singlePutAndSingleGetTest() {
        int size = 4;
        NativeCache<String> cache = new NativeCache<>(size, String.class);
        cache.put("1", "10");
        Assertions.assertEquals("10", cache.get("1"));
        Assertions.assertEquals(1, cache.hits[1]);
    }

    @Test
    public void singlePutAndManyGetTest() {
        int size = 4;
        NativeCache<String> cache = new NativeCache<>(size, String.class);
        cache.put("1", "10");
        IntStream.range(1, 11).forEach(x -> cache.get("1"));
        Assertions.assertEquals(10, cache.hits[1]);
    }

    @Test
    public void manyPutAndSingleGetTest() {
        int size = 4;
        NativeCache<String> cache = new NativeCache<>(size, String.class);
        cache.put("1", "10");
        cache.put("1", "10");
        cache.put("1", "10");
        Assertions.assertEquals("10", cache.get("1"));
        Assertions.assertEquals(1, cache.hits[1]);
    }

    @Test
    public void putCollisionVaryKeyTest() {
        int size = 4;
        NativeCache<String> cache = new NativeCache<>(size, String.class);
        cache.put("1", "10");
        cache.put("5", "50");
        cache.put("9", "90");
        cache.put("12", "120");
        Assertions.assertEquals("10", cache.get("1"));
        Assertions.assertEquals("50", cache.get("5"));
        Assertions.assertEquals("90", cache.get("9"));
        Assertions.assertEquals("120", cache.get("12"));
        IntStream.range(1, 4).forEach(x -> Assertions.assertEquals(1, cache.hits[x]));
    }

    @Test
    public void putCollisionVaryKeyAndHitsTest() {
        int size = 4;
        NativeCache<String> cache = new NativeCache<>(size, String.class);
        cache.put("1", "10");
        cache.put("5", "50");
        cache.put("9", "90");
        cache.put("12", "120");
        IntStream.range(1, 3).forEach(x -> cache.get("1"));
        IntStream.range(1, 3).forEach(x -> cache.get("5"));
        IntStream.range(1, 3).forEach(x -> cache.get("9"));
        IntStream.range(1, 3).forEach(x -> cache.get("12"));
        cache.put("16", "160");
        IntStream.range(1, 5).forEach(x -> cache.get("1"));
        IntStream.range(1, 3).forEach(x -> cache.get("5"));
        IntStream.range(1, 4).forEach(x -> cache.get("9"));
        IntStream.range(1, 10).forEach(x -> cache.get("16"));
        cache.put("21", "210");
        Assertions.assertArrayEquals(new String[]{"16", "1", "21", "9"}, cache.slots);
        Assertions.assertArrayEquals(new String[]{"160", "10", "210", "90"}, cache.values);
        Assertions.assertArrayEquals(new int[]{9, 6, 0, 5}, cache.hits);
    }

    @Test
    public void putCollisionSameKeyTest() {
        int size = 4;
        NativeCache<String> cache = new NativeCache<>(size, String.class);
        cache.put("1", "10");
        Assertions.assertEquals("10", cache.get("1"));
        cache.put("1", "50");
        Assertions.assertEquals("50", cache.get("1"));
        Assertions.assertEquals(2, cache.hits[1]);
    }

    @Test
    public void putWithoutCollisionTest() {
        int size = 4;
        NativeCache<String> cache = new NativeCache<>(size, String.class);
        cache.put("1", "10");
        cache.put("2", "20");
        cache.put("3", "30");
        cache.put("4", "40");
        Assertions.assertEquals("10", cache.get("1"));
        Assertions.assertEquals("20", cache.get("2"));
        Assertions.assertEquals("30", cache.get("3"));
        Assertions.assertEquals("40", cache.get("4"));
        IntStream.range(1, 4).forEach(x -> Assertions.assertEquals(1, cache.hits[x]));
    }

    @Test
    public void findTest() {
        int size = 4;
        NativeCache<String> cache = new NativeCache<>(size, String.class);
        cache.put("5", "50");
        Assertions.assertTrue(cache.isKey("5"));
    }

    @Test
    public void findEmptyTest() {
        int size = 4;
        NativeCache<String> cache = new NativeCache<>(size, String.class);
        Assertions.assertFalse(cache.isKey("1"));
    }

    @Test
    public void findWithCollisionKeyTest() {
        int size = 4;
        NativeCache<String> cache = new NativeCache<>(size, String.class);
        cache.put("5", "50");
        Assertions.assertFalse(cache.isKey("1"));
    }
}
