import org.example.lesson04.BracketValidator;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class BracketValidatorTest {

    private final BracketValidator bracketValidator = new BracketValidator();

    @Test
    void bracketValidator1() {
        Assertions.assertTrue(bracketValidator.validate("(()((())()))"));
    }

    @Test
    void bracketValidator2() {
        Assertions.assertFalse(bracketValidator.validate( "(()()(()"));
    }

    @Test
    void bracketValidator3() {
        Assertions.assertFalse(bracketValidator.validate("())("));
    }

    @Test
    void bracketValidator4() {
        Assertions.assertFalse(bracketValidator.validate("))(("));
    }

    @Test
    void bracketValidator5() {
        Assertions.assertFalse(bracketValidator.validate("((())"));
    }

    @Test
    void bracketValidator6() {
        Assertions.assertTrue(bracketValidator.validate("()()()"));
    }
}
