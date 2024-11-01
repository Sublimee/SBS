class StateMonad:
    def __init__(self, state, outputs=None):
        self.state = state
        self.outputs = outputs or []

    def bind(self, func):
        new_state, result = func(self.state)
        new_outputs = self.outputs + [result]
        return StateMonad(new_state, new_outputs)

    def __rshift__(self, func):
        return self.bind(func)