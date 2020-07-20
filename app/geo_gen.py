import itertools
import pprint

from physics import *

GLOBAL_DATA = {}

def check_geo(coord, speed, accel):
    num_ticks = 256
    state = KinematicState(coord, speed).update(accel)
    for _ in range(num_ticks):
        if abs(state.pos[0]) <= 16 and abs(state.pos[1]) <= 16:
            return False
        state = state.update()
    return True

def main():
    coords = [(x, y) for (x, y) in itertools.product(range(-48, 49), repeat=2) if abs(x) > 16 or abs(y) > 16]
    speeds = [(x, y) for (x, y) in itertools.product(range(-10, 11), repeat=2) if abs(x) + abs(y) < 10]
    accels = [(x, y) for (x, y) in itertools.product(range(-1, 2), repeat=2)]

    for coord in coords:
        print(f"Working on {coord}")
        for speed in speeds:
            for accel in accels:
                if check_geo(coord, speed, accel):
                    GLOBAL_DATA[(coord, speed)] = accel
    
    output = open('app/good_geo.py', 'w')
    output.write(f'LOOKUP_TABLE = {pprint.pformat(GLOBAL_DATA)}')
    output.close()

if __name__ == "__main__":
    main()