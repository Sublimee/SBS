from cleaning_state import CleaningState
from robot_api import RobotApi, RobotCommand
from pure_robot import RobotState
import pure_robot

def transfer_to_robot(message):
    print(message)

robot_api = RobotApi(pure_robot.move,
                     pure_robot.turn,
                     pure_robot.set_state,
                     pure_robot.start,
                     pure_robot.stop,
                     transfer_to_robot)
robot_state = robot_api.execute_command(RobotCommand(
    command='move 100',
    initial_state=RobotState(0.0, 0.0, 0, CleaningState.WATER),
))
robot_state = robot_api.execute_command(RobotCommand(
    command='turn -90',
    initial_state=robot_state,
))
robot_state = robot_api.execute_command(RobotCommand(
    command='set soap',
    initial_state=robot_state,
))
robot_state = robot_api.execute_command(RobotCommand(
    command='start',
    initial_state=robot_state,
))
robot_state = robot_api.execute_command(RobotCommand(
    command='move 50',
    initial_state=robot_state,
))
robot_state = robot_api.execute_command(RobotCommand(
    command='stop',
    initial_state=robot_state,
))
