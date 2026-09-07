from random import choice
from pipe21 import Pipe

from console_ui import draw, read_move
from game_logic import fill_empty_spaces, make_move
from model import SYMBOLS, make_empty_board, make_board_state
from process_cascade import process_cascade, process_cascade_piped


#     static void Main(string[] args)
#     {
#         BoardState bs = Game.InitializeGame();
#         while (true)
#         {
#             Game.Draw(bs.Board);
#             bs = Game.ReadMove(bs);
#         }
#     }
#
#     public static BoardState InitializeGame(int boardSize = 8)
#     {
#         return ProcessCascade(FillEmptySpaces(new BoardState(new Board(boardSize), 0)));
#     }
def initialize_game():
    empty_board_state = make_board_state(make_empty_board(8, lambda: choice(SYMBOLS)), 0)
    filled_board_state = fill_empty_spaces(empty_board_state)
    return process_cascade(filled_board_state)

def initialize_game_piped():
    return (
            make_empty_board(8, lambda: choice(SYMBOLS))
            | Pipe(make_board_state)
            | Pipe(fill_empty_spaces)
            | Pipe(process_cascade_piped)
    )

def process_move(board_state):
    move = read_move(board_state["board"])
    return make_move(board_state, move)

def show_state(board_state):
    draw(board_state["board"])
    print("Score:", board_state["score"])
    return board_state

def process_turn(board_state):
    return (
            board_state
            | Pipe(show_state)
            | Pipe(process_move)
            | Pipe(process_cascade_piped)
    )

board_state = initialize_game_piped()
while True:
    board_state = process_turn(board_state)

