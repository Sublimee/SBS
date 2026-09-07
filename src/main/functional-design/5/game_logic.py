from model import (
    EMPTY,
    HORIZONTAL,
    VERTICAL,
    clone_board,
    make_board_from_cells,
    make_board_state,
    make_empty_cells,
    make_match,
)


#     public static List<Match> FindMatches(Board board)
#     {
#         var matches = new List<Match>();
#
#         // Горизонтальные комбинации
#         for (int row = 0; row < board.size; row++)
#         {
#             int startCol = 0;
#             for (int col = 1; col < board.size; col++)
#             {
#                 // Пропускаем пустые ячейки в начале строки
#                 if (board.cells[row, startCol].Symbol == Element.EMPTY)
#                 {
#                     startCol = col;
#                     continue;
#                 }
#
#                 // Если текущая ячейка пустая, обрываем текущую последовательность
#                 if (board.cells[row, col].Symbol == Element.EMPTY)
#                 {
#                     AddMatchIfValid(matches, row, startCol, col - startCol, MatchDirection.Horizontal);
#                     startCol = col + 1;
#                     continue;
#                 }
#
#                 // Проверяем совпадение символов для непустых ячеек
#                 if (board.cells[row, col].Symbol != board.cells[row, startCol].Symbol)
#                 {
#                     AddMatchIfValid(matches, row, startCol, col - startCol, MatchDirection.Horizontal);
#                     startCol = col;
#                 }
#                 else if (col == board.size - 1)
#                 {
#                     AddMatchIfValid(matches, row, startCol, col - startCol + 1, MatchDirection.Horizontal);
#                 }
#             }
#         }
#
#         // Вертикальные комбинации
#         for (int col = 0; col < board.size; col++)
#         {
#             int startRow = 0;
#             for (int row = 1; row < board.size; row++)
#             {
#                 // Пропускаем пустые ячейки в начале столбца
#                 if (board.cells[startRow, col].Symbol == Element.EMPTY)
#                 {
#                     startRow = row;
#                     continue;
#                 }
#
#                 // Если текущая ячейка пустая, обрываем текущую последовательность
#                 if (board.cells[row, col].Symbol == Element.EMPTY)
#                 {
#                     AddMatchIfValid(matches, startRow, col, row - startRow, MatchDirection.Vertical);
#                     startRow = row + 1;
#                     continue;
#                 }
#
#                 // Проверяем совпадение символов для непустых ячеек
#                 if (board.cells[row, col].Symbol != board.cells[startRow, col].Symbol)
#                 {
#                     AddMatchIfValid(matches, startRow, col, row - startRow, MatchDirection.Vertical);
#                     startRow = row;
#                 }
#                 else if (row == board.size - 1)
#                 {
#                     AddMatchIfValid(matches, startRow, col, row - startRow + 1, MatchDirection.Vertical);
#                 }
#             }
#         }
#
#         return matches;
#     }
#
#     private static void AddMatchIfValid(List<Match> matches, int row, int col,
#                 int length, MatchDirection direction)
#    {
#         // Учитываем только комбинации из 3 и более элементов (ТЗ)
#         if (length >= 3)
#         {
#             matches.Add(new Match(direction, row, col, length));
#         }
#     }
def find_matches(board):
    matches = []

    for row in range(board["size"]):
        matches = matches + _find_line_matches(board, HORIZONTAL, row)

    for column in range(board["size"]):
        matches = matches + _find_line_matches(board, VERTICAL, column)

    return matches

def _find_line_matches(board, direction, fixed_index):
    size = board["size"]
    matches = []
    start = 0

    while start < size:
        symbol = _cell(board, direction, fixed_index, start)
        if symbol == EMPTY:
            start += 1
            continue

        end = start + 1
        while end < size and _cell(board, direction, fixed_index, end) == symbol:
            end += 1

        length = end - start
        if length >= 3:
            row = fixed_index if direction == HORIZONTAL else start
            column = start if direction == HORIZONTAL else fixed_index
            matches = matches + [make_match(direction, row, column, length)]

        start = end

    return matches

def _cell(board, direction, constant, offset):
    if direction == HORIZONTAL:
        return board["cells"][constant][offset]
    return board["cells"][offset][constant]


#     private static Element[,] MarkCellsForRemoval(Board board, List<Match> matches)
#     {
#         Element[,] newCells = (Element[,])board.cells.Clone();
#
#         foreach (var match in matches)
#         {
#             for (int i = 0; i < match.Length; i++)
#             {
#                 int row = match.Direction == MatchDirection.Horizontal ? match.Row : match.Row + i;
#                 int col = match.Direction == MatchDirection.Horizontal ? match.Col + i : match.Col;
#
#                 newCells[row, col] = new Element { Symbol = Element.EMPTY };
#             }
#         }
#
#         return newCells;
#     }
def _mark_cells_for_removal(board, matches):
    new_cells = [
        [cell for cell in row]
        for row in board["cells"]
    ]

    for match in matches:
        for offset in range(match["length"]):
            if match["direction"] == HORIZONTAL:
                row = match["row"]
                column = match["column"] + offset
            else:
                row = match["row"] + offset
                column = match["column"]

            new_cells[row][column] = EMPTY

    return new_cells


