from enum import Enum
from typing import List, Dict
from dataclasses import dataclass

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

@dataclass
class Cell:
    x: int
    y: int
    cell_type: CellType

@dataclass
class Player:
    name: str
    score: int
    gold: int
    status: PlayerStatus
    bio: str

@dataclass
class GameMap:
    name: str
    width: int
    height: int
    cells: List[Cell]
    description: str

@dataclass
class Battle:
    game_map: GameMap
    players: List[Player]
    status: BattleStatus
    results: Dict[str, BattleResult]

game_map = GameMap(
    name="Small Islands",
    width=3,
    height=3,
    cells=[
        Cell(0, 0, CellType.LAND),
        Cell(1, 0, CellType.LAND),
        Cell(2, 0, CellType.WATER),
        Cell(0, 1, CellType.LAND),
        Cell(1, 1, CellType.WATER),
        Cell(2, 1, CellType.WATER),
        Cell(0, 2, CellType.LAND),
        Cell(1, 2, CellType.LAND),
        Cell(2, 2, CellType.LAND),
    ],
    description="Маленькие острова",
)

player1 = Player(
    name="Player1",
    score=1500,
    gold=500,
    status=PlayerStatus.ONLINE,
    bio="Player1",
)

player2 = Player(
    name="Player2",
    score=1200,
    gold=300,
    status=PlayerStatus.ONLINE,
    bio="Player2",
)

battle = Battle(
    game_map=game_map,
    players=[player1, player2],
    status=BattleStatus.PENDING,
    results={}
)


battle.status = BattleStatus.RUNNING
battle.status = BattleStatus.FINISHED

player1.gold += 200
player1.score += 50

player2.gold -= 10
player2.score -= 5

battle.results = {
    player1.name: BattleResult.WIN,
    player2.name: BattleResult.LOOSE,
}

print("=== GAME MAP ===")
print(game_map)

print("\n=== PLAYERS ===")
print(player1)
print(player2)

print("\n=== BATTLE ===")
print(battle)

player3 = player2

player3.gold = 0

print("\n=== PLAYERS ===")
print(player2)
print(player3)