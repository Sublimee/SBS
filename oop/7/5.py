from engine.world.battle import Battle, BattleStatus, BattleResult
from engine.world.game_map import GameMap, LandCell, WaterCell
from engine.player.player import PlayerStatus, Player
from datetime import datetime

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


now = datetime.now()

print("=== BATTLE STARTED ===")
print(f"It's: {now:%H:%M:%S} of {now:%d.%m.%Y}")

print(f"Battle status: {battle.get_status()}")

player1.reward(200)
player1.reward(500)

print("=== PLAYERS DURING BATTLE ===")
print(player1.get_summary())
print(player2.get_summary())

battle.set_result(player1, BattleResult.WIN)
battle.set_result(player2, BattleResult.LOOSE)

battle.finish()

print("=== BATTLE FINISHED ===")
print(f"Battle status: {battle.get_status()}")
print(f"Winners: battle.get_winners()")

print("=== EVENT LOG ===")
for event in battle.get_event_log():
    print("-", event.get_message())