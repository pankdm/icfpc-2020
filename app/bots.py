from models import *

class Bot:
    def handle_join_response(self, game_response):
        if not game_response.is_valid or game_response.game_stage == GAME_STAGE_HAS_FINISHED:
            print(f"Skipping role detection for {game_response}")
            return

        self.role = game_response.static_game_info.role
        print(f"Detected role as {self.role}")

    def handle_start_response(self, game_response):
        if not game_response.is_valid or game_response.game_stage == GAME_STAGE_HAS_FINISHED:
            print(f"Skipping ship ID detection for {game_response}")
            return

        self.ship_id = None
        for ship in game_response.game_state.ships:
            if ship.role == self.role:
                self.ship_id = ship.ship_id

        print(f"Detected ship ID as {self.ship_id}")

        if self.ship_id is None:
            raise ValueError(f"Failed to find initial ship IDs in {game_response} with role {self.role}")

    def get_other_ship_ids(self, game_response):
        return [
            ship.ship_id 
            for ship in game_response.game_state.ships
            if ship.ship_id != self.ship_id
        ]

class DoNothingBot(Bot):
    def get_start_data(self, game_response: GameResponse):
        # default: not sure what it means
        return [64, 48, 14, 1] # [446, 0, 0, 1]
        # return [1, 1, 1, 1]

    def get_commands(self, game_response: GameResponse):
        # default: do nothing
        return []


class NaiveBot(Bot):
    def get_start_data(self, game_response: GameResponse):
        return [1, 1, 1, 1]

    def get_commands(self, game_response: GameResponse):
        # default: do nothing
        return []

class BasicFlyingHelper:
    def __init__(self, bot):
        self.bot = bot

    def get_commands(self, game_response: GameResponse, ship_id: int):
        """Issues commands to keep the given ship flying."""
        x, y = game_response.get_ship(ship_id).position

        if abs(x) > 47 or abs(y) > 47:
            # Just cool down
            return []
        else:
            x = -1 if x > 0 else 1
            y = -1 if y > 0 else 1

        return [
            AccelerateCommand(ship_id=ship_id, vector=(x, y))
        ]

class FlyingBot(Bot):
    def __init__(self):
        self.flying_helper = BasicFlyingHelper(self)

    def get_start_data(self, game_response: GameResponse):
        return [100, 10, 10, 1]

    def get_commands(self, game_response: GameResponse):
        return self.flying_helper.get_commands(game_response, self.ship_id)

class ShootAheadHelper:
    def __init__(self, bot):
        self.bot = bot

    def get_commands(self, game_response: GameResponse, shooter_ship_id: int, target_ship_id: int):
        target_ship = game_response.get_ship(target_ship_id)
        other_position = target_ship.position
        other_velocity = target_ship.velocity
        target = (
            other_position[0] + other_velocity[0],
            other_position[1] + other_velocity[1],
        )
        return [
            ShootCommand(ship_id=shooter_ship_id, target=target, x3=48)
        ]


class ShooterBot(Bot):
    def __init__(self):
        self.flying_helper = BasicFlyingHelper(self)
        self.shoot_ahead_helper = ShootAheadHelper(self)

    def get_start_data(self, game_response: GameResponse):
        return [64, 48, 14, 1]

    def get_commands(self, game_response: GameResponse):
        target_ship_id = self.get_other_ship_ids(game_response)[0]
        return (
            self.flying_helper.get_commands(game_response, ship_id=self.ship_id) + 
            self.shoot_ahead_helper.get_commands(game_response, shooter_ship_id=self.ship_id, target_ship_id=target_ship_id)
        )
        