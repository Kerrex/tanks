
import math
import vectors
import engine
import ident
from const import *

class Container:
	def __init__(self, conclass):
		self._con = []
		self._conclass = conclass
		self.atAddition = None
		self.atRemoval = None
	def __contains__(self, item):
		return item in self._con
	def __getitem__(self, key):
		return self._con[key]
	def add(self):
		self._con.append(self._conclass())
		self._con[-1].id = ident.get_id()
		if self.atAddition is not None:
			self.atAddition(self._con[-1])
		return self._con[-1]
	def remove(self, obj):
		if obj in self._con:
			self._con.remove(obj)
		if self.atRemoval is not None:
			self.atRemoval(obj)

class Sprite:
	def __init__(self):
		self.id = 0
		self._deleted = False
		self.health = 1
		self.mass = 1.0
		self.radius = 0
		self.friction = 0
		self.v_friction = 0
		self.h_friction = 0
		self.r_friction = 0
		self.pos = vectors.Vector3()
		self.v = vectors.Vector3()
		self.a = vectors.Vector3()
		self.color = "black"
		self.nick = ""
		self.type = TYPE_SPRITE
		self.turret = TURRET_MONO # workaround for export_delta
	def remove(self):
		pass
	def kill(self):
		self._deleted = True
		engine.deleted.append(self)
		self.remove()
	def export_delta(self):
		# to shrink sent data size, cast some values to int
		if self._deleted:
			return {"id": self.id, "delete": 0}
		else:
			return {"id": self.id, "x": self.pos.x, "y": self.pos.y, "r": self.pos.r,
					"radius": self.radius, "color": self.color, "nick": self.nick,
					"type": self.type, "turret": self.turret}
	def collides(self, other):
		distance2 = (self.pos.x - other.pos.x)**2 + (self.pos.y - other.pos.y)**2
		radiusum2 = (self.radius + other.radius)**2
		if distance2 > radiusum2:
			return False
		else:
			return True
	def step(self, ms):
		# friction
		ver = vectors.Vector3()
		hor = vectors.Vector3()
		ver.x = math.sin(self.pos.r)
		ver.y = -math.cos(self.pos.r)
		hor.x = -ver.y
		hor.y = ver.x
		base = vectors.Vector3() # friction acceleration in terms of tank's coordinates
		base.x = hor.x * self.v.x + hor.y * self.v.y # horizontal
		base.y = ver.x * self.v.x + ver.y * self.v.y # vertical
		base.x *= -self.h_friction
		base.y *= -self.v_friction
		self.a.x += -ver.y * base.x + hor.y * base.y
		self.a.y += ver.x * base.x - hor.x * base.y
		self.a.r -= self.v.r * self.r_friction
		# motion evaluation
		self.v += self.a * (ms / 1000.)
		self.pos += self.v * (ms / 1000.)
		# boundary check
		if self.pos.x > WIDTH + 10:
			self.pos.x = -10
		if self.pos.x < -10:
			self.pos.x = WIDTH + 10
		if self.pos.y > HEIGHT + 10:
			self.pos.y = -10
		if self.pos.y < -10:
			self.pos.y = HEIGHT + 10

