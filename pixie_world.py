import sys
import math
import time
import pygame
import random

from particle_world import World
from particle_world import Particle

from pygame.locals import *
from pygame.compat import geterror

sys.path.insert(0, '../vector3dm')
from vector3dm import Vector3dm

class Pixie(Particle):
	def __init__(self,pos_vect,vel_vect=Vector3dm.zero_vector()):
		super().__init__(pos_vect, vel_vect)
		self.goals = [Vector3dm(0,0,100,"c"),Vector3dm(400,400,100,"c"),Vector3dm(0,0,500,"c"),Vector3dm(-400,-400,800,"c")]
		self.goal_idx = 0 # first goal, increment as we go
		self.goal = None # brain will calculate first goal

	def brain(self):
		# this is code that changes the acceleration based on pixie desires.
		result = Vector3dm.zero_vector()
		CLOSE_RANGE = 10.0
		MAX_ACC = 20.0
		if self.goal is None:
			self.goal = self.goals[self.goal_idx]
			self.goal_idx += 1
			if self.goal_idx > len(self.goals):
				self.goal_idx = 0
			return result
		range = self.position.magnitude(self.goal)
		if range < CLOSE_RANGE: # we've reached our goal
			self.goal = None			
			return result
		direction = self.position.point_at_that(self.goal)
		if direction.get_r() > MAX_ACC:
			direction.set_r(MAX_ACC)
		speed = self.velocity.get_r()

		slowing = speed/MAX_ACC # Seconds to slow
		arrival = range/speed # seconds to get there
		if slowing < arrival:
			result = direction
		else: 
			if speed <= CLOSE_RANGE:
				return Vector3dm.zero_vector() #coast closer
			elif speed < CLOSE_RANGE+MAX_ACC:
				direction.set_r(speed - CLOSE_RANGE) #get the speed to around the close_range; fastest we can go to not overshoot
			result = direction.neg()
		return result
			

class PWorld(World):
	def __init__(self):
		super().__init__(1) #init world with one particle, except in this world it will be a pixie

	def create_world(self,particle_count):
		self.pixies = []

		for i in range(0,particle_count):
			position = Vector3dm(-400,-400,800,"c")
			pixie = Pixie(position)
			self.particles.append(pixie)

if __name__ == "__main__":
	pw = PWorld()
	print("pw",pw)
	for p in pw.particles:
		print("pixie",p)
	#print("goals",pw.goals)
	input("press return; esc ends")
	pw.run()
	