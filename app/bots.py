from models import *

class Bot:
    def handle_join_response(self, game_response):
        self.role = game_response.static_game_info.role
        print(f"Detected role as {self.role}")

    def handle_start_response(self, game_response):
        self.ship_id = None
        for ship in game_response.game_state.ships:
            if ship.role == self.role:
                self.ship_id = ship.ship_id
                break
        print(f"Detected ship ID as {self.ship_id}")
        if self.ship_id is None:
            raise ValueError(f"Failed to find ship id in {game_response} with role {self.role}")


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

        return [1, 1, 1, 1]

    def get_commands(self, game_response: GameResponse):
        # default: do nothing
        return [
            # AccelerateCommand
        ]