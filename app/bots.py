from models import *

class DoNothingBot:
    def get_start_data(self, game_response: GameResponse):
        # default: not sure what it means
        return [446, 0, 0, 1]
        # return [1, 1, 1, 1]

    def get_commands(self, game_response: GameResponse):
        # default: do nothing
        return []


class NaiveBot:
    def get_start_data(self, game_response: GameResponse):
        return [1, 1, 1, 1]

    def get_commands(self, game_response: GameResponse):
        # default: do nothing
        return []