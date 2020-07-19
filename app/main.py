import io
import requests
import sys

from modulate import modulate as mod
from parse_modulated import parse as dem

GAME_STAGE_NOT_STARTED=0
GAME_STAGE_HAS_STARTED=1
GAME_STAGE_HAS_FINISHED=2

def get_nth_element(l, index):
    if l is None:
        return None
    if index == 0:
        return l[0]
    return get_nth_element(l[1], index - 1)

def send(server_url, raw_request):
    print(f"sending {raw_request}")
    request = mod(raw_request)
    print(f"encoded as {request}")
    res = requests.post(server_url + "/aliens/send", data=request)
    if res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('Response body:', res.text)
        exit(2)
    raw_response = res.text
    print(f"received raw response {raw_response}")
    response = dem(io.StringIO(raw_response))
    print(f"decoded as {response}")
    return response

def make_join_request(player_key):
    return [2, int(player_key), []]

def make_start_request(player_key, game_response):
    return [3, int(player_key), [1, 1, 1, 1]]

def make_commands_request(player_key, game_response):
    return [4, int(player_key), []]

def get_game_stage(game_response):
    if game_response[0] != 1:
        raise ValueError("GameResponse is malformed, expecting first element to be 1: %s" % game_response)
    return get_nth_element(game_response, 1)


def main():
    server_url = sys.argv[1]
    player_key = sys.argv[2]
    print('ServerUrl: %s; PlayerKey: %s' % (server_url, player_key))

    # make valid JOIN request using the provided playerKey.
    join_request = make_join_request(player_key)

    # send it to aliens and get the GameResponse
    game_response = send(server_url, join_request)

    if get_game_stage(game_response) == GAME_STAGE_HAS_FINISHED:
        print("Game has already finished, quitting.")
        exit(0)

    # make valid START request using the provided playerKey and gameResponse returned from JOIN
    start_request = make_start_request(player_key, game_response)

    # send it to aliens and get the updated GameResponse
    game_response = send(server_url, start_request)

    while get_game_stage(game_response) != GAME_STAGE_HAS_FINISHED:
        # make valid COMMANDS request using the provided playerKey and gameResponse returned from START or previous COMMANDS
        commands_request = make_commands_request(player_key, game_response)

        # send it to aliens and get the updated GameResponse
        game_response = send(server_url, commands_request)

    print("Done.")

if __name__ == '__main__':
    main()
