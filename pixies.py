import sys
import math
import time
from particle import Particle
from world import World

class Pixies(World):
	def __init__(self):
		self.max_speed = 20.0
		self.max_acc = 20.0
		self.goal = None
		self.goal_distance = 50.0
		self.goal_close = 10.0

		World.__init__(self,10,1000,1000,1000,0)
		
	def pick_a_goal(self,particle):
		pass
	def close_to_goal(self,particle):
		pass
	def brains(self):
		for el in self.particles:
			
			if el.goal is None:
				el.goal = self.pick_a_goal(el)
				return
			if self.close_to_goal(el):
				self.goal = None
			
			# get a vector to the goal
			# reduce the length to max_acc
			# trial add to the trial velocity
			# if the trial velocity > max_speed, cut back on acc
			# make your trial acc this acc

if __name__ == "__main__":
	p = Pixies()