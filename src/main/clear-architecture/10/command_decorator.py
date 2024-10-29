command_map = {}

def command(name=None):
    def decorator(func):
        command_name = name if name else func.__name__
        command_map[command_name] = func
        return func
    return decorator