class Tank(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.mass = 1.0
		self.morph(TYPE_ALPHA)
		self.turretize(TURRET_MONO)
		self.radius = 8.
		self.motor = False
		self.reverse = False
		self.autofire = False
		self.rot = ACTID_ROTATE_STOP
		self.timeout = 0
		self.player = None
	def remove(self):
		engine.tanks.remove(self)
	def morph(self, vehtype):
		self.type = vehtype
		if vehtype == TYPE_ALPHA:
			self.accel = 360.
			self.raccel = 360.
			self.rotaccel = 15 * math.pi
			self.v_friction = 3.
			self.h_friction = 20.
			self.r_friction = 10.
			self.health = 9
		elif vehtype == TYPE_LAMBDA:
			self.accel = 240.
			self.raccel = 240.
			self.rotaccel = 9 * math.pi
			self.v_friction = 1.
			self.h_friction = 1.
			self.r_friction = 3.
			self.health = 6
	def turretize(self, turret):
		self.turret = turret
		self.turret_state = 0
		if turret == TURRET_MONO:
			self.timeout_max = 500
		elif turret == TURRET_SOLI:
			self.timeout_max = 600
		elif turret == TURRET_DUO:
			self.timeout_max = 300
		elif turret == TURRET_OMNI:
			self.timeout_max = 100
		elif turret == TURRET_WIDER:
			self.timeout_max = 500
		elif turret == TURRET_BECKY:
			self.timeout_max = 500
	def act(self, actid):
		if actid == ACTID_MOTOR_ON:
			self.motor = True
		elif actid == ACTID_MOTOR_OFF:
			self.motor = False
		elif actid == ACTID_REVERSE_ON:
			self.reverse = True
		elif actid == ACTID_REVERSE_OFF:
			self.reverse = False
		elif actid == ACTID_FIRE_ON:
			self.autofire = True
		elif actid == ACTID_FIRE_OFF:
			self.autofire = False
		elif actid == ACTID_ROTATE_CL:
			self.rot = ACTID_ROTATE_CL
		elif actid == ACTID_ROTATE_CC:
			self.rot = ACTID_ROTATE_CC
		elif actid == ACTID_ROTATE_STOP:
			self.rot = ACTID_ROTATE_STOP
	def step(self, ms):
		if self.motor:
			self.a.x = self.accel * math.sin(self.pos.r)
			self.a.y = -self.accel * math.cos(self.pos.r)
		elif self.reverse:
			self.a.x = -self.raccel * math.sin(self.pos.r)
			self.a.y = self.raccel * math.cos(self.pos.r)
		else:
			self.a.x = 0
			self.a.y = 0
		if self.rot == ACTID_ROTATE_STOP:
			self.a.r = 0
		elif self.rot == ACTID_ROTATE_CL:
			self.a.r = self.rotaccel
		elif self.rot == ACTID_ROTATE_CC:
			self.a.r = -self.rotaccel
		# autofire
		self.timeout = self.timeout - ms if self.timeout > 0 else 0
		if self.timeout == 0 and self.autofire:
			if self.turret == TURRET_MONO:
				engine.bullets.add().fly(self, 0, -8, 0, TYPE_CANNONBALL)
			elif self.turret == TURRET_SOLI:
				bullet = engine.bullets.add()
				bullet.timeout = 800
				bullet.fly(self, 0, -8, 0, TYPE_CANNONBALL)
			elif self.turret == TURRET_DUO:
				self.turret_state += 1
				self.turret_state %= 2
				bullet = engine.bullets.add()
				bullet.timeout = 400
				if self.turret_state == 0:
					bullet.fly(self, -3, -8, 0, TYPE_CANNONBALL)
				else:
					bullet.fly(self, 3, -8, 0, TYPE_CANNONBALL)
			elif self.turret == TURRET_OMNI:
				self.turret_state += 1
				self.turret_state %= 4
				bullet = engine.bullets.add()
				bullet.timeout = 300
				bullet.fly(self, 0, 0, self.turret_state * math.pi / 2, TYPE_CANNONBALL)
				temp = math.pi / 6 if self.turret_state % 2 == 0 else 0
				bullet = engine.bullets.add()
				bullet.timeout = 150
				bullet.fly(self, 0, 0, math.pi / 6 + temp, TYPE_BULLET)
				bullet = engine.bullets.add()
				bullet.timeout = 150
				bullet.fly(self, 0, 0, 4 * math.pi / 6 + temp, TYPE_BULLET)
				bullet = engine.bullets.add()
				bullet.timeout = 150
				bullet.fly(self, 0, 0, 7 * math.pi / 6 + temp, TYPE_BULLET)
				bullet = engine.bullets.add()
				bullet.timeout = 150
				bullet.fly(self, 0, 0, 10 * math.pi / 6 + temp, TYPE_BULLET)
			elif self.turret == TURRET_WIDER:
				bullet = engine.bullets.add()
				bullet.timeout = 400
				bullet.fly(self, 0, -8, 0, TYPE_CANNONBALL)
				bullet = engine.bullets.add()
				bullet.timeout = 400
				bullet.fly(self, 0, 0, math.pi / 24, TYPE_BULLET)
				bullet = engine.bullets.add()
				bullet.timeout = 400
				bullet.fly(self, 0, 0, -math.pi / 24, TYPE_BULLET)
			elif self.turret == TURRET_BECKY:
				bullet = engine.bullets.add()
				bullet.timeout = 400
				bullet.fly(self, 0, -8, 0, TYPE_CANNONBALL)
				bullet = engine.bullets.add()
				bullet.timeout = 200
				bullet.fly(self, 0, 0, 11 * math.pi / 12, TYPE_BULLET)
				bullet = engine.bullets.add()
				bullet.timeout = 200
				bullet.fly(self, 0, 0, 13 * math.pi / 12, TYPE_BULLET)
			self.timeout = self.timeout_max
		Sprite.step(self, ms)

class Bullet(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.type = TYPE_BULLET
		self.damage = 1
		self.radius = 1.5
		self.mass = 0.01
		self.speed = 400
		self.timeout = 500
		self.owner = None
	def remove(self):
		engine.bullets.remove(self)
	def fly(self, tank, xoff, yoff, angle, kind):
		self.pos.x = tank.pos.x + xoff * math.cos(tank.pos.r) - yoff * math.sin(tank.pos.r)
		self.pos.y = tank.pos.y + xoff * math.sin(tank.pos.r) + yoff * math.cos(tank.pos.r)
		self.v.x = self.speed * math.sin(tank.pos.r + angle)
		self.v.y = -self.speed * math.cos(tank.pos.r + angle)
		self.owner = tank.player
		self.type = kind
		if kind == TYPE_BULLET:
			self.mass = 0.1
			self.radius = 2.
			self.damage = 1
		elif kind == TYPE_CANNONBALL:
			self.mass = 0.2
			self.radius = 3.
			self.damage = 3
	def step(self, ms):
		self.timeout -= ms
		if self.timeout < 0:
			self.kill()
		Sprite.step(self, ms)

class Obstacle(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.type = TYPE_OBSTACLE
		self.radius = 20.
		self.mass = 10.
	def remove(self):
		engine.obstacles.remove(self)
