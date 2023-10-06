package oa1.two_way_list;

public class TwoWayList<T> extends ParentList<T> {

    public final int LEFT_NIL = 0;
    public final int LEFT_OK = 1;
    public final int LEFT_ERR = 2;

    private int LEFT_STATUS = LEFT_NIL;

    public TwoWayList() {
        clear();
    }

    public void left() {
        if (is_value() && !is_head()) {
            cursor = cursor.prev;
            LEFT_STATUS = LEFT_OK;
        } else {
            LEFT_STATUS = LEFT_ERR;
        }
    }

    @Override
    public void clear() {
        super.clear();
        LEFT_STATUS = LEFT_NIL;
    }

    public int get_left_status() {
        return LEFT_STATUS;
    }
}