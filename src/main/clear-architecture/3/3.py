import math

# Декоратор для пометки команд
def command(name=None):
    def decorator(func):
        func.is_command = True
        func.command_name = name if name else func.__name__
        return func
    return decorator

def transfer_to_cleaner(message):
    print(message)

class Robot:
    def __init__(self, transfer_func):
        self.__x = 0.0
        self.__y = 0.0
        self.__angle = 0.0
        self.valid_states = ['water', 'soap', 'brush']
        self.state = self.valid_states[0]
        self.transfer = transfer_func

        # Автоматически собрать методы-команды с декоратором @command
        self.command_map = {}
        for attr_name in dir(self):
            method = getattr(self, attr_name)
            if callable(method) and hasattr(method, 'is_command'):
                self.command_map[method.command_name] = method

    @property
    def x(self):
        return int(self.__x)

    @x.setter
    def x(self, value):
        self.__x = int(value)

    @property
    def y(self):
        return int(self.__y)

    @y.setter
    def y(self, value):
        self.__y = int(value)

    @property
    def angle(self):
        return int(self.__angle)

    @angle.setter
    def angle(self, value):
        self.__angle = int(value % 360)

    def execute_commands(self, commands):
        for cmd in commands:
            self.execute_command(cmd)

    def execute_command(self, cmd):
        tokens = cmd.strip().split()
        if not tokens:
            return
        command_name = tokens[0]
        args = tokens[1:]
        command_func = self.command_map.get(command_name)
        if command_func:
            command_func(args)
        else:
            self.transfer(f"Unknown command: {command_name}")

    @command()
    def move(self, args):
        if len(args) != 1:
            self.transfer("Error: 'move' command requires one argument")
            return
        try:
            distance = int(args[0])
        except ValueError:
            self.transfer("Error: 'move' command requires a numeric argument")
            return
        theta_rad = math.radians(self.angle)
        self.x += int(distance * math.cos(theta_rad))
        self.y += int(distance * math.sin(theta_rad))
        self.transfer(f"POS {self.x},{self.y}")

    @command()
    def turn(self, args):
        if len(args) != 1:
            self.transfer("Error: 'turn' command requires one argument")
            return
        try:
            delta_angle = int(args[0])
        except ValueError:
            self.transfer("Error: 'turn' command requires a numeric argument")
            return
        self.angle += delta_angle
        self.transfer(f"ANGLE {self.angle}")

    @command('set')
    def set_state(self, args):
        if len(args) != 1:
            self.transfer("Error: 'set' command requires one argument")
            return
        state = args[0]
        if state not in self.valid_states:
            self.transfer(f"Error: Invalid state '{state}'")
            return
        self.state = state
        self.transfer(f"STATE {self.state}")

    @command()
    def start(self, args):
        self.transfer(f"START WITH {self.state}")

    @command()
    def stop(self, args):
        self.transfer("STOP")

# Пример использования:
commands = [
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
]

robot = Robot(transfer_to_cleaner)
robot.execute_commands(commands)