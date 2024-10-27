from cleaning_state import CleaningState
from pure_robot import RobotState


class RobotApi:

    def setup(self, handler_func, transfer_func):
        self.transfer = transfer_func
        self.execute = handler_func

    def make(self, command):
        if not hasattr(self, 'cleaner_state'):
            self.state = RobotState(0.0, 0.0, 0, CleaningState.WATER)
        args = command.strip().split()[1:]

        execute_func = self.execute(command)
        if execute_func is not None:
            self.state = execute_func(self.transfer, args, self.state)

        return self.state

    def __call__(self, command):
        return self.make(command)
