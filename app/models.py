from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class Command:
  @staticmethod
  def from_list(l):
    kind = l[0]
    if kind == 0:
      return AccelerateCommand(ship_id=l[1], vector=tuple(l[2]))
    elif kind == 1:
      return DetonateCommand(ship_id=l[1])
    elif kind == 2:
      return ShootCommand(ship_id=l[1], target=tuple(l[2]), x3=l[3])
    else:
      raise ValueError(f"Unknown command: {l}")

@dataclass
class AccelerateCommand:
  ship_id: int 
  vector: (int, int)

  def to_list(self):
    # (0, shipId, vector)
    return [0, ship_id, list(vector)]

@dataclass
class DetonateCommand:
  ship_id: int 

  def to_list(self):
    # (1, shipId)
    return [1, ship_id]

@dataclass
class ShootCommand:
  ship_id: int 
  target: (int, int)
  x3: Any

  def to_list(self):
    # (2, shipId, target, x3)
    return [2, ship_id, list(target), x3]

@dataclass
class StaticGameInfo:
  x0: Any
  role: int
  x2: Any
  x3: Any
  x4: Any

  @staticmethod
  def from_list(l):
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
    # dirty HACK:
    l += [-1, -1, []]

    # gameState = (gameTick, x1, shipsAndCommands)
    ships = []
    for l in l[2]:
      ship = Ship.from_list(l[0])
      ship.commands = [Command.from_list(c) for c in l[1]]
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
    # (1, gameStage, staticGameInfo, gameState)
    if l == [0]:
      return GameResponse(is_valid=False, game_stage=None, static_game_info=None, game_state=None)
    return GameResponse(
        is_valid = True,
        game_stage = l[1],
        static_game_info = StaticGameInfo.from_list(l[2]),
        game_state = GameState.from_list(l[3]),
      )
