from datetime import datetime
import io
import requests
import sys
import threading

import io
import requests
import sys
import threading

from modulate import modulate as mod
from parse_modulated import parse as dem

from bots import *
from models import *

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


def player_loop(player):
    print (f'Starting loop for player {player.player_key}')
    game_response = player.make_join_request()
    print(f"Joined parsed response: {game_response}")
    if not game_response.is_valid:
        print("Got invalid response")
        return
    if game_response.game_stage == GAME_STAGE_HAS_FINISHED:
        print("Game has already finished.")
        return
    game_response = player.make_start_request(game_response)
    print(f"Start parsed response: {game_response}")
    while game_response.is_valid and game_response.game_stage != GAME_STAGE_HAS_FINISHED:
        game_response = player.make_commands_request(game_response)
        print(f"Commands parsed response: {game_response}")

def get_create_data():
    return [1, 0]

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
