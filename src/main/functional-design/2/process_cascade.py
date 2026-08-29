from game_logic import fill_empty_spaces, find_matches, remove_matches


def process_cascade(board_state):
    matches = find_matches(board_state["board"])
    if not matches:
        return board_state

    state_without_matches = remove_matches(board_state, matches)
    filled_state = fill_empty_spaces(state_without_matches)

    return process_cascade(filled_state)
