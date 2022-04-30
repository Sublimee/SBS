package lesson09;

import org.example.lesson09.NativeDictionary;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.stream.IntStream;

public class NativeDictionaryTest {

    @Test
    public void hashFunTest() {
        int size = 4;
        NativeDictionary<String> map = new NativeDictionary<>(size, String.class);
        IntStream.range(1, 10)
                .boxed()
                .forEach(x -> Assertions.assertEquals(x % size, map.hashFun(String.valueOf(x))));
    }

    @Test
    public void hashFunBigValueTest() {
        int size = 4;
        NativeDictionary<String> map = new NativeDictionary<>(size, String.class);
        Assertions.assertEquals(3, map.hashFun("10000000000"));
    }

    @Test
    public void hashFunNullValueTest() {
        int size = 4;
        NativeDictionary<String> map = new NativeDictionary<>(size, String.class);
        Assertions.assertEquals(-1, map.hashFun(null));
    }

    @Test
    public void putTest() {
        int size = 4;
        NativeDictionary<String> map = new NativeDictionary<>(size, String.class);
        map.put("1", "10");
        Assertions.assertEquals("10", map.get("1"));
    }

    @Test
    public void putCollisionVaryKeyTest() {
        int size = 4;
        NativeDictionary<String> map = new NativeDictionary<>(size, String.class);
        map.put("1", "10");
        map.put("5", "50");
        map.put("9", "90");
        map.put("12", "120");
        Assertions.assertEquals("10", map.get("1"));
        Assertions.assertEquals("50", map.get("5"));
        Assertions.assertEquals("90", map.get("9"));
        Assertions.assertEquals("120", map.get("12"));
    }

    @Test
    public void putCollisionSameKeyTest() {
        int size = 4;
        NativeDictionary<String> map = new NativeDictionary<>(size, String.class);
        map.put("1", "10");
        map.put("1", "50");
        Assertions.assertEquals("50", map.get("1"));
    }

    @Test
    public void putWithoutCollisionTest() {
        int size = 4;
        NativeDictionary<String> map = new NativeDictionary<>(size, String.class);
        map.put("1", "10");
        map.put("2", "20");
        map.put("3", "30");
        map.put("4", "40");
        Assertions.assertEquals("10", map.get("1"));
        Assertions.assertEquals("20", map.get("2"));
        Assertions.assertEquals("30", map.get("3"));
        Assertions.assertEquals("40", map.get("4"));
    }

    @Test
    public void findTest() {
        int size = 4;
        NativeDictionary<String> map = new NativeDictionary<>(size, String.class);
        map.put("5", "50");
        Assertions.assertTrue(map.isKey("5"));
    }

    @Test
    public void findEmptyTest() {
        int size = 4;
        NativeDictionary<String> map = new NativeDictionary<>(size, String.class);
        Assertions.assertFalse(map.isKey("1"));
    }

    @Test
    public void findWithCollisionKeyTest() {
        int size = 4;
        NativeDictionary<String> map = new NativeDictionary<>(size, String.class);
        map.put("5", "50");
        Assertions.assertFalse(map.isKey("1"));
    }
}
