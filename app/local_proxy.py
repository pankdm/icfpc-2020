
from datetime import datetime
import io
import requests
import sys
import threading

from modulate import modulate as mod
from parse_modulated import parse as dem
from bots import *
from models import *
from player import *


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

    create = send_to_proxy(get_create_data())
    print (create)
    key1 = create[1][0][1]
    key2 = create[1][1][1]

    bot1 = DoNothingBot()
    player1 = Player(key1, bot1, log=True, display_name="Player 1")

    bot2 = DoNothingBot()
    player2 = Player(key2, bot2, log=True, display_name="Player 2")

    t = threading.Thread(target=player_loop, args=(player1,))
    t.start()

    player_loop(player2)


if __name__ == '__main__':
    main()


