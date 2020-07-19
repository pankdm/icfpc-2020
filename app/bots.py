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
            else:
                self.other_ship_id = ship.ship_id
        print(f"Detected ship ID as {self.ship_id}")
        print(f"Detected other ship ID as {self.other_ship_id}")
        if self.ship_id is None or self.other_ship_id is None:
            raise ValueError(f"Failed to find ship IDs in {game_response} with role {self.role}")

    def get_my_position(self, game_response):
        position = None
        for ship in game_response.game_state.ships:
            if ship.ship_id == self.ship_id:
                position = ship.position
        return position

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
        position = self.get_my_position(game_response)
        if position is None:
            return []

        x, y = position

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
        return [133,64,10,1]

    def get_commands(self, game_response: GameResponse):
        # default: do nothing
        target = (0,0)
        for ship in game_response.game_state.ships:
            if ship.ship_id == self.other_ship_id:
                target = ship.position
        return [
            ShootCommand(ship_id=self.other_ship_id, target=target, x3=[64,70,4])
        ]        