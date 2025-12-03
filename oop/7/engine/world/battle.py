from enum import Enum
from typing import List, Dict
from .game_map import GameMap
from ..player.player import Player
from ..event.event import Event, SystemEvent

class BattleStatus(Enum):
    PENDING = "pending"  # ещё не началась
    RUNNING = "running"  # в процессе
    FINISHED = "finished"  # завершена

class BattleResult(Enum):
    LOOSE = "loose"
    DRAW = "draw"
    WIN = "win"

class ResultEvent(Event):
    def __init__(self, player_name: str, result: BattleResult):
        message = f"Результат игрока {player_name}: {result.value}"
        super().__init__(message)
        self._player_name = player_name
        self._result = result

def get_result(self) -> BattleResult:
    return self._result

def get_kind(self) -> str:
    return "result"

class Battle:
    def __init__(self, game_map: GameMap, players: List[Player], status: BattleStatus = BattleStatus.PENDING):
        self.__game_map = game_map
        self.__players = players
        self.__status = status
        self.__results: Dict[str, BattleResult] = {}
        self.__event_log: List[Event] = []

    def get_status(self) -> BattleStatus:
        return self.__status

    def get_event_log(self) -> List[Event]:
        return self.__event_log

    def start(self) -> None:
        if self.__status == BattleStatus.PENDING:
            self.__status = BattleStatus.RUNNING
            self.__event_log.append(SystemEvent("Битва началась."))
        else:
            self.__event_log.append(
                SystemEvent(f"Нельзя стартовать битву, находящуюся в статусе {self.__status}.")
            )

    def finish(self) -> None:
        if self.__status == BattleStatus.RUNNING:
            self.__status = BattleStatus.FINISHED
            self.__event_log.append(SystemEvent("Битва завершена."))
        else:
            self.__event_log.append(SystemEvent("Нельзя завершить битву, находящуюся в статусе {self.status}."))

    def set_result(self, player: Player, result: BattleResult) -> None:
        self.__results[player.get_name()] = result
        self.__event_log.append(ResultEvent(player.get_name(), result))

    def get_winners(self) -> List[str]:
        return [name for name, game_result in self.__results.items() if game_result == BattleResult.WIN]
