from enum import Enum

class PlayerStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"

class Player:
    def __init__(self, name: str, gold: int, status: PlayerStatus, bio: str):
        self.__name = name
        self.__gold = gold
        self.__status = status
        self.__bio = bio

    def get_name(self):
        return self.__name

    def reward(self, amount: int):
        if amount > 0:
            self.__gold += amount

    def go_online(self):
        self.__status = PlayerStatus.ONLINE

    def go_offline(self):
        self.__status = PlayerStatus.OFFLINE

    def get_summary(self) -> str:
        return f"{self.__name}, [gold={self.__gold}, status={self.__status.value}]. About: {self.__bio}"