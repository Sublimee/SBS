package oa1.two_way_list;

public abstract class ParentList<T> {

    public final int HEAD_NIL = 0;
    public final int HEAD_OK = 1;
    public final int HEAD_ERR = 2;

    public final int TAIL_NIL = 0;
    public final int TAIL_OK = 1;
    public final int TAIL_ERR = 2;

    public final int RIGHT_NIL = 0;
    public final int RIGHT_OK = 1;
    public final int RIGHT_ERR = 2;

    public final int PUT_RIGHT_NIL = 0;
    public final int PUT_RIGHT_OK = 1;
    public final int PUT_RIGHT_ERR = 2;

    public final int PUT_LEFT_NIL = 0;
    public final int PUT_LEFT_OK = 1;
    public final int PUT_LEFT_ERR = 2;

    public final int REMOVE_NIL = 0;
    public final int REMOVE_OK = 1;
    public final int REMOVE_ERR = 2;

    public final int REPLACE_NIL = 0;
    public final int REPLACE_OK = 1;
    public final int REPLACE_ERR = 2;

    public final int FIND_NIL = 0;
    public final int FIND_OK = 1;
    public final int FIND_ERR = 2;

    public final int GET_NIL = 0;
    public final int GET_OK = 1;
    public final int GET_ERR = 2;
    protected Node<T> cursor;
    private Node<T> head;
    private Node<T> tail;
    private int size;

    private int HEAD_STATUS = HEAD_NIL;
    private int TAIL_STATUS = TAIL_NIL;
    private int RIGHT_STATUS = RIGHT_NIL;
    private int PUT_RIGHT_STATUS = PUT_RIGHT_NIL;
    private int PUT_LEFT_STATUS = PUT_LEFT_NIL;
    private int REMOVE_STATUS = REMOVE_NIL;
    private int REPLACE_STATUS = REPLACE_NIL;
    private int FIND_STATUS = FIND_NIL;
    private int GET_STATUS = GET_NIL;

    public ParentList() {
        clear();
    }


    public void head() {
        if (is_value()) {
            cursor = head;
            HEAD_STATUS = HEAD_OK;
        } else {
            HEAD_STATUS = HEAD_ERR;
        }
    }

    public void tail() {
        if (is_value()) {
            cursor = tail;
            TAIL_STATUS = TAIL_OK;
        } else {
            TAIL_STATUS = TAIL_ERR;
        }
    }

    public void right() {
        if (is_value() && cursor.next != null) {
            cursor = cursor.next;
            RIGHT_STATUS = RIGHT_OK;
        } else {
            RIGHT_STATUS = RIGHT_ERR;
        }
    }

    public void put_right(T value) {
        if (is_value()) {
            Node<T> newNode = new Node<>(value);

            if (is_tail()) {
                newNode.prev = tail;
                tail.next = newNode;
                tail = newNode;
            } else {
                newNode.prev = cursor;
                newNode.next = cursor.next;

                cursor.next.prev = newNode;
                cursor.next = newNode;
            }

            size++;
            PUT_RIGHT_STATUS = PUT_RIGHT_OK;
        } else {
            PUT_RIGHT_STATUS = PUT_RIGHT_ERR;
        }
    }

    public void put_left(T value) {
        if (is_value()) {
            Node<T> newNode = new Node<>(value);

            newNode.next = cursor;
            if (is_head()) {
                cursor.prev = newNode;
                head = newNode;
            } else {
                newNode.prev = cursor.prev;

                cursor.prev.next = newNode;
                cursor.prev = newNode;
            }

            size++;
            PUT_LEFT_STATUS = PUT_LEFT_OK;
        } else {
            PUT_LEFT_STATUS = PUT_LEFT_ERR;
        }
    }

    public void remove() {
        if (is_value()) {
            if (is_tail() && is_head()) {
                tail = null;
                head = null;
                cursor = null;
            } else if (is_tail()) {
                tail = cursor.prev;
                cursor.prev.next = null;
                cursor = tail;
            } else if (is_head()) {
                head = cursor.next;
                cursor.next.prev = null;
                cursor = head;
            } else {
                cursor.next.prev = cursor.prev;
                cursor.prev.next = cursor.next;
                cursor = cursor.next;
            }

            size--;
            REMOVE_STATUS = REMOVE_OK;
        } else {
            REMOVE_STATUS = REMOVE_ERR;
        }
    }

    public void add_tail(T value) {
        Node<T> newNode = new Node<>(value);

        if (is_value()) {
            newNode.prev = tail;
            tail.next = newNode;
        } else {
            head = newNode;
            cursor = head;
        }
        tail = newNode;

        size++;
    }

    public void replace(T value) {
        if (is_value()) {
            cursor.value = value;
            REPLACE_STATUS = REPLACE_OK;
        } else {
            REPLACE_STATUS = REPLACE_ERR;
        }
    }

    public void find(T value) {
        if (is_value()) {
            Node<T> start = cursor;

            while (cursor.value != value && cursor.next != null) {
                right();
            }

            if (cursor == tail && tail.value != value) {
                cursor = start;
                FIND_STATUS = FIND_ERR;
            } else {
                FIND_STATUS = FIND_OK;
            }
        } else {
            FIND_STATUS = FIND_ERR;
        }
    }

    public void remove_all(T value) {
        Node<T> start = cursor;

        cursor = head;
        find(value);
        while (FIND_STATUS == FIND_OK) {
            if (cursor == start) {
                remove();
                start = cursor;
            } else {
                remove();
            }
            cursor = head;
            find(value);
        }
        cursor = start;
    }

    public void clear() {
        this.head = null;
        this.tail = null;
        this.cursor = null;
        this.size = 0;

        HEAD_STATUS = HEAD_NIL;
        TAIL_STATUS = TAIL_NIL;
        RIGHT_STATUS = RIGHT_NIL;
        PUT_RIGHT_STATUS = PUT_RIGHT_NIL;
        PUT_LEFT_STATUS = PUT_LEFT_NIL;
        REMOVE_STATUS = REMOVE_NIL;
        REPLACE_STATUS = REPLACE_NIL;
        FIND_STATUS = FIND_NIL;
        GET_STATUS = GET_NIL;
    }

    public T get() {
        T result;
        if (is_value()) {
            result = cursor.value;
            GET_STATUS = GET_OK;
        } else {
            result = null;
            GET_STATUS = GET_ERR;
        }
        return result;
    }

    public int size() {
        return size;
    }

    public boolean is_head() {
        return cursor == head;
    }

    public boolean is_tail() {
        return cursor == tail;
    }

    public boolean is_value() {
        return cursor != null;
    }


    public int get_head_status() {
        return HEAD_STATUS;
    }

    public int get_tail_status() {
        return TAIL_STATUS;
    }

    public int get_right_status() {
        return RIGHT_STATUS;
    }

    public int get_put_right_status() {
        return PUT_RIGHT_STATUS;
    }

    public int get_put_left_status() {
        return PUT_LEFT_STATUS;
    }

    public int get_remove_status() {
        return REMOVE_STATUS;
    }

    public int get_replace_status() {
        return REPLACE_STATUS;
    }

    public int get_find_status() {
        return FIND_STATUS;
    }

    public int get_get_status() {
        return GET_STATUS;
    }
}
