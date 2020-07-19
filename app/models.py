import traceback

from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class Command:
  @staticmethod
  def from_list(l, ship_id):
    # print (f"from_list {l}")
    # Example of command from logs: "appliedCommands":[[0,[-1,1]]]
    # the ship_id is implicitly assumed
    kind = l[0]
    try:
      if kind == 0:
        return AccelerateCommand(ship_id=ship_id, vector=tuple(l[1]))
      elif kind == 1:
        return DetonateCommand(ship_id=ship_id)
      elif kind == 2:
        return ShootCommand(ship_id=ship_id, target=tuple(l[1]), x3=l[2])
      else:
        print(f"Command.from_list got unknown command: {l} ship_id={ship_id}")
        return UnknownCommand(ship_id=ship_id, raw_data=l)
    except:
      traceback.print_exc()
      print(f"Command parsing failed. Using UnknownCommand as last resort.")
      return UnknownCommand(ship_id=ship_id, raw_data=l)


@dataclass
class UnknownCommand:
  ship_id: int 
  raw_data: list

@dataclass
class AccelerateCommand:
  ship_id: int 
  vector: (int, int)

  def to_list(self):
    # (0, shipId, vector)
    return [0, self.ship_id, tuple(self.vector)]

@dataclass
class DetonateCommand:
  ship_id: int 

  def to_list(self):
    # (1, shipId)
    return [1, self.ship_id]

@dataclass
class ShootCommand:
  ship_id: int 
  target: (int, int)
  x3: Any

  def to_list(self):
    # (2, shipId, target, x3)
    return [2, self.ship_id, tuple(self.target), self.x3]

@dataclass
class StaticGameInfo:
  x0: Any
  role: int
  x2: Any
  x3: Any
  x4: Any

  @staticmethod
  def from_list(l):
    # print(f"StaticGameInfo {l}")
    if not l:
      return StaticGameInfo(
        x0 = None,
        role = None,
        x2 = None,
        x3 = None,
        x4 = None,
      )  
    # staticGameInfo = (x0, role, x2, x3, x4)
    return StaticGameInfo(
        x0 = l[0],
        role = l[1],
        x2 = l[2],
        x3 = l[3],
        x4 = l[4],
      )  

SHIP_ROLE_ATTACKER=0
SHIP_ROLE_DEFENDER=1

@dataclass
class Ship:
  role: int
  ship_id: int
  position: (int, int)
  velocity: (int, int)
  x4: int
  x5: int
  x6: int
  x7: int
  commands: list = None

  @staticmethod
  def from_list(l):
    # ship = (role, shipId, position, velocity, x4, x5, x6, x7)
    return Ship(
        role = l[0],
        ship_id = l[1],
        position = tuple(l[2]),
        velocity = tuple(l[3]),
        x4 = l[4],
        x5 = l[5],
        x6 = l[6],
        x7 = l[7],
      )

@dataclass
class GameState:
  game_tick: int
  x1: Any
  ships: list

  @staticmethod
  def from_list(l):
    if not l:
      return GameState(game_tick=None, x1=None, ships=[])

    # gameState = (gameTick, x1, shipsAndCommands)
    ships = []
    for ship_list in l[2]:
      ship = Ship.from_list(ship_list[0])
      # print (f"ship list: {ship_list}")
      # print (f"ship: {ship}")
      # print (f"appliedCommands: {ship_list[1]}")
      ship.commands = [Command.from_list(c, ship_id=ship.ship_id) for c in ship_list[1]]
      ships.append(ship)
    return GameState(
        game_tick = l[0],
        x1 = l[1],
        ships = ships
      )


GAME_STAGE_NOT_STARTED=0
GAME_STAGE_HAS_STARTED=1
GAME_STAGE_HAS_FINISHED=2

@dataclass
class GameResponse:
  is_valid: bool
  game_stage: Optional[int]
  static_game_info: Optional[StaticGameInfo]
  game_state: Optional[GameState]

  @staticmethod
  def from_list(l):
    print(f"Parsing GameResponse {l}")  # keep to see raw data in server logs
    # (1, gameStage, staticGameInfo, gameState)
    if l == [0]:
      return GameResponse(is_valid=False, game_stage=None, static_game_info=None, game_state=None)
    return GameResponse(
        is_valid = True,
        game_stage = l[1],
        static_game_info = StaticGameInfo.from_list(l[2]) if l[2] else None,
        game_state = GameState.from_list(l[3]) if l[3] else None,
      )


if __name__ == "__main__":
  # input =  [1, 1, [256, 0, [512, 1, 64], [16, 128], [1, 1, 1, 1]], [1, [16, 128], [[[1, 0, [46, 32], [-2, 1], [0, 1, 1, 1], 7, 64, 1], [[0, [1, -1]]]], [[0, 1, [-48, -30], [0, 1], [0, 1, 1, 1], 7, 64, 1], [[0, [1, -1]]]]]]]
  # print (GameResponse.from_list(input))
  input = [3, [32, 32, 5, 2]]
  print(Command.from_list(input, 0))