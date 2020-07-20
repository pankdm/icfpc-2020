

import itertools
import pprint

from physics import *

NUM_FUEL = 4
GLOBAL_DATA = {}

def run_simulation(x, y, take):
    num_ticks = 256
    state = KinematicState((x, y), (0, 0))
    for tick in range(num_ticks):
        acc = take.get(tick, None)
        state = state.update(accelerate=acc)
        if abs(state.pos[0]) <= 16 and abs(state.pos[1]) <= 16:
            return False
    return True


def try_find_good_combination(x, y):
    global GLOBAL_DATA
    deltas = itertools.product([-1, 0, 1], repeat=2)
    applications = itertools.product(deltas, repeat=NUM_FUEL)
    for c in itertools.combinations(range(20), NUM_FUEL):
        for apps in applications:
            take = {}
            for key, value in zip(c, apps):
                take[key] = value
            ok = run_simulation(x, y, take)
            if ok:
                print(f"x = {x}, found good: {take}")
                GLOBAL_DATA[ (x, y) ] = take
                return



def main():
    for x in range(-48, 49):
        print (f"finding for x = {x}")
        try_find_good_combination(x, 48)
        try_find_good_combination(x, -48)


    for y in range(-48, 49):
        print (f"finding for y = {y}")
        try_find_good_combination(48, y)
        try_find_good_combination(-48, y)
    
    output = open('app/lookup_table.py', 'w')
    output.write(f'LOOKUP_TABLE = {pprint.pformat(GLOBAL_DATA)}')
    output.close()


if __name__ == "__main__":
    main()