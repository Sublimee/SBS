from game_logic import fill_empty_spaces, find_matches, remove_matches
from pipe21 import Pipe

def process_cascade(board_state):
    matches = find_matches(board_state["board"])
    if not matches:
        return board_state

    state_without_matches = remove_matches(board_state, matches)
    filled_state = fill_empty_spaces(state_without_matches)

    return process_cascade(filled_state)

def process_cascade_piped(board_state):
    matches = find_matches(board_state["board"])
    if not matches:
        return board_state

    return (
        remove_matches(board_state, matches)
        | Pipe(fill_empty_spaces)
        | Pipe(process_cascade_piped)
    )
