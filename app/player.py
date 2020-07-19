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


def join_and_play_the_game(key, bot, proxy, name):
    player = Player(key, bot, proxy=proxy, log=True, display_name=name)
    player_loop(player)

def player_loop(player):
    print (f'Starting loop for player {player.player_key} ({player.display_name})')

    game_response = player.make_join_request()
    print(f"[{player.display_name}] Joined parsed response: {game_response}")
    if not game_response.is_valid:
        print("[{player.display_name}] Got invalid response")
        return
    if game_response.game_stage == GAME_STAGE_HAS_FINISHED:
        print("[{player.display_name}] Game has already finished.")
        return

    game_response = player.make_start_request(game_response)
    print(f"[{player.display_name}] Start parsed response: {game_response}")

    while game_response.is_valid and game_response.game_stage != GAME_STAGE_HAS_FINISHED:
        game_response = player.make_commands_request(game_response)
        print(f"[{player.display_name}] Commands parsed response: {game_response}")

class Proxy:
    def __init__(self, full_url):
        self.full_url = full_url
    
    def create_new_game(self):
        create_new_game_data = [1, 0]
        return self.send(create_new_game_data)

    def send(self, raw_request):
        print()
        # print(f"sending {raw_request}")
        request = mod(raw_request)
        # print(f"encoded as {request}")
        res = requests.post(full_url, data=request)
        if res.status_code != 200:
            print('Unexpected server response:')
            print('HTTP code:', res.status_code)
            print('Response body:', res.text)
            exit(2)
        raw_response = res.text
        # print(f"received raw response {raw_response}")
        response = dem(io.StringIO(raw_response))
        # print(f"decoded as {response}")
        flat = flatten_cons(response)
        # print(f"flattened response: {flat}")
        return flat


class Player:
    def __init__(self, player_key, bot, proxy, log=False, display_name=None):
        self.player_key = player_key
        self.bot = bot
        self.log = log
        self.proxy = proxy

        self.output = None
        self.display_name = display_name
        if self.log:
            ts = datetime.utcnow().isoformat()
            self.output = open(f"game-logs/{ts}.txt", "w")

    def make_join_request(self):
        print(f"[{self.display_name}] Joining")
        request_data = [2, int(self.player_key), []]
        response = self.proxy.send(request_data)
        if self.log:
            self.output.write(f"join: {response}\n")
        
        game_response = GameResponse.from_list(response)
        self.bot.handle_join_response(game_response)

        return game_response

    def make_start_request(self, game_response):
        data = self.bot.get_start_data(game_response)
        print(f"[{self.display_name}] Starting with {data}")
        request_data = [3, int(self.player_key), data]
        response = self.proxy.send(request_data)
        if self.log:
            self.output.write(f"start: {response}\n")

        game_response = GameResponse.from_list(response)
        self.bot.handle_start_response(game_response)

        return game_response

    def make_commands_request(self, game_response):
        commands = self.bot.get_commands(game_response)
        print(f"[{self.display_name}] Sending commands: {commands}")
        data = [c.to_list() for c in commands]
        request_data = [4, int(self.player_key), data]
        response = self.proxy.send(request_data)
        if self.log:
            self.output.write(f"commands: {response}\n")
        return GameResponse.from_list(response)

