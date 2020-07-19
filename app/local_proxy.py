
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

KONTUR_URL = "https://icfpc2020-api.testkontur.ru"
API_KEY = "apiKey=6e1336a2ffa94971b5f74715a85708b9"


def main():
    # a = [1, [[[0, [8278679430195342144, None]], [[1, [8541530479718220884, None]], None]], None]]
    # print (flatten_cons(a))
    # a = [1, [1, [[256, [0, [[512, [1, [64, None]]], [[16, [128, None]], [[446, [0, [0, [1, None]]]], None]]]]], [[0, [[16, [128, None]], [[[[1, [0, [[-48, -29], [[0, 0], [[446, [0, [0, [1, None]]]], [0, [64, [1, None]]]]]]]], [None, None]], [[[0, [1, [[48, 29], [[0, 0], [[446, [0, [0, [1, None]]]], [0, [64, [1, None]]]]]]]], [None, None]], None]], None]]], None]]]]
    # print (flatten_cons(a))
    # return
    full_url = f'{KONTUR_URL}/aliens/send?{API_KEY}'

    proxy = Proxy(full_url)
    create = proxy.create_new_game()

    print (create)
    key1 = create[1][0][1]
    key2 = create[1][1][1]

    bot1 = DoNothingBot()
    bot2 = DoNothingBot()
    
    t = threading.Thread(target=join_and_play_the_game, args=(proxy, key2, bot2, "Player 2"))
    t.start()

    join_and_play_the_game(proxy, key1, bot1, "Player 1")


if __name__ == '__main__':
    main()


