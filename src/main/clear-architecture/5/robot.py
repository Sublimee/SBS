import math
from collections import namedtuple

from cleaning_state import CleaningState
from command_decorator import command
from command_decorator import command_map

RobotState = namedtuple("RobotState", ["x", "y", "angle", "state"])


def transfer_to_cleaner(message):
    print(message)


def make(transfer, commands, state):
    for cmd in commands:
        state = execute_command(transfer, cmd, state)
    return state


def execute_command(transfer, cmd, state):
    tokens = cmd.strip().split()
    if not tokens:
        return state
    command_name = tokens[0]
    args = tokens[1:]
    command_func = command_map.get(command_name)
    if command_func:
        return command_func(transfer, args, state)
    else:
        transfer(f"Unknown command: {command_name}")
        return state


@command()
def move(transfer, args, state):
    if len(args) != 1:
        transfer("Error: 'move' command requires one argument")
        return state
    try:
        distance = int(args[0])
    except ValueError:
        transfer("Error: 'move' command requires a numeric argument")
        return state
    theta_rad = math.radians(state.angle)
    new_x = state.x + distance * math.cos(theta_rad)
    new_y = state.y + distance * math.sin(theta_rad)
    new_state = RobotState(
        x=int(new_x),
        y=int(new_y),
        angle=state.angle,
        state=state.state
    )
    transfer(f"POS {new_state.x},{new_state.y}")
    return new_state


@command()
def turn(transfer, args, state):
    if len(args) != 1:
        transfer("Error: 'turn' command requires one argument")
        return state
    try:
        delta_angle = int(args[0])
    except ValueError:
        transfer("Error: 'turn' command requires a numeric argument")
        return state
    new_state = RobotState(
        x=state.x,
        y=state.y,
        angle=(state.angle + delta_angle) % 360,
        state=state.state
    )
    transfer(f"ANGLE {new_state.angle}")
    return new_state


@command('set')
def set_state(transfer, args, state):
    if len(args) != 1:
        transfer("Error: 'set' command requires one argument")
        return state
    state_str = args[0]
    try:
        new_state_value = CleaningState(state_str)
    except ValueError:
        transfer(f"Error: Invalid state '{state_str}'")
        return state
    new_state = RobotState(
        x=state.x,
        y=state.y,
        angle=state.angle,
        state=new_state_value
    )
    transfer(f"STATE {new_state.state.value}")
    return new_state


@command()
def start(transfer, args, state):
    transfer(f"START WITH {state.state.value}")
    return state


@command()
def stop(transfer, args, state):
    transfer("STOP")
    return state
