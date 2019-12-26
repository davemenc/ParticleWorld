import sys
import math
import time
import pygame
import random

from pygame.locals import *
from pygame.compat import geterror

sys.path.insert(0, '../vector3dm')
from vector3dm import Vector3dm

"""" Particle class: single entity that may or may not have autonomy """
class Particle:
	def __init__(self,pos_vect,vel_vect=Vector3dm.zero_vector()):
		self.position = pos_vect
		self.p_pos = self.position # provisional position
		self.velocity = vel_vect
		self.p_vel = self.velocity # provisional velocity
		self.acceleration = Vector3dm.zero_vector()
		
		# various accelration Attributes
		# aerodynamics
		self.aero_coef = .05 # scale factor for Aerodynamic drag which opposes velocity
	
		#colision avoidance
		self.col_size = 1 # collision size
		self.dis_size = 20 # display size
		self.color = (255, 255, 255)
		self.flash_color = (255, 50, 0) # bright red
		
	def __repr__(self):
		return "position: {}; velocity: {}; acceleration: {}".format(self.position,self.velocity,self.acceleration)
	
	def brain(self):
		# this is code that changes the acceleration based on autonomy
		# it returns a value in m/s
		# by default it does nothing except call collision_avoidance which, by default, also does nothing
		collision_vector = self.collision_avoidance()
		return collision_vector
	
	def collision_avoidance(self):
		#apply the efforts of the 
		return Vector3dm.zero_vector()
	
	def aero_acc(self):
		# this is code that changes the acceleration based on aerodynamic drag
		# it returns a value in m/s
		# drag is proportional to speed**2 times drag coef in the vector opposite speed
		speed_squared = self.velocity.magnitude()**2
		v_drag = self.velocity.unit().neg().mult(speed_squared).mult(self.aero_coef)
		return v_drag

