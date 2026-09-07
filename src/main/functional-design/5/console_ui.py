#     public static void Draw(Board board)
#     {
#         Console.WriteLine("  0 1 2 3 4 5 6 7");
#         for (int i = 0; i < 8; i++)
#         {
#             Console.Write(i + " ");
#             for (int j = 0; j < 8; j++)
#             {
#                 Console.Write(board.cells[i, j].Symbol + " ");
#             }
#
#             Console.WriteLine();
#         }
#
#         Console.WriteLine();
#     }
def draw(board):
    print(_header_line(board["size"]))
    for row in range(board["size"]):
        print(_board_line(board, row))
    print()


def _board_line(board, row):
    line = format(row) + " "
    for column in range(board["size"]):
        line = line + board["cells"][row][column] + " "
    return line


def _header_line(size):
    line = "  "
    for column in range(size):
        line = line + format(column) + " "
    return line


#     public static BoardState ReadMove(BoardState bs)
#     {
#         Console.WriteLine(">");
#         string input = Console.ReadLine();
#         if (input == "q")
#             Environment.Exit(0);
#
#         Board board = CloneBoard(bs.Board);
#         string[] coords = input.Split(' ');
#         int x = int.Parse(coords[1]);
#         int y = int.Parse(coords[0]);
#         int x1 = int.Parse(coords[3]);
#         int y1 = int.Parse(coords[2]);
#         ...
#     }
def read_move(board):
    while True:
        size = board["size"]
        first_column = _read_coordinate("x", size)
        first_row = _read_coordinate("y", size)
        second_column = _read_coordinate("x1", size)
        second_row = _read_coordinate("y1", size)

        if _is_valid_move(
                first_row,
                first_column,
                second_row,
                second_column,
        ):
            return {
                "first_row": first_row,
                "first_column": first_column,
                "second_row": second_row,
                "second_column": second_column,
            }

        print("Illegal move.")

def _read_coordinate(name, size):
    while True:
        value = input(name + ": ")
        if value == "q":
            raise SystemExit

        try:
            coordinate = int(value)
        except ValueError:
            print("Enter correct coordinate.")
            continue

        if 0 <= coordinate < size:
            return coordinate

        print(f"Coordinate must be between 0 and {size - 1}.")


def _is_valid_move(first_row, first_column, second_row, second_column):
    distance = abs(first_row - second_row) + abs(first_column - second_column)
    return distance == 1
