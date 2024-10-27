import pure_robot
from robot_api import RobotApi


def transfer_to_robot(message):
    print(message)


def command_handler(command):
    tokens = command.strip().split()
    command_name = tokens[0]
    if command_name == 'move':
        return pure_robot.move
    elif command_name == 'turn':
        return pure_robot.turn
    elif command_name == 'set':
        return pure_robot.set_state
    elif command_name == 'start':
        return pure_robot.start
    elif command_name == 'stop':
        return pure_robot.stop
    return None


api = RobotApi()
api.setup(command_handler, transfer_to_robot)
api('move 100')
api('turn -90')
api('set soap')
api('start')
api('move 50')
api('stop')
