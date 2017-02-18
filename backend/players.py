import engine
import random
import math

from const import *

players = []


class Player:
    def __init__(self, hnd):
        self.handler = hnd
        self.spawn()
        self.nick = "guest"
        self.tank.nick = self.nick
        self.score = 0
        self.respawn = 0

    def spawn(self):
        self.tank = engine.tanks.add()
        self.tank.pos.x = 40 + random.randint(1, 400)
        self.tank.pos.y = 40 + random.randint(1, 400)
        self.tank.pos.r = random.random() * 2 * math.pi
        self.tank.morph(TYPE_ALPHA if random.random() > 0.5 else TYPE_LAMBDA)
        self.tank.turretize(random.randint(0, 5))
        self.tank.player = self

    def kill(self):
        self.tank = None
        self.respawn = RESPAWN_TIME

    def step(self, ms):
        if self.tank is None:
            if self.respawn > 0:
                self.respawn -= ms
            else:
                self.spawn()
                self.tank.nick = self.nick


def register(handler):
    player = Player(handler)
    players.append(player)
    return player


def unregister(handler):
    for elem in players:
        if elem.handler == handler:
            if elem.tank is not None:
                elem.tank.kill()
            players.remove(elem)


def get_player_from_handler(handler):
    for elem in players:
        if elem.handler == handler:
            return elem
    return None
