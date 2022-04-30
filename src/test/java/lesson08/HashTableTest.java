package lesson08;

import org.example.lesson08.HashTable;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class HashTableTest {

    @Test
    public void hashFunTest() {
        int size = 4;
        HashTable hashTable = new HashTable(size, 1);
        IntStream.range(1, 10)
                .boxed()
                .forEach(x -> {
                            System.out.println(x);
                            Assertions.assertEquals(x % size, hashTable.hashFun(String.valueOf(x)));
                        }
                );
    }

    @Test
    public void hashFunBigValueTest() {
        int size = 4;
        HashTable hashTable = new HashTable(size, 1);
        Assertions.assertEquals(3, hashTable.hashFun("10000000000"));
    }

    @Test
    public void putVaryWithSameHashAndEvenSizeOddStepTest() {
        int size = 4;
        HashTable hashTable = new HashTable(size, 1);
        Stream.of(1, 5, 9, 12, 16).forEach(x -> hashTable.put(String.valueOf(x)));
        Assertions.assertArrayEquals(Arrays.asList("12", "1", "5", "9").toArray(), hashTable.slots);
    }

    @Test
    public void putVaryWithSameHashAndEvenSizeEvenStepTest() {
        int size = 4;
        HashTable hashTable = new HashTable(size, 2);
        Stream.of(1, 5, 9, 12, 16).forEach(x -> hashTable.put(String.valueOf(x)));
        Assertions.assertArrayEquals(Arrays.asList(null, "1", null, "5").toArray(), hashTable.slots);
    }

    @Test
    public void putVaryWithSameHashAndOddSizeOddStepTest() {
        int size = 5;
        HashTable hashTable = new HashTable(size, 1);
        Stream.of(1, 6, 12, 17, 21, 26).forEach(x -> hashTable.put(String.valueOf(x)));
        Assertions.assertArrayEquals(Arrays.asList("6", "12", "17", "21", "1").toArray(), hashTable.slots);
    }

    @Test
    public void putVaryWithSameHashAndOddSizeEvenStepTest() {
        int size = 5;
        HashTable hashTable = new HashTable(size, 2);
        Stream.of(1, 6, 12, 17, 21, 26).forEach(x -> hashTable.put(String.valueOf(x)));
        Assertions.assertArrayEquals(Arrays.asList("17", "6", "21", "12", "1").toArray(), hashTable.slots);
    }

    @Test
    public void putSameTest() {
        int size = 4;
        HashTable hashTable = new HashTable(size, 1);
        Stream.of(1, 1).forEach(x -> hashTable.put(String.valueOf(x)));
        Assertions.assertArrayEquals(Arrays.asList(null, "1", null, null).toArray(), hashTable.slots);
    }

    @Test
    public void putEvenSizeOddStepVaryTest() {
        int size = 4;
        HashTable hashTable = new HashTable(size, 1);
        IntStream.range(1, 2 * size + 1)
                .boxed()
                .forEach(x -> hashTable.put(String.valueOf(x)));
        Assertions.assertArrayEquals(Arrays.asList("4", "1", "2", "3").toArray(), hashTable.slots);
    }

    @Test
    public void putEvenSizeEvenStepVaryTest() {
        int size = 4;
        HashTable hashTable = new HashTable(size, 2);
        IntStream.range(1, 2 * size + 1)
                .boxed()
                .forEach(x -> hashTable.put(String.valueOf(x)));
        Assertions.assertArrayEquals(Arrays.asList("4", "1", "2", "3").toArray(), hashTable.slots);
    }

    @Test
    public void putOddSizeOddStepVaryTest() {
        int size = 5;
        HashTable hashTable = new HashTable(size, 1);
        IntStream.range(1, 2 * size + 1)
                .boxed()
                .forEach(x -> hashTable.put(String.valueOf(x)));
        Assertions.assertArrayEquals(Arrays.asList("2", "3", "4", "5", "1").toArray(), hashTable.slots);
    }

    @Test
    public void putOddSizeEvenStepVaryTest() {
        int size = 5;
        HashTable hashTable = new HashTable(size, 2);
        IntStream.range(1, 2 * size + 1)
                .boxed()
                .forEach(x -> hashTable.put(String.valueOf(x)));
        Assertions.assertArrayEquals(Arrays.asList("2", "3", "4", "5", "1").toArray(), hashTable.slots);
    }

    @Test
    public void findTest() {
        int size = 4;
        HashTable hashTable = new HashTable(size, 1);
        Stream.of(1, 5, 9, 12, 16).forEach(x -> hashTable.put(String.valueOf(x)));
        AtomicInteger i = new AtomicInteger(-2);
        Stream.of(16, 12, 1, 5, 9).forEach(x -> Assertions.assertEquals(i.incrementAndGet() % 4, hashTable.find(String.valueOf(x))));
    }

    @Test
    public void findEmptyTest() {
        HashTable hashTable = new HashTable(4, 1);
        Assertions.assertEquals(-1, hashTable.find("1"));
    }
}
