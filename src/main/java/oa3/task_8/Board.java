/*
    АТД Board

abstract class Board {

    public final int MAKE_MOVE_NIL = 0;     // make_move() ещё не вызывалась
    public final int MAKE_MOVE_OK = 1;      // последняя команда выполнения хода make_move() отработала нормально
    public final int MAKE_MOVE_ERR = 2;     // 1 или более поле-источник в рамках хода -- пустое

    // конструктор

    // постусловие: создана игровая доска с расставленными на ней фигурами
    public Board Board();


    // команды

    // предусловие: поля-источники (на которых изначально стоят фигуры) не пустые
    // постусловие: поля-источники становятся пустым, а поля-приемники заполняются переданными фигурами
    public void make_move(Move move);


    // запросы

    public boolean isFieldEmpty(Field field); // проверяет, занято ли поле фигурой

    public Piece getPiece(Field field); // получает фигуру по переданному полю


    // дополнительные запросы

    // возвращает значение MAKE_MOVE_
    public int get_make_move_status();
}
 */