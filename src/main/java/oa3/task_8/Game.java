/*
    АТД Game

abstract class Game {

    public final int MAKE_MOVE_NIL = 0;     // make_move() ещё не вызывалась
    public final int MAKE_MOVE_OK = 1;      // последняя команда выполнения хода make_move() отработала нормально
    public final int MAKE_MOVE_ERR = 2;     // ход не соответствует правилам шахмат

    public final int EXECUTE_ACTION_NIL = 0;     // execute_action() ещё не вызывалась
    public final int EXECUTE_ACTION_OK = 1;      // последняя команда execute_action() отработала нормально
    public final int EXECUTE_ACTION_ERR = 2;     // действие не найдено

    // конструктор

    // постусловие: создана новая игра
    public Game Game();


    // команды

    // предусловие: ход соответствует правилам
    // постусловие: в соответствии с правилами фигура(ы) изменила(и) положение на игровой доске и при необходимости изменилось состояние игры
    public void make_move(Move move);

    // предусловие: игра распознает переданный тип действия пользователя
    // постусловие: меняется состояние игры
    public void execute_action(Action action);


    // запросы

    public boolean getState(); // получить состояние игры

    public boolean getBoard(); // получить игровое поле


    // дополнительные запросы

    // возвращает значение MAKE_MOVE_
    public int get_make_move_status();

    // возвращает значение EXECUTE_ACTION_
    public int get_execute_action_status();
}
*/