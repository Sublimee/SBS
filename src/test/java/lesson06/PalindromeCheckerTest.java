package lesson06;

import org.example.algo01.lesson06.PalindromeChecker;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class PalindromeCheckerTest {

    @Test
    public void checkNullTest() {
        PalindromeChecker checker = new PalindromeChecker();
        Assertions.assertFalse(checker.check(null));
    }

    @Test
    public void checkSingleTest() {
        PalindromeChecker checker = new PalindromeChecker();
        Assertions.assertTrue(checker.check("1"));
    }

    @Test
    public void checkPalindromePairTest() {
        PalindromeChecker checker = new PalindromeChecker();
        Assertions.assertTrue(checker.check("11"));
    }

    @Test
    public void checkNotPalindromePairTest() {
        PalindromeChecker checker = new PalindromeChecker();
        Assertions.assertFalse(checker.check("21"));
    }

    @Test
    public void checkPalindromeTripleTest() {
        PalindromeChecker checker = new PalindromeChecker();
        Assertions.assertTrue(checker.check("131"));
    }

    @Test
    public void checkNotPalindromeTripleTest() {
        PalindromeChecker checker = new PalindromeChecker();
        Assertions.assertFalse(checker.check("132"));
    }

    @Test
    public void checkPalindromeTest() {
        PalindromeChecker checker = new PalindromeChecker();
        Assertions.assertTrue(checker.check("2332"));
    }

    @Test
    public void checkNotPalindromeTest() {
        PalindromeChecker checker = new PalindromeChecker();
        Assertions.assertFalse(checker.check("23142"));
    }
}
