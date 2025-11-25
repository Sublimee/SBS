from enum import Enum
from typing import List, Dict, Optional


class BattleStatus(Enum):
    PENDING = "pending"  # ещё не началась
    RUNNING = "running"  # в процессе
    FINISHED = "finished"  # завершена


class PlayerStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"


class CellType(Enum):
    LAND = "land"
    WATER = "water"


class BattleResult(Enum):
    LOOSE = "loose"
    DRAW = "draw"
    WIN = "win"


class Cell:
    def __init__(self, x: int, y: int, cell_type: CellType):
        self.__x = x
        self.__y = y
        self._cell_type = cell_type

    def get_coords(self) -> tuple[int, int]:
        return self.__x, self.__y

    def get_type(self) -> CellType:
        return self._cell_type


class WaterCell(Cell):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, CellType.WATER)


class LandCell(Cell):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, CellType.LAND)


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


class GameMap:
    def __init__(self, name: str, width: int, height: int, cells: List[Cell], description: str):
        self.__name = name
        self.__width = width
        self.__height = height
        self.__cells = cells
        self.__description = description

    def get_optional_cell(self, x: int, y: int) -> Optional[Cell]:
        for cell in self.__cells:
            coords = cell.get_coords()
            if coords[0] == x and coords[1] == y:
                return cell
        return None

    def get_cell(self, x: int, y: int) -> Cell:
        cell = self.get_optional_cell(x, y)
        if cell is None:
            raise ValueError(f"No cell at ({x}, {y})")
        return cell

    def get_area(self) -> int:
        return self.__width * self.__height

    def is_water(self, x: int, y: int) -> bool:
        return self.get_cell(x, y).get_type() == CellType.WATER

    def is_land(self, x: int, y: int) -> bool:
        return self.get_cell(x, y).get_type() == CellType.LAND

    def print_map(self):
        for y in range(self.__height):
            for x in range(self.__width):
                if self.__cells[y * self.__width + x].get_type() == CellType.LAND:
                    print('L', end='')
                else:
                    print('W', end='')
            print('')


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


cells = [
    LandCell(0, 0),
    LandCell(1, 0),
    WaterCell(2, 0),
    LandCell(0, 1),
    WaterCell(1, 1),
    WaterCell(2, 1),
    LandCell(0, 2),
    LandCell(1, 2),
    LandCell(2, 2),
]

game_map = GameMap(
    name="Small Islands",
    width=3,
    height=3,
    cells=cells,
    description="Маленькие острова",
)

player1 = Player(
    name="Player1",
    gold=500,
    status=PlayerStatus.ONLINE,
    bio="Player1",
)

player2 = Player(
    name="Player2",
    gold=300,
    status=PlayerStatus.ONLINE,
    bio="Player2",
)

battle = Battle(
    game_map=game_map,
    players=[player1, player2],
    status=BattleStatus.PENDING,
)

print("=== GAME MAP ===")
game_map.print_map()

print("=== PLAYERS BEFORE BATTLE ===")
print(player1.get_summary())
print(player2.get_summary())

battle.start()
player1.go_online()
player2.go_online()

print("=== BATTLE STARTED ===")
print("Battle status:", battle.get_status())

player1.reward(200)
player1.reward(500)

print("=== PLAYERS DURING BATTLE ===")
print(player1.get_summary())
print(player2.get_summary())

battle.set_result(player1, BattleResult.WIN)
battle.set_result(player2, BattleResult.LOOSE)

battle.finish()

print("=== BATTLE FINISHED ===")
print("Battle status:", battle.get_status())
print("Winners:", battle.get_winners())

print("=== EVENT LOG ===")
for event in battle.get_event_log():
    print("-", event.get_message())