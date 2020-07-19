
from datetime import datetime
import io
import requests
import sys
import threading

from modulate import modulate as mod
from parse_modulated import parse as dem
from bots import *
from models import *


from main import (
    make_join_request,
    make_start_request,
    make_commands_request
)


def make_create_request():
    return [1, 0]


def flatten_cons(data):
    # print (f"flattening {data}")
    if data is None:
        return []
    if isinstance(data, int):
        return data
    if len(data) == 2 and isinstance(data[0], int) and isinstance(data[1], int):
        return data
    first, tail = data
    flat_tail = flatten_cons(tail)
    return [flatten_cons(first)] + flat_tail


def send_to_proxy(raw_request):
    print()
    print(f"sending {raw_request}")
    request = mod(raw_request)
    print(f"encoded as {request}")
    server_url = "https://icfpc2020-api.testkontur.ru"
    api_key = "apiKey=6e1336a2ffa94971b5f74715a85708b9"
    res = requests.post(f'{server_url}/aliens/send?{api_key}', data=request)
    if res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('Response body:', res.text)
        exit(2)
    raw_response = res.text
    print(f"received raw response {raw_response}")
    response = dem(io.StringIO(raw_response))
    print(f"decoded as {response}")
    flat = flatten_cons(response)
    print(f"flattened: {flat}")
    return flat

class Player:
    def __init__(self, player_key, bot, log=False):
        self.player_key = player_key
        self.bot = bot
        self.log = log
        self.output = None
        if self.log:
            ts = datetime.utcnow().isoformat()
            self.output = open(f"game-logs/{ts}.txt", "w")

    def make_join_request(self):
        request_data = [2, int(self.player_key), []]
        response = send_to_proxy(request_data)
        if self.log:
            self.output.write(f"join: {response}\n")
        return GameResponse.from_list(response)

    def make_start_request(self, game_response):
        data = self.bot.get_start_data(game_response)
        request_data = [3, int(self.player_key), data]
        response = send_to_proxy(request_data)
        if self.log:
            self.output.write(f"start: {response}\n")
        return GameResponse.from_list(response)

    def make_commands_request(self, game_response):
        commands = self.bot.get_commands(game_response)
        data = [c.to_list() for c in commands]
        request_data = [4, int(self.player_key), data]
        response = send_to_proxy(request_data)
        if self.log:
            self.output.write(f"commands: {response}\n")
        return GameResponse.from_list(response)


def get_game_stage(game_response):
    if game_response[0] != 1:
        raise ValueError("GameResponse is malformed, expecting first element to be 1: %s" % game_response)
    return game_response[1]

def player_loop(player):
    print (f'Starting loop for player {player.player_key}')
    game_response = player.make_join_request()
    if not game_response.is_valid:
        print("Got invalid response")
        return
    if game_response.game_stage == GAME_STAGE_HAS_FINISHED:
        print("Game has already finished.")
        return
    game_response = player.make_start_request(game_response)
    while game_response.is_valid and game_response.game_stage != GAME_STAGE_HAS_FINISHED:
        game_response = player.make_commands_request(game_response)


def main():
    # a = [1, [[[0, [8278679430195342144, None]], [[1, [8541530479718220884, None]], None]], None]]
    # print (flatten_cons(a))
    # a = [1, [1, [[256, [0, [[512, [1, [64, None]]], [[16, [128, None]], [[446, [0, [0, [1, None]]]], None]]]]], [[0, [[16, [128, None]], [[[[1, [0, [[-48, -29], [[0, 0], [[446, [0, [0, [1, None]]]], [0, [64, [1, None]]]]]]]], [None, None]], [[[0, [1, [[48, 29], [[0, 0], [[446, [0, [0, [1, None]]]], [0, [64, [1, None]]]]]]]], [None, None]], None]], None]]], None]]]]
    # print (flatten_cons(a))
    # return

    # if sys.argv[1] == "create":
    #     create = send_to_proxy(make_create_request())
    #     print (create)
    #     key1 = create[1][0][1]
    #     key2 = create[1][1][1]
    #     print (f'joining as key1: {key1}')
    #     print (f'key2: {key2}')

    #     bot = DoNothingBot()
    #     player = Player(key1, bot, log=True)
    #     player_loop(player)
    #     player.output.close()
    # if sys.argv[1] == "join":
    #     key = sys.argv[2]

    #     bot = DoNothingBot()
    #     player = Player(key, bot)
    #     player_loop(player)
    # bot2 = DoNothingBot()
    # assert False, f"invalid usage: {sys.argv}"

    create = send_to_proxy(make_create_request())
    print (create)
    key1 = create[1][0][1]
    key2 = create[1][1][1]

    bot1 = DoNothingBot()
    player1 = Player(key1, bot1, log=True)

    bot2 = DoNothingBot()
    player2 = Player(key2, bot1, log=True)

    t = threading.Thread(target=player_loop, args=(player1,))
    t.start()

    player_loop(player2)


if __name__ == '__main__':
    main()


