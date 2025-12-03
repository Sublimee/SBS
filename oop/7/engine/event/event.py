class Event:
    def __init__(self, message: str):
        self._message = message

    def get_message(self) -> str:
        return self._message

    def get_kind(self) -> str:
        return "event"


class SystemEvent(Event):
    def get_kind(self) -> str:
        return "system"


