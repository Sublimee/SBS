import math
from collections import namedtuple

from cleaning_state import CleaningState

RobotState = namedtuple("RobotState", ["x", "y", "angle", "state"])


def move(distance):
    def inner(state):
        theta_rad = math.radians(state.angle)
        new_x = state.x + distance * math.cos(theta_rad)
        new_y = state.y + distance * math.sin(theta_rad)
        new_state = RobotState(
            x=int(new_x),
            y=int(new_y),
            angle=state.angle,
            state=state.state
        )
        result = f"POS {new_state.x},{new_state.y}"
        return new_state, result

    return inner


def turn(delta_angle):
    def inner(state):
        new_state = RobotState(
            x=state.x,
            y=state.y,
            angle=(state.angle + delta_angle) % 360,
            state=state.state
        )
        result = f"ANGLE {new_state.angle}"
        return new_state, result

    return inner


def set_state(state_str):
    def inner(state):
        try:
            new_state_value = CleaningState(state_str)
        except ValueError:
            result = f"Error: Invalid state '{state_str}'"
            return state, result
        new_state = RobotState(
            x=state.x,
            y=state.y,
            angle=state.angle,
            state=new_state_value
        )
        result = f"STATE {new_state.state.value}"
        return new_state, result

    return inner


def start():
    def inner(state):
        result = f"START WITH {state.state.value}"
        return state, result

    return inner


def stop():
    def inner(state):
        result = "STOP"
        return state, result

    return inner
