import io
import requests
import sys

from player import *

def main():
    server_url = sys.argv[1]
    player_key = sys.argv[2]
    print('ServerUrl: %s; PlayerKey: %s' % (server_url, player_key))

    # NOTE: fix here for different algorithms
    bot = DoNothingBot()

    proxy = Proxy(server_url)
    player = Player(player_key, bot=bot, proxy=proxy)
    player_loop(player)
    print("Done.")

if __name__ == '__main__':
    main()
