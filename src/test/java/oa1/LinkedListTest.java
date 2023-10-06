package oa1;

import oa1.two_way_list.LinkedList;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class LinkedListTest {

    private LinkedList<Integer> list;

    @BeforeEach
    public void setUp() {
        list = new LinkedList<>();
    }

    @Test
    public void testHead() {
        list.add_tail(1);
        list.head();
        assertEquals(1, list.get().intValue());
        assertEquals(list.get_head_status(), list.HEAD_OK);
    }

    @Test
    public void testHeadWhenEmpty() {
        list.head();
        assertEquals(list.get_head_status(), list.HEAD_ERR);
    }

    @Test
    public void testTail() {
        list.add_tail(1);
        list.tail();
        assertEquals(1, list.get().intValue());
        assertEquals(list.get_tail_status(), list.TAIL_OK);
    }

    @Test
    public void testTailWhenEmpty() {
        list.tail();
        assertEquals(list.get_tail_status(), list.TAIL_ERR);
    }

    @Test
    public void testRight() {
        list.add_tail(1);
        list.add_tail(2);
        list.head();
        list.right();
        assertEquals(2, list.get().intValue());
        assertEquals(list.get_right_status(), list.RIGHT_OK);
    }

    @Test
    public void testRightWhenAtEnd() {
        list.add_tail(1);
        list.tail();
        list.right();
        assertEquals(list.get_right_status(), list.RIGHT_ERR);
    }

    @Test
    public void testPutRight() {
        list.add_tail(1);
        list.head();
        list.put_right(2);
        list.right();
        assertEquals(2, list.get().intValue());
        assertEquals(list.get_put_right_status(), list.PUT_RIGHT_OK);
    }

    @Test
    public void testPutRightWhenEmpty() {
        list.put_right(1);
        assertEquals(list.get_put_right_status(), list.PUT_RIGHT_ERR);
    }

    @Test
    public void testPutLeft() {
        list.add_tail(1);
        list.head();
        list.put_left(2);
        assertEquals(1, list.get().intValue());
        assertEquals(list.get_put_left_status(), list.PUT_LEFT_OK);
    }

    @Test
    public void testPutLeftWhenEmpty() {
        list.put_left(1);
        assertEquals(list.get_put_left_status(), list.PUT_LEFT_ERR);
    }

    @Test
    public void testRemove() {
        list.add_tail(1);
        list.head();
        list.remove();
        assertEquals(0, list.size());
        assertEquals(list.get_remove_status(), list.REMOVE_OK);
    }

    @Test
    public void testRemoveWhenEmpty() {
        list.remove();
        assertEquals(list.get_remove_status(), list.REMOVE_ERR);
    }

    @Test
    public void testAddTail() {
        list.add_tail(1);
        assertEquals(1, list.size());
    }

    @Test
    public void testReplace() {
        list.add_tail(1);
        list.head();
        list.replace(2);
        assertEquals(2, list.get().intValue());
        assertEquals(list.get_replace_status(), list.REPLACE_OK);
    }

    @Test
    public void testReplaceWhenEmpty() {
        list.replace(1);
        assertEquals(list.get_replace_status(), list.REPLACE_ERR);
    }

    @Test
    public void testFind() {
        list.add_tail(1);
        list.head();
        list.find(1);
        assertEquals(1, list.get().intValue());
        assertEquals(list.get_find_status(), list.FIND_OK);
    }

    @Test
    public void testFindWhenEmpty() {
        list.find(1);
        assertEquals(list.get_find_status(), list.FIND_ERR);
    }

    @Test
    public void testRemoveAll1() {
        list.add_tail(1);
        list.add_tail(1);
        list.add_tail(2);
        list.remove_all(1);
        assertEquals(1, list.size());
    }

    @Test
    public void testRemoveAll2() {
        list.add_tail(2);
        list.add_tail(1);
        list.add_tail(1);
        list.add_tail(2);

        list.remove_all(1);
        assertEquals(2, list.size());
    }

    @Test
    public void testRemoveAll3() {
        list.add_tail(2);
        list.add_tail(1);
        list.add_tail(1);
        list.add_tail(2);
        list.add_tail(1);
        list.add_tail(1);
        list.add_tail(2);

        list.remove_all(1);
        assertEquals(3, list.size());
    }

    @Test
    public void testRemoveAll4() {
        list.add_tail(2);
        list.add_tail(1);
        list.add_tail(1);
        list.add_tail(2);
        list.add_tail(1);
        list.add_tail(1);
        list.add_tail(2);

        list.remove_all(2);
        assertEquals(4, list.size());
    }


    @Test
    public void testClear() {
        list.add_tail(1);
        list.clear();
        assertEquals(0, list.size());
    }

    @Test
    public void testGet() {
        list.add_tail(1);
        list.head();
        assertEquals(1, list.get().intValue());
    }

    @Test
    public void testSize() {
        list.add_tail(1);
        assertEquals(1, list.size());
    }

    @Test
    public void testIsHead() {
        list.add_tail(1);
        list.head();
        assertTrue(list.is_head());
    }

    @Test
    public void testIsTail() {
        list.add_tail(1);
        list.tail();
        assertTrue(list.is_tail());
    }

    @Test
    public void testIsValue() {
        list.add_tail(1);
        list.head();
        assertTrue(list.is_value());
    }
}