""" World Class: collection of entities that get processes as a whole: physics, display, collisions, etc """
class World:
	#WALL TYPES
	WALL_REFLECT = 0
	WALL_DISAPPEAR = 1
	WALL_FADE = 2
	WALL_BOUNCE = 3
	WALL_CREATE = 4

	def __init__(self,particle_count=10,width=1000,depth=1000,height=1000,wall_type=0):
		# create the log
		self.world_log = "log1.txt"
		f = open(self.world_log,"wt")
		f.close() #clear the file
		self.log_pointer = None
		self.log_pointer = open(self.world_log,"at")
		self.log_data("=======================================================\n")
		
		#init clock
		self.clock = None
		
		# world dimensions
		self.width = float(width) # total x dimension
		self.depth = float(depth) # total y dimension
		self.height = float(height) # total z dimension
		self.min_x = -width/2 # x coordinate of left wall
		self.min_y = -depth/2 # y coordinate of back wall
		self.min_z = 0.0 #z coordinate of floor
		self.max_x = self.width/2
		self.max_y = self.depth/2
		self.max_z = self.height
		
		self.log_data("self.width: {}".format(self.width))
		self.log_data("self.depth: {}".format(self.depth))
		self.log_data("self.min_x: {}".format(self.min_x))
		self.log_data("self.min_y: {}".format(self.min_y))
		self.log_data("self.min_z: {}".format(self.min_z))
		self.log_data("self.max_x: {}".format(self.max_x))
		self.log_data("self.max_y: {}".format(self.max_y))
		self.log_data("self.max_z: {}".format(self.max_z))
		
		# Wall Type
		
		"""
		Reflect: comes back in the other side with the same velocity
		Disappear: Things that hit an edge keep going but we stop tracking them
		Fade: things that hit and edge keep going but we keep tracking them to see if they come back
		Bounce: classic pong: hits and edge and bounces back
		Create: Leaves but another one is created with random velocity on the opposite edge
		"""
	
		self.wall_type = wall_type
		self.wall_type_desc = ["Reflect","Disappear","Fade","Bounce","Create"] # type is an index into table for descriptive purposes
		
		# basic sim artifacts
		self.particles = [] # list of particles
		self.collision_list = [] # list of collisions in this impulse
		self.sections = [] # list of sections
		self.gravity_mag = 9.8 # m/sec/sec
		self.gravity_locus = Vector3dm(0,0,self.max_z+6.371e6,"c") # a long ways below the floor
		self.impulse_duration = 1000 # micros
		self.sim_time = 0 # micros
		
		# Display Parameters
		self.displaysurf = None
		self.screen_size_width = 1680 
		self.screen_size_height = 1050
		self.screen_size_depth = self.depth
		self.display = None
		self.pixel_width_ratio = None
		self.pixel_height_ratio = None
		
		self.create_world(particle_count)
		#for el in self.particles:
			#self.log_data(el)

	def log_data(self,text):
		now =  time.localtime()
		now_str = "{}-{}-{}T{}:{}:{}".format(now[0],now[1],now[2],now[3],now[4],now[5])
		if self.log_pointer is None:
			self.log_pointer = open(self.world_log,at)
			#self.log_data("=======================================================\n")
			self.log_pointer.write("==================== {} ====================\n".format(now_str))
		self.log_pointer.write("{}: {}\n".format(now_str,text))
	def __del__(self):
		self.log_pointer.close()
	def __repr__(self):
		return "width: {}; depth: {}; height: {}; type: {}; particle count: {}".format(self.width,self.depth,self.height,self.wall_type_desc[self.wall_type],len(self.particles))

	def create_world(self,particle_count):
		for i in range(0,particle_count):
			position = Vector3dm(random.randrange(int(self.min_x),int(self.max_x)),random.randrange(int(self.min_y),int(self.max_y)),random.randrange(int(self.min_z),int(self.max_z)),"c")
			self.particles.append(Particle(position))


	def init_screen(self):
		# how big is the screen & what is it's relationship to the world

		pygame.init()
		self.displaysurf = pygame.display.set_mode(( self.screen_size_width, self.screen_size_height),pygame.FULLSCREEN)
		self.displaysurf.fill((0,0,0))
		pygame.display.set_caption('Particle World')
		pygame.mouse.set_visible(0)
		self.clock = pygame.time.Clock()
		pygame.display.update()
		
		
	def display_stats(self):
		pass
		
	def display_world(self):
		self.log_data("DISPLAY WORLD")
		self.displaysurf.fill((0,0,0))
		for el in self.particles:
			world_x = el.position.get_x()
			world_z = el.position.get_z()
			screen_x = int(((world_x+self.width/2)*self.screen_size_width)/self.width)
			if screen_x >= self.screen_size_width-4:
				screen_x = self.screen_size_width-4
			if screen_x <= 4:
				screen_x = 4
			screen_y = int(((world_z)*self.screen_size_height)/self.height)
			if screen_y >= self.screen_size_height-4:
				screen_y = self.screen_size_height-4
			if screen_y <= 4:
				screen_y = 4
			self.log_data("x{}->x{}; z{}->y{} ".format(world_x,screen_x,world_z,screen_y))
			pygame.draw.rect(self.displaysurf,el.color,(screen_x+1,screen_y+1,4,4),0)
			#pygame.draw.rect(self.displaysurf,(255,0,0),(self.screen_size_width/2,self.screen_size_height/2,3,3),0)
		pygame.display.update()

	def real_millis(self):
		return int(round(time.time() * 1000)) # real time milliseconds
		
	def run(self):
		self.log_data("run: {}".format(self))
		
		self.init_screen()
		start_real_millis = self.real_millis()
		self.log_data("STAT_REAL_MILLIS {}".format(self.real_millis()))
		screens = 0
		
		#Main Loop
		going = True
		player_state = 1
		#Draw Everything
		#self.display_world()
		while going:
			#self.clock.tick(20)
			#Handle Input Events
			for event in pygame.event.get():
				if event.type == QUIT:
					going = False
					continue
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					going = False
					continue
				elif event.type == KEYDOWN:
					pass
				elif event.type == MOUSEBUTTONUP:
					click_location = event.pos

			#self.log_data("elapsed RT: {}; ST:{}  ".format((self.real_millis() - start_real_millis),self.sim_time//1000))
			if True or (self.real_millis() - start_real_millis) >= self.sim_time//100: #choke sim time to real time
				# Do sim
				self.impulse()
			
			if (self.real_millis() - start_real_millis) >= screens*50 : # display 20 times a second, real time
				screens+=1
				#Draw Everything
				self.display_world()

		pygame.quit()
		#write_gameschema()

		self.display_stats()
	def gravity(self,particle):
		# return the value for gravity in m/impulse/impulse
		
		gravity_acc = particle.position.point_at_that(self.gravity_locus)

		gravity_acc.set_r(self.gravity_mag *  float(self.impulse_duration) / 1000000.0)

		self.log_data("physics_acc:{}".format(gravity_acc))
		return gravity_acc

		return Vector3dm.zero_vector()
	def constraints(self,particle):
		# adjust the effects of the limits (constraints) of the world on the partcle
		# it must run before acceleration and velocity are applied in impulse
		pass
		if particle.p_pos.get_z() >= self.max_z:
			particle.p_vel = Vector3dm.zero_vector()
			particle.p_pos = Vector3dm(particle.p_pos.get_x(),particle.p_pos.get_y(),self.max_z,"c")
			#self.log_data("Rock bottom post:{}".format(particle))
	
	def physics(self,particle):
		# apply other kinds of physics (besides aerodynamics and gravity )
		return Vector3dm.zero_vector()
	def impulse(self):
		for el in self.particles:
			el.acceleration = Vector3dm.zero_vector()
			self.log_data("impulse old: {}".format(el))
