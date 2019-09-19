import sys
import math

sys.path.insert(0, '../vector3dm')
from vector3dm import Vector3dm

class Particle:
	def __init__(self,pos_vect,vel_vect=None):
		self.position = pos_vect
		if vel_vect is None:
			vel_vect = Vector3dm.zero_vector()
		self.velocity = vel_vect
		self.acceleration = Vector3dm.zero_vector()

	def __repr__(self):
		return "position: {}; velocity: {}; acceleration: {}".format(self.position,self.velocity,self.position)
	
	def brain(self):
		# this is code that changes the acceleration
		pass
	
	def impulse(self):
		# this is the code that updates the particle
		self.brain()
		self.velocity = self.velocity.add(self.acceleration)
		self.position = self.position.add(self.velocity)

if __name__ == "__main__":
	print(Particle(Vector3dm(1,2,3,"c"),Vector3dm(4,5,6,"c")))