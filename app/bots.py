from models import *
from physics import *

class Bot:
    def handle_join_response(self, game_response):
        if not game_response.is_valid or game_response.game_stage == GAME_STAGE_HAS_FINISHED:
            print(f"{self} Skipping role detection for {game_response}")
            return

        self.role = game_response.static_game_info.role
        print(f"{self} Detected role as {self.role}")

    def handle_start_response(self, game_response):
        if not game_response.is_valid or game_response.game_stage == GAME_STAGE_HAS_FINISHED:
            print(f"{self} Skipping ship ID detection for {game_response}")
            return

        self.ship_id = None
        for ship in game_response.game_state.ships:
            if ship.role == self.role:
                self.ship_id = ship.ship_id

        print(f"{self} Detected ship ID as {self.ship_id}")

        if self.ship_id is None:
            raise ValueError(f"Failed to find initial ship IDs in {game_response} with role {self.role}")

    def get_start_data(self, game_response: GameResponse):
        raise RuntimeError("not implemented")

    def get_commands(self, game_response: GameResponse):
        raise RuntimeError("not implemented")

    def get_other_ship_ids(self, game_response):
        return [
            ship.ship_id 
            for ship in game_response.game_state.ships
            if ship.ship_id != self.ship_id
        ]

class DoNothingBot(Bot):
    def get_start_data(self, game_response: GameResponse):
        # default: not sure what it means
        # return [64, 48, 14, 1] # [446, 0, 0, 1]
        # return [5, 5, 5, 5]
        return [1, 1, 1, 1]

    def get_commands(self, game_response: GameResponse):
        # default: do nothing
        return []


class NaiveBot(Bot):
    def get_start_data(self, game_response: GameResponse):
        return [1, 1, 1, 1]

    def get_commands(self, game_response: GameResponse):
        # default: do nothing
        return []

class BasicFlyingHelper:
    def __init__(self, bot):
        self.bot = bot

    def get_commands(self, game_response: GameResponse, ship_id: int):
        """Issues commands to keep the given ship flying."""
        x, y = game_response.get_ship(ship_id).position

        if abs(x) > 47 or abs(y) > 47:
            # Just cool down
            return []
        else:
            x = -1 if x > 0 else 1
            y = -1 if y > 0 else 1

        return [
            AccelerateCommand(ship_id=ship_id, vector=(x, y))
        ]

class FlyingBot(Bot):
    def __init__(self):
        self.flying_helper = BasicFlyingHelper(self)

    def get_start_data(self, game_response: GameResponse):
        return [200, 10, 10, 1]

    def get_commands(self, game_response: GameResponse):
        return self.flying_helper.get_commands(game_response, self.ship_id)


class TrajectoryBot(FlyingBot):
    def get_commands(self, game_response: GameResponse):
        ship_state = game_response.get_ship(self.ship_id)
        x, y = ship_state.position
        vx, vy = ship_state.velocity

        N_PREDICTION_STEPS = 13
        W_CENTER1 = 10
        W_CENTER2 = 4
        W_CORNER = 3
        W_FUEL = 20
        W_PLANET_DIRECTION = 20
        W_V_DIRECTION = 10
        # print(f"params {(N_PREDICTION_STEPS, W_CENTER1, W_CENTER2, W_CORNER, W_FUEL)}")
        
        best_dv = (0, 0)
        best_cost = 1000
        for dvx in (-1, 0, 1):
            for dvy in (-1, 0, 1):
                # traj = []
                # print(f"\n\ndv: {(dvx, dvy)}")
                ks = KinematicState((x,y), (vx-dvx,vy-dvy))
                cost = 0
                min_linf_center_dist = min_l2_center_dist = min_l2_corner_dist = 1000
                for i in range(N_PREDICTION_STEPS):
                    ks = ks.update()
                    pos = ks.pos
                    # print(f"pos {i}: {pos}")
                    min_linf_center_dist = min(linf_norm(pos), min_linf_center_dist)
                    min_l2_center_dist = min(l2_norm(pos), min_l2_center_dist)
                    min_l2_corner_dist = min(min(l2_norm((pos[0]-cx, pos[1]-cy)) \
                     for cx in (16, -16) for cy in (16, -16) ), min_l2_corner_dist)
                    # print(f"dists {(min_linf_center_dist, min_l2_center_dist, min_l2_corner_dist)}")
                    cost = W_CENTER1*hinge(16 - min_linf_center_dist) \
                        + W_CENTER2*hinge(24 - min_l2_center_dist) \
                        + W_CORNER*hinge(5 - min_l2_corner_dist) \
                        + W_FUEL*linf_norm((dvx, dvy)) \
                        + W_PLANET_DIRECTION * (int(sign(x) == sign(dvx) and abs(y)<= 18) \
                             + int(sign(y) == sign(dvy) and abs(x) <= 18) )
                    # print(f"cost {cost}")

                if cost < best_cost:
                    best_dv = (dvx, dvy)
                    best_cost = cost
                    # print(f"new best dv: {best_dv}, cost {best_cost}\n")
        
        # print(f"Overall best dv {best_dv}, cost {best_cost} \n \n")
        return [AccelerateCommand(ship_id=self.ship_id, vector=best_dv)] if best_dv != (0, 0) else []




