class RobotCommand:

    def __init__(self, command, initial_state):
        self.command = command
        self.initial_state = initial_state


class RobotApi:

    def __init__(self, move_func, turn_func, set_state_func, start_func, stop_func, transfer_func):
        self.move_func = move_func
        self.turn_func = turn_func
        self.set_state_func = set_state_func
        self.start_func = start_func
        self.stop_func = stop_func
        self.transfer_func = transfer_func

    def execute_command(self, robot_command):
        tokens = robot_command.command.strip().split()
        command_name = tokens[0]
        args = tokens[1:]
        state = robot_command.initial_state
        if command_name == 'move':
            return self.move_func(self.transfer_func, args, state)
        elif command_name == 'turn':
            return self.turn_func(self.transfer_func, args, state)
        elif command_name == 'set':
            return self.set_state_func(self.transfer_func, args, state)
        elif command_name == 'start':
            return self.start_func(self.transfer_func, args, state)
        elif command_name == 'stop':
            return self.stop_func(self.transfer_func, args, state)
