package oa1.two_way_list;

/*

АТД ParentList

abstract class ParentList<T> {

    // интерфейс класса, реализующий АТД ParentList

    public final int HEAD_NIL = 0;      // head() ещё не вызывалась
    public final int HEAD_OK = 1;       // последняя команда установки курсора отработала нормально
    public final int HEAD_ERR = 2;      // список пуст

    public final int TAIL_NIL = 0;      // tail() ещё не вызывалась
    public final int TAIL_OK = 1;       // последняя команда установки курсора отработала нормально
    public final int TAIL_ERR = 2;      // список пуст

    public final int RIGHT_NIL = 0;     // right() ещё не вызывалась
    public final int RIGHT_OK = 1;      // последняя команда установки курсора отработала нормально
    public final int RIGHT_ERR = 2;     // список пуст (курсор не задан) или узел, на который указывает курсор, не имеет соседа справа

    public final int PUT_RIGHT_NIL = 0; // put_right() ещё не вызывалась
    public final int PUT_RIGHT_OK = 1;  // последняя команда добавления узла отработала нормально
    public final int PUT_RIGHT_ERR = 2; // список пуст (курсор не задан)

    public final int PUT_LEFT_NIL = 0;  // put_left() ещё не вызывалась
    public final int PUT_LEFT_OK = 1;   // последняя команда добавления узла отработала нормально
    public final int PUT_LEFT_ERR = 2;  // список пуст (курсор не задан)

    public final int REMOVE_NIL = 0;    // remove() ещё не вызывалась
    public final int REMOVE_OK = 1;     // последняя команда удаления узла отработала нормально
    public final int REMOVE_ERR = 2;    // список пуст (курсор не задан)

    public final int REPLACE_NIL = 0;   // replace() ещё не вызывалась
    public final int REPLACE_OK = 1;    // последняя команда замены значения узла отработала нормально
    public final int REPLACE_ERR = 2;   // список пуст (курсор не задан)

    public final int FIND_NIL = 0;      // find() ещё не вызывалась
    public final int FIND_OK = 1;       // последняя команда поиска искомого значения отработала нормально
    public final int FIND_ERR = 2;      // следующий узел не найден или список пуст (курсор не задан)

    public final int GET_NIL = 0;       // get() ещё не вызывалась
    public final int GET_OK = 1;        // последняя команда получения значения текущего узла отработала нормально
    public final int GET_ERR = 2;       // список пуст (курсор не задан)


    // конструктор

    // постусловие: создан новый список
    public ParentList<T> ParentList();


    // команды

    // предусловие: список не пуст
    // постусловие: курсор установлен на первый узел в списке
    public void head();

    // предусловие: список не пуст
    // постусловие: курсор установлен на последний узел в списке
    public void tail();

    // предусловие: 1) список не пуст (курсор задан)
    //              2) узел, на который указывает курсор, имеет соседа справа
    // постусловие: курсор сдвинут на один узел вправо
    public void right();

    // предусловие: список не пуст (курсор задан)
    // постусловие: следом за текущим узлом вставлен новый узел с заданным значением
    public void put_right(T value);

    // предусловие: список не пуст (курсор задан)
    // постусловие: перед текущим узлом вставлен новый узел с заданным значением
    public void put_left(T value);

    // предусловие: список не пуст (курсор задан)
    // постусловие: текущий узел удален (курсор смещается к правому соседу, если он есть, в противном случае курсор
    //                                  смещается к левому соседу, если он есть, в противном случае курсор сбрасывается
    //                                  т.к. список пуст)
    public void remove();

    // постусловие: новый узел добавлен в хвост списка
    public void add_tail(T value);

    // предусловие: список не пуст (курсор задан)
    // постусловие: значение текущего узла заменено на заданное
    public void replace(T value);

    // предусловие: список не пуст (курсор задан)
    // постусловие: курсор установлен на следующий узел с искомым значением (по отношению к текущему узлу),
    //              если таковой существует
    public void find(T value);

    // постусловие: из списка удалятся все узлы с заданным значением (если узел, на который указывал курсор, был удален,
    //                                                               то курсор смещается к первому оставшемуся правому
    //                                                               соседу, если он есть, в противном случае курсор
    //                                                               смещается к первому оставшемуся левому соседу, если
    //                                                               он есть, в противном случае курсор сбрасывается,
    //                                                               т.к. список пуст)
    public void remove_all(T value);

    // постусловие: из списка удалятся все значения, курсор сбрасывается, т.к. список пуст
    public void clear();


    // запросы

    // предусловие: курсор установлен
    public T get();             // получить значение текущего узла

    public int size();          // посчитать количество узлов в списке

    public boolean is_head();   // находится ли курсор в начале списка?

    public boolean is_tail();   // находится ли курсор в конце списка?

    public boolean is_value();  // установлен ли курсор на какой-либо узел в списке (по сути, непустой ли список)


    // дополнительные запросы:

    // возвращает значение HEAD_
    public int get_head_status();

    // возвращает значение TAIL_
    public int get_tail_status();

    // возвращает значение RIGHT_
    public int get_right_status();

    // возвращает значение PUT_RIGHT
    public int get_put_right_status();

    // возвращает значение PUT_LEFT_
    public int get_put_left_status();

    // возвращает значение REMOVE_
    public int get_remove_status();

    // возвращает значение REPLACE_
    public int get_replace_status();

    // возвращает значение FIND_
    public int get_find_status();

    // возвращает значение GET_
    public int get_get_status();
}


АТД LinkedList

abstract class LinkedList<T> extends ParentList<T> {

    // конструктор

    // постусловие: создан новый список
    public LinkedList<T> LinkedList();
}


АТД TwoWayList

abstract class TwoWayList<T> extends ParentList<T> {

    public final int LEFT_NIL = 0;     // left() ещё не вызывалась
    public final int LEFT_OK = 1;      // последняя команда установки курсора отработала нормально
    public final int LEFT_ERR = 2;     // список пуст (курсор не задан) или узел, на который указывает курсор, не имеет соседа слева


    // конструктор

    // постусловие: создан новый список
    public TwoWayList<T> TwoWayList();


    // команды

    // предусловие: 1) список не пуст (курсор задан)
    //              2) узел, на который указывает курсор, имеет соседа слева
    // постусловие: курсор сдвинут на один узел влево
    public void left();


    // дополнительные запросы:

    // возвращает значение LEFT_
    public int get_left_status();
}
*/