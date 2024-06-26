Взаимодействие с движком игры (описывается АТД Game) происходит через интерфейс пользователя. Выбор интерфейса не влияет на работу игры (ни на АТД Game, ни на реализацию).

В качестве интерфейса для взаимодействия пользователя с игрой выступает консоль, через которую игроки поочередно вводят команды и ходы. Интерфейс используется также для отображения текущего состояния игры (State) и доски (Board) после каждого хода.

Реализация Game задает начальные позиции фигур на доске, а также задает влияние, которые оказывают ходы и команды пользователей на состояние игры (make_move() и execute_action()). Текущее состояние, которое говорит о возможности продолжения игры, результате игры, ожидаемой команде или ходе, можно получить, выполнив запрос getState(). Для отображения игровой доски в UI используется запрос getBoard(). За хранение истории ходов отвечает АТД MovesHistory, которая позволяет правильно оценить состояние игры.

Кроме оговоренных выше АТД есть еще ряд классов, которые важны для игры, но АТД не являются. Это иерархия фигур Piece, ход Move, команда Command, поле Field.

Game должна производить валидацию вводимых команд и ходов на корректность. Если осуществлен некорректный ввод, то система просит ввести команду или ход повторно.

Если была введена команда, то:
0) если это команда старта игры, то игра начинается
1) если это предложение ничьей, то требуется соглашение с ней или ее отклонение от второго игрока. Игра при объявлении ничьей завершается.
2) если это предложение сдачи, то игра завершается в пользу другого игрока. Игра при этом завершается.

Если введенная команда не найдена, то игроку дается возможность повторно осуществить ввод с соответствующим сообщением о неверной команде.

Если был введен ход, то проверяем его на соответствие классическим правилам шахмат.

Если игра в соответствии с классическим правилам шахмат не может быть продолжена, то игрокам сообщается причина. Они могут начать игру заново вводом соответствующей команды. 

Для удобства тестирования используется конструктор Game и Board, которые должны уметь принимать fen-нотацию (не было учтено в АТД) для удобной расстановки фигур в заданной конфигурации. Должны быть осуществлены проверки:
* перехода во все состояния игры (мат, пат, троекратное повторение ходов, 50 ходов без взятий, ничья)
* проверка возможности сделать очередной ход по заданным координатам для различных вариаций фигур и короля (рокировка, корректность координат, подпадание под шахи, взятие короля, взятие на проходе, движение пешкой на 2 клетки вперед)
* проверка превращения фигуры
* проверка работы взятия