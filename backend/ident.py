
import engine
from const import *

freeId = 0

def get_id():
	global freeId
	freeId += 1
	return freeId - 1

def clean_ids():
	pass

def get_object_from_id(id):
	for tank in engine.tanks:
		if tank.id == id:
			return tank
	for bullet in engine.bullets:
		if bullet.id == id:
			return bullet
	for obstacle in engine.obstacles:
		if obstacle.id == id:
			return obstacle
	return None
