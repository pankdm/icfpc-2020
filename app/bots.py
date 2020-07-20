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
        self.other_ship_ids = []
        for ship in game_response.game_state.ships:
            if ship.role == self.role:
                self.ship_id = ship.ship_id
            else:
                self.other_ship_ids.append(ship.ship_id)
        self.other_ship_id = self.other_ship_ids[0]

        print(f"Detected ship ID as {self.ship_id}")
        print(f"Detected other ship IDs as {self.other_ship_ids}")

        if self.ship_id is None or self.other_ship_id is None:
            raise ValueError(f"Failed to find at least 2 ship IDs in {game_response} with role {self.role}")

class DoNothingBot(Bot):
    def get_start_data(self, game_response: GameResponse):
        # default: not sure what it means
        return [446, 0, 0, 1]
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

class FlyingBot(Bot):
    def get_start_data(self, game_response: GameResponse):
        return [100, 10, 10, 1]

    def get_commands(self, game_response: GameResponse):
        x, y = game_response.get_ship(self.ship_id).position

        if abs(x) > 47 or abs(y) > 47:
            # Just cool down
            return []
        else:
            x = -1 if x > 0 else 1
            y = -1 if y > 0 else 1

        return [
            AccelerateCommand(ship_id=self.ship_id, vector=(x, y))
        ]

class ShooterBot(Bot):
    def get_start_data(self, game_response: GameResponse):
        return [64, 48, 14, 1]

    def get_commands(self, game_response: GameResponse):
        other_position = game_response.get_ship(self.other_ship_id).position
        other_velocity = game_response.get_ship(self.other_ship_id).velocity
        target = (
            other_position[0] + other_velocity[0],
            other_position[1] + other_velocity[1],
        )
        return [
            # AccelerateCommand(ship_id=self.ship_id, vector=(-1, 1)),
            ShootCommand(ship_id=self.ship_id, target=target, x3=86)
        ]