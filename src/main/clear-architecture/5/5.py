from cleaning_state import CleaningState
from robot import RobotState, make, transfer_to_cleaner

# Список команд
commands = [
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
]

# Начальное состояние
initial_state = RobotState(0.0, 0.0, 0, CleaningState.WATER)

final_state = make(transfer_to_cleaner, commands, initial_state)
