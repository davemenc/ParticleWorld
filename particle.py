import sys
import math

sys.path.insert(0, '../vector3dm')
from vector3dm import Vector3dm

class Particle:
	def __init__(self,pos_vect,vel_vect=Vector3dm.zero_vector()):
		self.position = pos_vect
		self.p_pos = self.position # provisional position
		self.velocity = vel_vect
		self.p_vel = self.velocity # provisional velocity
		self.acceleration = Vector3dm.zero_vector()
		self.col_size = 1 # collision size
		self.dis_size = 20 # display size
		self.color = (255, 255, 255)
		self.flash_color = (255, 50, 0) # bright red

	def __repr__(self):
		return "position: {}; velocity: {}; acceleration: {}".format(self.position,self.velocity,self.acceleration)
	
	def brain(self):
		# this is code that changes the acceleration
		pass
	
	def impulse(self):
		# this is the code that updates the particle
		self.brain()
		self.velocity = self.velocity.add(self.acceleration)
		self.position = self.position.add(self.velocity)

if __name__ == "__main__":
	pass
	#print(Particle(Vector3dm(1,2,3,"c"),Vector3dm(4,5,6,"c")))