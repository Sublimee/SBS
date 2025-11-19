from enum import Enum
from typing import List, Dict, Optional

class BattleStatus(Enum):
    PENDING = "pending"      # ещё не началась
    RUNNING = "running"      # в процессе
    FINISHED = "finished"    # завершена

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
        self.x = x
        self.y = y
        self.cell_type = cell_type

    def is_land(self) -> bool:
        return self.cell_type == CellType.LAND

    def is_water(self) -> bool:
        return self.cell_type == CellType.WATER

    def get_coords(self) -> tuple[int, int]:
        return self.x, self.y

class Player:
    def __init__(self, name: str, gold: int, status: PlayerStatus, bio: str):
        self.name = name
        self.gold = gold
        self.status = status
        self.bio = bio

    def reward(self, amount: int):
        if amount > 0:
            self.gold += amount

    def go_online(self):
        self.status = PlayerStatus.ONLINE

    def go_offline(self):
        self.status = PlayerStatus.OFFLINE

    def get_summary(self) -> str:
        return f"{self.name}, [gold={self.gold}, status={self.status.value}]. About: {self.bio}"

class GameMap:
    def __init__(self, name: str, width: int, height: int, cells: List[Cell], description: str):
        self.name = name
        self.width = width
        self.height = height
        self.cells = cells
        self.description = description

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        for cell in self.cells:
            if cell.x == x and cell.y == y:
                return cell
        return None

    def get_area(self) -> int:
        return self.width * self.height

    def is_water(self, x: int, y: int) -> bool:
        cell = self.get_cell(x, y)
        if cell is None:
            raise ValueError(f"No cell at ({x}, {y})")
        return cell.is_water()

    def is_land(self, x: int, y: int) -> bool:
        cell = self.get_cell(x, y)
        if cell is None:
            raise ValueError(f"No cell at ({x}, {y})")
        return cell.is_land()

class Battle:
    def __init__(self, game_map: GameMap, players: List[Player], status: BattleStatus = BattleStatus.PENDING):
        self.game_map = game_map
        self.players = players
        self.status = status
        self.results: Dict[str, BattleResult] = {}
        self.event_log: List[str] = []

    def start(self) -> None:
        if self.status == BattleStatus.PENDING:
            self.status = BattleStatus.RUNNING
            self.event_log.append("Битва началась.")
        else:
            self.event_log.append(f"Нельзя стартовать битву, находящуюся в статусе {self.status}.")

    def finish(self) -> None:
        if self.status == BattleStatus.RUNNING:
            self.status = BattleStatus.FINISHED
            self.event_log.append("Битва завершена.")
        else:
            self.event_log.append("Нельзя завершить битву, находящуюся в статусе {self.status}.")

    def set_result(self, player: Player, result: BattleResult) -> None:
        self.results[player.name] = result
        self.event_log.append(f"Результат игрока {player.name}: {result.value}")

    def get_winners(self) -> List[str]:
        return [name for name, game_result in self.results.items() if game_result == BattleResult.WIN]


cells = [
    Cell(0, 0, CellType.LAND),
    Cell(1, 0, CellType.LAND),
    Cell(2, 0, CellType.WATER),
    Cell(0, 1, CellType.LAND),
    Cell(1, 1, CellType.WATER),
    Cell(2, 1, CellType.WATER),
    Cell(0, 2, CellType.LAND),
    Cell(1, 2, CellType.LAND),
    Cell(2, 2, CellType.LAND),
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

print("=== PLAYERS BEFORE BATTLE ===")
print(player1.get_summary())
print(player2.get_summary())

# Стартуем битву
battle.start()
player1.go_online()
player2.go_online()

print("=== BATTLE STARTED ===")
print("Battle status:", battle.status)


player1.reward(200)
player1.reward(500)

print("=== PLAYERS DURING BATTLE ===")
print(player1.get_summary())
print(player2.get_summary())

battle.set_result(player1, BattleResult.WIN)
battle.set_result(player2, BattleResult.LOOSE)

battle.finish()

print("=== BATTLE FINISHED ===")
print("Battle status:", battle.status)
print("Winners:", battle.get_winners())

print("=== EVENT LOG ===")
for event in battle.event_log:
    print("-", event)