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
        return tuple(data)
    first, tail = data
    flat_tail = flatten_cons(tail)
    return [flatten_cons(first)] + flat_tail


def player_loop(player):
    print (f'Starting loop for player {player.player_key} ({player.display_name})')

    game_response = player.make_join_request()

    if not game_response.is_valid:
        print("[{player.display_name}] Got invalid response when joining.")
        return
    if game_response.game_stage == GAME_STAGE_HAS_FINISHED:
        print("[{player.display_name}] Game has already finished (but we just joined).")
        return

    game_response = player.make_start_request(game_response)

    while game_response.is_valid and game_response.game_stage != GAME_STAGE_HAS_FINISHED:
        game_response = player.make_commands_request(game_response)

    print(f"[{player.display_name}] loop done.")
    if player.log:
        player.output.close()
        player.space_log.close()

class Proxy:
    def __init__(self, full_url):
        self.full_url = full_url
    
    def create_new_game(self):
        create_new_game_data = [1, 0]
        return self.send(create_new_game_data)

    def send(self, raw_request):
        print()
        print(f"[{threading.current_thread().name}] sending {raw_request}")  # keep to see raw data in server logs
        request = mod(raw_request)
        # print(f"[{threading.current_thread().name}] encoded as {request}")
        res = requests.post(self.full_url, data=request)
        # print(f"[{threading.current_thread().name}] GOT {res}")
        if res.status_code != 200:
            print('Unexpected server response:')
            print('HTTP code:', res.status_code)
            print('Response body:', res.text)
            exit(2)
        raw_response = res.text
        # print(f"[{threading.current_thread().name}] received raw response {raw_response}")
        response = dem(io.StringIO(raw_response))
        # print(f"[{threading.current_thread().name}] decoded as {response}")
        return response


class Player:
    def __init__(self, proxy, key, bot, log=False, display_name=None, ui=None):
        self.player_key = key
        self.bot = bot
        self.log = log
        self.proxy = proxy

        self.ui = ui

        self.output = None
        self.display_name = display_name
        if self.log:
            ts = datetime.utcnow().isoformat()
            self.output = open(f"game-logs/{ts}.txt", "w")
            self.space_log = open("space-log.txt", "w")

    def make_join_request(self):
        print(f"[{self.display_name}] Joining")
        request_data = [2, int(self.player_key), []]
        response = self.proxy.send(request_data)
        
        if self.log:
            self.output.write(f"join: {response}\n")
        
        game_response = GameResponse.from_list(response)
        print(f"[{self.display_name}] Got join response: {game_response}")

        try:
            self.bot.handle_join_response(game_response)
        except:
            traceback.print_stack()

        return game_response

    def make_start_request(self, game_response):
        data = self.bot.get_start_data(game_response)
        print(f"[{self.display_name}] Starting with {data}")
        request_data = [3, int(self.player_key), data]
        response = self.proxy.send(request_data)
        
        if self.log:
            self.space_log.write(f"{response}\n")
            self.output.write(f"start: {response}\n")

        game_response = GameResponse.from_list(response)
        print(f"[{self.display_name}] Got start response: {game_response}")

        try:
            self.bot.handle_start_response(game_response)
        except:
            traceback.print_stack()
            
        if self.ui:
            print(f"updating UI")
            self.ui.append_response(game_response)

        return game_response

    def make_commands_request(self, game_response):
        try:
            commands = self.bot.get_commands(game_response)
        except:
            traceback.print_stack()
            print(f"Bot failed with exception. Just sending no commands to stay alive.")
            commands = []

        print(f"[{self.display_name}] Sending commands: {commands}")
        data = [c.to_list() for c in commands]
        request_data = [4, int(self.player_key), data]
        response = self.proxy.send(request_data)
        
        if self.log:
            self.space_log.write(f"{response}\n")
            self.output.write(f"commands: {response}\n")
        
        game_response = GameResponse.from_list(response)
        print(f"[{self.display_name}] Got commands response: {game_response}")

        if self.ui:
            print(f"updating UI")
            self.ui.append_response(game_response)
        
        return game_response

