import io
import requests
import sys

from player import *

def main():
    server_url = sys.argv[1]
    player_key = sys.argv[2]
    print('ServerUrl: %s; PlayerKey: %s' % (server_url, player_key))

    full_url = f"{server_url}/aliens/send"
    proxy = Proxy(full_url)

    # NOTE: fix here for different algorithms
    bot = FlyingBot()

    player = Player(proxy, key, bot, display_name="Me")
    player_loop(player)

    print("Done.")

if __name__ == '__main__':
    main()
