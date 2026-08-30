from pipe21 import Pipe

# нравится больше
def initialize_game():
    empty_board = make_empty_board(8)
    empty_board_state = make_board_state(empty_board, 0)
    filled_board_state = fill_empty_spaces(empty_board_state)
    return process_cascade(filled_board_state)

# нравится меньше из-за Pipe
def initialize_game_piped():
    return (
            make_empty_board(8)
            | Pipe(make_board_state)
            | Pipe(fill_empty_spaces)
            | Pipe(process_cascade)
    )

# Есть другие библиотеки с более чистым синтаксисом, например, https://github.com/Jordan-Kowal/pipe-operator, но в
# основном перестали поддерживаться авторами