#     private static Element[,] ApplyGravity(Element[,] cells, int size)
#     {
#         Element[,] newCells = new Element[size, size];
#
#         for (int row = 0; row < size; row++)
#         {
#             for (int col = 0; col < size; col++)
#             {
#                 newCells[row, col] = new Element { Symbol = Element.EMPTY };
#             }
#         }
#
#         for (int col = 0; col < size; col++)
#         {
#             int newRow = size - 1;
#             for (int row = size - 1; row >= 0; row--)
#             {
#                 if (cells[row, col].Symbol != Element.EMPTY)
#                 {
#                     newCells[newRow, col] = cells[row, col];
#                     newRow--;
#                 }
#             }
#         }
#
#         return newCells;
#     }
def _apply_gravity(cells, size):
    new_cells = make_empty_cells(size)

    for column in range(size):
        remaining = [
            cells[row][column]
            for row in range(size)
            if cells[row][column] != EMPTY
        ]
        first_row = size - len(remaining)

        for offset in range(len(remaining)):
            new_cells[first_row + offset][column] = remaining[offset]

    return new_cells


#     public static BoardState RemoveMatches(BoardState currentState, List<Match> matches)
#     {
#         if (matches == null || matches.Count == 0)
#             return currentState;
#
#         // Шаг 1: Помечаем ячейки для удаления
#         Element[,] markedCells = MarkCellsForRemoval(currentState.Board, matches);
#
#         // Шаг 2: Применяем гравитацию
#         Element[,] gravityAppliedCells = ApplyGravity(markedCells, currentState.Board.size);
#
#         // Шаг 3: Подсчитываем очки
#         int removedCount = matches.Sum(m => m.Length);
#         int newScore = currentState.Score + CalculateScore(removedCount);
#
#         // Возвращаем НОВОЕ состояние
#         return new BoardState(
#             new Board { size = currentState.Board.size, cells = gravityAppliedCells },
#             newScore
#         );
#     }
#
#     private static int CalculateScore(int removedCount)
#     {
#         // Базовая система подсчета очков: 10 за каждый элемент
#         return removedCount * 10;
#     }
def remove_matches(current_state, matches):
    if not matches:
        return current_state

    board = current_state["board"]
    marked_cells = _mark_cells_for_removal(board, matches)
    gravity_applied_cells = _apply_gravity(marked_cells, board["size"])
    removed_count = sum(match["length"] for match in matches)
    new_score = current_state["score"] + removed_count * 10
    new_board = make_board_from_cells(
        board["size"],
        gravity_applied_cells,
        board["choose_symbol"],
    )

    return make_board_state(new_board, new_score)


#     public static BoardState FillEmptySpaces(BoardState currentState)
#     {
#         if (currentState.Board.cells == null)
#             return currentState;
#
#         Element[,] newCells = (Element[,])currentState.Board.cells.Clone();
#
#         for (int row = 0; row < currentState.Board.size; row++)
#         {
#             for (int col = 0; col < currentState.Board.size; col++)
#             {
#                 if (newCells[row, col].Symbol == Element.EMPTY)
#                 {
#                     newCells[row, col] = new Element
#                     {
#                         Symbol = symbols[r.Next(symbols.Length)]
#                     };
#                 }
#             }
#         }
#
#         return new BoardState(
#             new Board { size = currentState.Board.size, cells = newCells },
#             currentState.Score
#         );
#     }
def fill_empty_spaces(current_state):
    board = current_state["board"]
    if board["cells"] is None:
        return current_state

    choose_symbol = board["choose_symbol"]
    new_cells = [
        [
            choose_symbol() if cell == EMPTY else cell
            for cell in row
        ]
        for row in board["cells"]
    ]
    new_board = make_board_from_cells(
        board["size"],
        new_cells,
        choose_symbol,
    )

    return make_board_state(new_board, current_state["score"])

#     public static BoardState ReadMove(BoardState bs)
#     {
#         ...
#         Element e = board.cells[x, y];
#         board.cells[x, y] = board.cells[x1, y1];
#         board.cells[x1, y1] = e;
#         BoardState bb = new BoardState(board, bs.Score);
#         return bb;
#     }
def make_move(current_state, move):
    board = clone_board(current_state["board"])
    cells = board["cells"]
    first_row = move["first_row"]
    first_column = move["first_column"]
    second_row = move["second_row"]
    second_column = move["second_column"]
    first_element = cells[first_row][first_column]
    cells[first_row][first_column] = cells[second_row][second_column]
    cells[second_row][second_column] = first_element

    return make_board_state(board, current_state["score"])
