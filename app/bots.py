

class DoNothingBot:
    def get_start_data(self, game_response):
        # default: not sure what it means
        return [446, 0, 0, 1]
        # return [1, 1, 1, 1]

    def get_commands_data(self, game_response):
        # default: do nothing
        return []


class NaiveBot:
    def get_start_data(self, game_response):
        return [1, 1, 1, 1]

    def get_commands_data(self, game_response):
        # default: do nothing
        return []