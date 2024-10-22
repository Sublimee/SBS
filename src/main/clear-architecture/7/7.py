from robot import Robot, RobotInterface


def transfer_to_robot(message):
    print(message)


commands = [
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
]

robot: RobotInterface = Robot(transfer_to_robot)
robot.execute_commands(commands)