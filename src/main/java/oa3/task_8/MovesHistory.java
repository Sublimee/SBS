/*
    АТД MovesHistory

abstract class MovesHistory {

    public final int GET_LAST_MOVE_NIL = 0;     // add_move() ещё не вызывалась
    public final int GET_LAST_MOVE_OK = 1;      // последняя команда добавления нового хода get_last_move() отработала нормально

    public final int IS_LAST_MOVES_REPEATED_OK = 1;      // последний запрос is_last_moves_repeated() отработал нормально
    public final int IS_LAST_MOVES_REPEATED_ERR = 2;     // количество последних анализируемых ходов count больше, чем количество элементов в истории ходов

    public final int IS_LAST_MOVES_NO_TAKING_OK = 1;      // последний запрос is_last_moves_no_taking() отработал нормально
    public final int IS_LAST_MOVES_NO_TAKING_ERR = 2;     // количество последних анализируемых ходов count больше, чем количество элементов в истории ходов

    // конструктор

    // постусловие: создана пустая история ходов
    public MovesHistory MovesHistory();


    // команды

    // постусловие: в историю ходов добавлено новое значение move
    public void add_move(Move move);


    // запросы

    // предусловие: история ходов не пуста
    public Move get_last_move(); // получить последний сделанный ход

    // предусловие: количество последних анализируемых ходов count меньше или равно, количеству элементов в истории ходов
    public Move is_last_moves_repeated(int count); // повторяются ли последние count ходов

    // предусловие: количество последних анализируемых ходов count меньше или равно, количеству элементов в истории ходов
    public Move is_last_moves_no_taking(int count); // было ли взятие последние count ходов

    // дополнительные запросы

    // возвращает значение GET_LAST_MOVE_
    public int get_get_last_move_status();

    // возвращает значение IS_LAST_MOVES_REPEATED_
    public int get_is_last_moves_repeated_status();

    // возвращает значение IS_LAST_MOVES_NO_TAKING_
    public int get_is_last_moves_no_taking_status();
}
 */