from robot import Robot

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

cleaner = Robot(transfer_to_robot)
cleaner.execute_commands(commands)