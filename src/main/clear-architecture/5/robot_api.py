from pure_robot import execute_command


def _default_transfer(message):
    print(message)


class RobotCommand:

    def __init__(self, command, initial_state):
        self.command = command
        self.initial_state = initial_state


class RobotApi:
    def __init__(self):
        self._transfer = _default_transfer

    def set_transfer_function(self, transfer_func):
        self._transfer = transfer_func

    def execute(self, robot_command):
        return execute_command(self._transfer, robot_command.command, robot_command.initial_state)
