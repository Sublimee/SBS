#     public const char EMPTY = '0';
EMPTY = "0"


#     static char[] symbols = { 'A', 'B', 'C', 'D', 'E', 'F' };
SYMBOLS = ("A", "B", "C", "D", "E", "F")


#     public enum MatchDirection
#     {
#         Horizontal,
#         Vertical
#     }
HORIZONTAL = "horizontal"
VERTICAL = "vertical"


#     public Board(int s)
#     {
#         size = s;
#         cells = new Element[size, size];
#         for (int x = 0; x < size; x++)
#         for (int y = 0; y < size; y++)
#             cells[x, y] = new Element(Element.EMPTY);
#     }
def make_empty_board(size, choose_symbol):
    return {
        "size": size,
        "cells": make_empty_cells(size),
        "choose_symbol": choose_symbol,
    }

def make_empty_cells(size):
    return [
        [EMPTY for _ in range(size)]
        for _ in range(size)
    ]

def make_board_from_cells(size, cells, choose_symbol):
    copied_cells = [
        [cell for cell in row]
        for row in cells
    ]
    return {
        "size": size,
        "cells": copied_cells,
        "choose_symbol": choose_symbol,
    }


#     public static Board CloneBoard(Board board)
#     {
#         Board b = new Board(board.size);
#         for (int row = 0; row < board.size; row++)
#         for (int col = 0; col < board.size; col++)
#             b.cells[row, col] = board.cells[row, col];
#         return b;
#     }
def clone_board(board):
    return make_board_from_cells(
        board["size"],
        board["cells"],
        board["choose_symbol"],
    )


#     public BoardState(Board board, int score)
#     {
#         Board = board;
#         Score = score;
#     }
def make_board_state(board, score=0):
    return {"board": board, "score": score}


#     public Match(MatchDirection direction, int row, int col, int length)
#     {
#         Direction = direction;
#         Row = row;
#         Col = col;
#         Length = length;
#     }
def make_match(direction, row, column, length):
    return {
        "direction": direction,
        "row": row,
        "column": column,
        "length": length,
    }
