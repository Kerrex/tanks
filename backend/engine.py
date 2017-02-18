import math
import vectors
import objects
import time

from const import *

tanks = objects.Container(objects.Tank)
tanks.atRemoval = lambda obj: obj.player.kill() if obj and obj.player else None
bullets = objects.Container(objects.Bullet)
obstacles = objects.Container(objects.Obstacle)
deleted = []

then = time.time()
now = time.time()


def bounce_reaction(spr1, spr2):
    unit = spr1.pos - spr2.pos
    unit.r = 0
    length = math.sqrt(unit.x * unit.x + unit.y * unit.y)
    unit /= length
    # position correction
    error = spr1.radius + spr2.radius - length
    errata = unit * error
    spr1.pos += errata
    spr2.pos -= errata
    # conservation of momentum and energy
    v1 = unit * (unit.x * spr1.v.x + unit.y * spr1.v.y)
    v2 = unit * (unit.x * spr2.v.x + unit.y * spr2.v.y)
    mass_sum = spr1.mass + spr2.mass
    mass_diff = spr1.mass - spr2.mass
    spr1.v += v1 * (mass_diff / mass_sum) + v2 * (2 * spr2.mass / mass_sum) - v1
    spr2.v += v2 * (-mass_diff / mass_sum) + v1 * (2 * spr1.mass / mass_sum) - v2


def process_step(ms):
    # movement step
    for tank in tanks:
        tank.step(ms)
    for bullet in bullets:
        bullet.step(ms)
    for obstacle in obstacles:
        obstacle.step(ms)
    # collision check
    for ti, tank in enumerate(tanks):
        for bullet in bullets:
            if bullet.owner is None or bullet.owner.tank != tank:
                if tank.collides(bullet):
                    bullet.kill()
                    tank.health -= bullet.damage
                    if tank.health <= 0:
                        tank.kill()
                    # score
                    if bullet.owner is not None:
                        bullet.owner.score += 1
                        print "Player %s scored! (%d)" % (bullet.owner.nick, bullet.owner.score)
        for tank2 in tanks[ti + 1:]:
            if tank.collides(tank2):
                bounce_reaction(tank, tank2)
        for obstacle in obstacles:
            if tank.collides(obstacle):
                bounce_reaction(tank, obstacle)
    for bi, bullet in enumerate(bullets):
        for bullet2 in bullets[bi + 1:]:
            if bullet.owner != bullet2.owner:
                if bullet.collides(bullet2):
                    bounce_reaction(bullet, bullet2)
        for obstacle in obstacles:
            if bullet.collides(obstacle):
                bullet.owner = None
                bounce_reaction(bullet, obstacle)


def process_physics():
    global then, now
    then = now
    now = time.time()
    delta = (now - then) * 1000
    process_step(delta)
