


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def get_g_force(x, y):
    if y > abs(x):
        return (0, -sign(y))
    if x > abs(y):
        return (-sign(x), 0)
    else:
        return (-sign(x), -sign(y))


class KinematicState:
    def __init__(self, pos, velocity):
        self.pos = pos
        self.velocity = velocity
    
    def update(self):
        x, y = self.pos
        vx, vy = self.velocity

        gx, gy = get_g_force(x, y)
        vx += gx
        vy += gy

        x += vx
        y += vy
        return KinematicState( (x, y), (vx, vy))


def expect_eq(a, b):
    print (f"comparing {a} and {b}")
    assert a == b, f'{a} != {b}'

if __name__ == "__main__":
    expect_eq (get_g_force(0, 10), (0, -1))
    expect_eq(get_g_force(10, 10), (-1, -1))
    expect_eq(get_g_force(10, 0), (-1, 0))
    expect_eq(get_g_force(10, -10), (-1, 1))