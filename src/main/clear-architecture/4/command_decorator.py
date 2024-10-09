def command(name=None):
    def decorator(func):
        func.is_command = True
        func.command_name = name if name else func.__name__
        return func
    return decorator