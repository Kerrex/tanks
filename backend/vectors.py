
import math

class Vector3:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.r = 0
	def __abs__(self):
		return math.sqrt(self.x * self.x + self.y * self.y)
	def __iadd__(self, other):
		self.x += other.x
		self.y += other.y
		self.r += other.r
		return self
	def __isub__(self, other):
		self.x -= other.x
		self.y -= other.y
		self.r -= other.r
		return self
	def __imul__(self, other):
		self.x *= other
		self.y *= other
		self.r *= other
		return self
	def __idiv__(self, other):
		self.x /= other
		self.y /= other
		self.r /= other
		return self
	def __add__(self, other):
		val = Vector3()
		val.x = self.x + other.x
		val.y = self.y + other.y
		val.r = self.r + other.r
		return val
	def __sub__(self, other):
		val = Vector3()
		val.x = self.x - other.x
		val.y = self.y - other.y
		val.r = self.r - other.r
		return val
	def __mul__(self, other):
		val = Vector3()
		val.x = self.x * other
		val.y = self.y * other
		val.r = self.r * other
		return val
	def __div__(self, other):
		val = Vector3()
		val.x = self.x / other
		val.y = self.y / other
		val.r = self.r / other
		return val
