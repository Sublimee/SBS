from cleaning_state import CleaningState
from robot_api import RobotApi, RobotCommand
from pure_robot import RobotState


robot_api = RobotApi()
robot_state = robot_api.execute(RobotCommand(
    command='move 100',
    initial_state=RobotState(0.0, 0.0, 0, CleaningState.WATER),
))
robot_state = robot_api.execute(RobotCommand(
    command='turn -90',
    initial_state=robot_state,
))
robot_state = robot_api.execute(RobotCommand(
    command='set soap',
    initial_state=robot_state,
))
robot_state = robot_api.execute(RobotCommand(
    command='start',
    initial_state=robot_state,
))
robot_state = robot_api.execute(RobotCommand(
    command='move 50',
    initial_state=robot_state,
))
robot_state = robot_api.execute(RobotCommand(
    command='stop',
    initial_state=robot_state,
))