class ShootAheadHelper:
    def __init__(self, bot):
        self.bot = bot

    def get_commands(self, game_response: GameResponse, shooter_ship_id: int, target_ship_id: int, power: int):
        target_ship = game_response.get_ship(target_ship_id)
        p = target_ship.position
        v = target_ship.velocity
        g = get_g_force(p[0], p[1])
        target = (
            p[0] + v[0] + g[0],
            p[1] + v[1] + g[1],
        )
        return [
            ShootCommand(ship_id=shooter_ship_id, target=target, x3=power)
        ]


class ShooterBot(Bot):
    def __init__(self):
        self.flying_helper = BasicFlyingHelper(self)
        self.shoot_ahead_helper = ShootAheadHelper(self)

    def get_start_data(self, game_response: GameResponse):
        return [20, 52, 15, 1]

    def get_commands(self, game_response: GameResponse):
        ship  = game_response.get_ship(self.ship_id)
        if ship.x5 > ship.x6 / 2:
            print(f"Skipping shooting, ship's too hot {ship}")
            return []
        target_ship_id = self.get_other_ship_ids(game_response)[0]
        
        return (
            # self.flying_helper.get_commands(game_response, ship_id=self.ship_id) + 
            self.shoot_ahead_helper.get_commands(game_response, shooter_ship_id=self.ship_id, target_ship_id=target_ship_id, power=52)
        )

def get_away_vectors(xy1, xy2):
    x1, y1 = xy1
    x2, y2 = xy2

    if abs(x2 - x1) + abs(y2 - y1) <= 5:
        dx = sign(x2 - x1)
        dy = sign(y2 - y1)
        if dx == 0: dx += 1
        if dy == 0: dy += 1
        return ((dx, dy), (-dx, -dy))
    return None

def apply_point(pt, delta):
    return (pt[0] + delta[0], pt[1] + delta[1])


class ForkBot(Bot):
    def __init__(self):
        self.flying_helper = BasicFlyingHelper(self)
        self.starting_stats = [64, 64, 10, 4]
        self.num_forked = 0

    def get_start_data(self, game_response: GameResponse):
        return self.starting_stats

    def get_commands(self, game_response: GameResponse):
        team_ship_ids = []
        for ship in game_response.game_state.ships:
            if ship.role == self.role:
                team_ship_ids.append(ship.ship_id)

        if self.num_forked == 0:
            self.num_forked += 1
            return [ ForkCommand(
                        ship_id=self.ship_id,
                        x4=map(lambda x: x // 2, self.starting_stats))
                    ]
        commands = []
        if len(team_ship_ids) >= 2:
            ship_id1 = team_ship_ids[0]
            ship_id2 = team_ship_ids[1]

            pos1 = game_response.get_ship(ship_id1).position
            pos2 = game_response.get_ship(ship_id2).position
            vectors = get_away_vectors(pos1, pos2)
            if vectors:
                return [
                    AccelerateCommand(ship_id=ship_id1, vector=vectors[0]),
                    AccelerateCommand(ship_id=ship_id2, vector=vectors[1])
                ]
            
        for ship_id in team_ship_ids:
            commands.extend(self.flying_helper.get_commands(game_response, ship_id))
        return commands

class RoleSmartBot(Bot):
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender

    def handle_join_response(self, game_response):
        self.role = game_response.static_game_info.role
        if self.role == SHIP_ROLE_ATTACKER:
            print(f"{self} will use the ATTACKER strategy with bot {self.attacker}.")
            self.bot = self.attacker
        else:
            print(f"{self} will use the DEFENDER strategy with bot {self.defender}.")
            self.bot = self.defender

        self.bot.handle_join_response(game_response)

    def handle_start_response(self, game_response):
        self.bot.handle_start_response(game_response)

    def get_start_data(self, game_response: GameResponse):
        return self.bot.get_start_data(game_response)

    def get_commands(self, game_response: GameResponse):
        return self.bot.get_commands(game_response)