#			el.flash_color = el.color
			
			#el.p_vel = el.velocity
			#el.p_pos = el.position
			
			brain_acc = el.brain()
			brain_acc.set_r(brain_acc.get_r()*float(self.impulse_duration)/1000000.0)
			el.acceleration = el.acceleration.add(brain_acc)
			self.log_data("brain: {}".format(brain_acc.convert_to_cartesian()))
			
			aero_acc = el.aero_acc()
			aero_acc.set_r(brain_acc.get_r()*float(self.impulse_duration)/1000000.0)
			self.log_data("aero_acc: {}".format(aero_acc.convert_to_cartesian()))

			gravity_acc = self.gravity(el)
			
			physics_acc = self.physics(el)
			
			self.log_data("impulse pre:{}".format(el))

			el.acceleration = Vector3dm.zero_vector().add(brain_acc).add(aero_acc).add(gravity_acc).add(physics_acc)
			
			self.log_data("impulse post:{}".format(el))

			el.velocity = el.velocity.add(el.acceleration)
			el.position = el.position.add(el.velocity)

			self.constraints(el) # change the particle based on wall/space constraints
			self.log_data("impulse new: {}".format(el))
			
		self.collisions()
		self.sim_time += self.impulse_duration
		self.log_data("time: {}".format(self.sim_time))


		
 
	def collisions(self):
		for el1_idx in range(1,len(self.particles)):
			for el2_idx in range(0,el1_idx):
				el1 = self.particles[el1_idx]
				el2 = self.particles[el2_idx]
				if self.collision(el1,el2):
					el1.flash_color = (255,24,24)
					self.log_data("collision {} and {}".format(el1,el2))

	def distance_squared(self,el1,el2):
		diff = el1.p_pos.sub(el2.p_pos)
		return (diff.get_x()**2+diff.get_y()**2+diff.get_z()**2)

	def collision(self,el1,el2):
		safe_dist = (el1.col_size+el2.col_size)**2
		return self.distance_squared(el1,el2)<safe_dist		

	def draw_text(self,str,font,position):
		global gamedata
		text = font.render(str,1,(0,0,0))
		gamedata['self.displaysurf'].blit(text,position)
if __name__ == "__main__":
	pass
	w = World(50)
	#print(w)
	#for p in w.particles:
	#	print(p)
#	input("press return; esc ends")
	w.run()
	