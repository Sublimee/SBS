from cleaning_state import CleaningState
from command_decorator import command_map
from pure_robot import RobotState


def _default_transfer(message):
    print(message)


class RobotApi:
    def __init__(self):
        self.stack = [RobotState(0.0, 0.0, 0, CleaningState.WATER)]
        self._transfer = _default_transfer

    def set_transfer_function(self, transfer_func):
        self._transfer = transfer_func

    def execute(self, commands):
        tokens = commands.strip().split()
        for token in tokens:
            self.handle_token(token)
        return self.stack[0]

    def handle_token(self, token):
        command = command_map.get(token)
        if command:
            args, current_state = self.pop_args_until_state()
            if current_state is None:
                self._transfer(f"Error: No RobotState found on stack for command '{token}'")
                return
            new_state = command(self._transfer, args, current_state)
            self.stack.append(new_state)
        else:
            self.stack.append(token)

    def pop_args_until_state(self):
        args = []
        while self.stack:
            item = self.stack.pop()
            if isinstance(item, RobotState):
                return args, item
            else:
                args.insert(0, item)
        return None, None
