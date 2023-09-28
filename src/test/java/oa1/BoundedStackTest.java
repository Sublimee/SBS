package oa1;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

public class BoundedStackTest {

    private static final int CAPACITY = 3;
    private BoundedStack<Integer> boundedStack;

    @BeforeEach
    public void setUp() {
        boundedStack = new BoundedStack<>(CAPACITY);
    }

    @Test
    public void testDefaultConstructor() {
        BoundedStack<Integer> boundedStack = new BoundedStack<>();

        assertEquals(0, boundedStack.size());
        assertEquals(32, boundedStack.capacity());
    }

    @Test
    public void testParametrizedConstructor() {
        BoundedStack<Integer> boundedStack = new BoundedStack<>(CAPACITY);

        assertEquals(0, boundedStack.size());
        assertEquals(CAPACITY, boundedStack.capacity());
    }

    @Test
    public void testPushPositive() {
        boundedStack.push(1);
        assertEquals(1, boundedStack.size());
        assertEquals(BoundedStack.PUSH_OK, boundedStack.get_push_status());
    }

    @Test
    public void testPushNegative() {
        boundedStack.push(1);
        boundedStack.push(2);
        boundedStack.push(3);
        boundedStack.push(4);
        assertEquals(3, boundedStack.size());
        assertEquals(BoundedStack.PUSH_ERR, boundedStack.get_push_status());
    }

    @Test
    public void testPopPositive() {
        boundedStack.push(1);
        boundedStack.push(2);
        boundedStack.pop();
        assertEquals(1, boundedStack.size());
        assertEquals(BoundedStack.POP_OK, boundedStack.get_pop_status());
    }

    @Test
    public void testPopNegative() {
        boundedStack.pop();
        assertEquals(0, boundedStack.size());
        assertEquals(BoundedStack.POP_ERR, boundedStack.get_pop_status());
    }

    @Test
    public void testClear() {
        boundedStack.push(1);
        boundedStack.push(2);
        boundedStack.clear();
        assertEquals(0, boundedStack.size());
        assertEquals(CAPACITY, boundedStack.capacity());
        assertEquals(BoundedStack.PUSH_NIL, boundedStack.get_push_status());
        assertEquals(BoundedStack.POP_NIL, boundedStack.get_pop_status());
        assertEquals(BoundedStack.PEEK_NIL, boundedStack.get_peek_status());
    }

    @Test
    public void testPeekPositive() {
        boundedStack.push(1);
        boundedStack.push(2);
        assertEquals(2, (int) boundedStack.peek());
        assertEquals(BoundedStack.PEEK_OK, boundedStack.get_peek_status());
    }

    @Test
    public void testPeekNegative() {
        assertNull(boundedStack.peek());
        assertEquals(BoundedStack.PEEK_ERR, boundedStack.get_peek_status());
    }
}