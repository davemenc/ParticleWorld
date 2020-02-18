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
	def __init__(self,pos_vect,vel_vect=Vector3dm.zero_vector(),id=""):
		self.position = pos_vect
		self.velocity = vel_vect
		self.acceleration = Vector3dm.zero_vector()
		self.id = id
		self.count = 0
		
		# various accelration Attributes
		# aerodynamics
		self.aero_coef = .05 # scale factor for Aerodynamic drag which opposes velocity
	
		#colision avoidance
		self.col_size = 1 # collision size
		self.dis_size = 20 # display size
		self.color = (255, 255, 255)
		self.flash_color = (255, 50, 0) # bright red
		
	def __repr__(self):
		return "{} position: {}; velocity: {}; acceleration: {}".format(self.id,self.position,self.velocity,self.acceleration)
	
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
	MICROS_IN_SEC = 1.0e6
	Log_Pointer = None
	World_Log_Name = "log.txt"
	
	def Log_Data(text):
		now =  time.localtime()
		now_str = "{}-{}-{}T{}:{}:{}".format(now[0],now[1],now[2],now[3],now[4],now[5])
		if World.Log_Pointer is None:
			World.Log_Pointer = open(World.World_Log_Name,"wt")
			World.Log_Pointer.write("======================= {} ================================\n".format(now_str))
		World.Log_Pointer.write("{}: {}\n".format(now_str,text))
	def __init__(self,particle_count=10,width=1000,depth=1000,height=1000,wall_type=0):
		self.wall_type_desc = ["Reflect","Disappear","Fade","Bounce","Create"] # type is an index into table for descriptive purposes

		# create the log
		World.Log_Data("Pcount: {}; Width: {}; Depth: {};, Height: {}; Wall: {}".format(particle_count,width,depth,height,self.wall_type_desc[wall_type]))
		
		#init clock
		self.clock = None
		self.going = True

		
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
		
		World.Log_Data("self.width: {}".format(self.width))
		World.Log_Data("self.depth: {}".format(self.depth))
		World.Log_Data("self.min_x: {}".format(self.min_x))
		World.Log_Data("self.min_y: {}".format(self.min_y))
		World.Log_Data("self.min_z: {}".format(self.min_z))
		World.Log_Data("self.max_x: {}".format(self.max_x))
		World.Log_Data("self.max_y: {}".format(self.max_y))
		World.Log_Data("self.max_z: {}".format(self.max_z))
		
		# Wall Type
		
		"""
		Reflect: comes back in the other side with the same velocity
		Disappear: Things that hit an edge keep going but we stop tracking them
		Fade: things that hit and edge keep going but we keep tracking them to see if they come back
		Bounce: classic pong: hits and edge and bounces back
		Create: Leaves but another one is created with random velocity on the opposite edge
		"""
	
		self.wall_type = wall_type
		
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
			#World.Log_Data(el)

	def __del__(self):
		if World.Log_Pointer is not None:
			World.Log_Pointer.close()
	def __repr__(self):
		return "width: {}; depth: {}; height: {}; type: {}; particle count: {}".format(self.width,self.depth,self.height,self.wall_type_desc[self.wall_type],len(self.particles))

	def random_position(self):
		r_x = random.random()*self.width+self.min_x
		r_y = random.random()*self.depth+self.min_y
		r_z = random.random()*self.height+self.min_z
		r_pos = Vector3dm(r_x,r_y,r_z,"c")
		return r_pos
	
	def random_goal(self,current_pos,min_dist,max_dist):
		# given your current position and how far (min and max) you want to go, this gets you a goal
		# input: vector of current_pos, scaler of minimum and maximum distance
		# return: a vector with the new position of the random goal.
#		self.width = float(width) # total x dimension
#		self.depth = float(depth) # total y dimension
#		self.height = float(height) # total z dimension
#		self.min_x = -width/2 # x coordinate of left wall
#		self.min_y = -depth/2 # y coordinate of back wall
#		self.min_z = 0.0 #z coordinate of floor
#		self.max_x = self.width/2
#		self.max_y = self.depth/2
#		self.max_z = self.height
		dist = random.random()*(max_dist-min_dist)+min_dist	
		theta = random.random()*2*math.pi
		phi = random.random()*math.pi
		result = Vector3dm(dist,theta,phi,"s").add(current_pos)
		x,y,z = result.convert_to_cartesian().vals		
		if x>self.max_x:
			result.set_x(self.max_x)
		elif x<self.min_x:
			result.set_x(self.min_x)
		if y>self.max_y:
			result.set_y(self.max_y)
		elif y<self.min_y:
			result.set_y(self.min_y)
		if z>self.max_z:
			result.set_z(self.max_z)
		elif z<self.min_z:
			result.set_z(self.min_z)
		return result
		
	def create_world(self,particle_count):
		for i in range(0,particle_count):
			position = Vector3dm(
				random.randrange(int(self.min_x),int(self.max_x)),
				random.randrange(int(self.min_y),int(self.max_y)),
				random.randrange(int(self.min_z),int(self.max_z)),
				"c")
			self.particles.append(Particle(pos_vect=position,id=i))
#	def __init__(self,pos_vect,vel_vect=Vector3dm.zero_vector(),id=None):


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
		#World.Log_Data("DISPLAY WORLD")
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
			#World.Log_Data("x{}->x{}; z{}->y{} ".format(world_x,screen_x,world_z,screen_y))
			pygame.draw.rect(self.displaysurf,el.color,(screen_x+1,screen_y+1,4,4),0)
			#pygame.draw.rect(self.displaysurf,(255,0,0),(self.screen_size_width/2,self.screen_size_height/2,3,3),0)
		pygame.display.update()

	def real_millis(self):
		return int(round(time.time() * 1000)) # real time milliseconds
		
	def run(self):
		World.Log_Data("run: {}".format(self))
		
		self.init_screen()
		start_real_millis = self.real_millis()
		World.Log_Data("START_REAL_MILLIS {}".format(self.real_millis()))
		screens = 0
		
		#Main Loop
		self.going = True
		player_state = 1
		#Draw Everything
		#self.display_world()
		while self.going:
			#self.clock.tick(20)
			#Handle Input Events
			World.Log_Data("_______________ R{}:S{} _______________".format((self.real_millis()-start_real_millis)*self.impulse_duration,self.sim_time))
			for event in pygame.event.get():
				if event.type == QUIT:
					self.going = False
					continue
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					self.going = False
					continue
				elif event.type == KEYDOWN:
					pass
				elif event.type == MOUSEBUTTONUP:
					click_location = event.pos

			#World.Log_Data("elapsed RT: {}; ST:{}  ".format((self.real_millis() - start_real_millis),self.sim_time//1000))
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
		#gravity_acc = particle.position.point_at_that(self.gravity_locus)
		#World.Log_Data("point at:{}".format(gravity_acc.convert_to_cartesian()))
		#World.Log_Data("self.gravity_mag: {}".format(self.gravity_mag*  float(self.impulse_duration) / World.MICROS_IN_SEC))
		#gravity_acc.set_r(self.gravity_mag *  float(self.impulse_duration) / World.MICROS_IN_SEC)
		gravity_acc = Vector3dm(0,0,0.0098,"c")
		World.Log_Data("gravity_acc:{}->{}".format(gravity_acc.convert_to_spherical(),gravity_acc.convert_to_cartesian()))
		return gravity_acc

	def constraints(self,particle):
		# adjust the effects of the limits (constraints) of the world on the partcle
		# it must run before acceleration and velocity are applied in impulse
		World.Log_Data("constraint start: {}".format(particle))
		if particle.position.get_z() > self.max_z:
			particle.velocity = Vector3dm.zero_vector()
			particle.acceleration = Vector3dm.zero_vector()
			particle.position.set_z(self.max_z)
			World.Log_Data("YES! Rock bottom post constraints:{}".format(particle))
		if particle.position.get_y() > self.max_y:
			particle.position.set_y(self.max_y)
					
		if particle.position.get_x() > self.max_x:
			particle.position.set_y(self.max_x)
					
		if particle.position.get_y() < self.min_y:
			particle.position.set_y(self.min_y)
					
		if particle.position.get_x() < self.min_x:
			particle.position.set_x(self.min_x)
					
		if particle.position.get_z() < self.min_z:
			particle.position.set_z(self.min_z)
	
		if particle.velocity.get_z() > 20.0:
			particle.velocity.set_z(20.0)
		World.Log_Data("constraint end: {}".format(particle))

	def physics(self,particle):
		# apply other kinds of physics (besides aerodynamics and gravity )
		return Vector3dm.zero_vector()

	def impulse(self):
		for i in range(0,len(self.particles)):
			el = self.particles[i]
			el.acceleration = Vector3dm.zero_vector()
			World.Log_Data("{}: impulse old: {}".format(i,el))
			
			brain_acc = el.brain()
			brain_acc.set_r(brain_acc.get_r()*float(self.impulse_duration)/World.MICROS_IN_SEC)
			World.Log_Data("{}: brain: {}".format(i,brain_acc.convert_to_cartesian()))
			
			aero_acc = el.aero_acc()
			aero_acc.set_r(brain_acc.get_r()*float(self.impulse_duration)/World.MICROS_IN_SEC)
			#World.Log_Data("{}: aero_acc: {}".format(i,aero_acc.convert_to_cartesian()))

			gravity_acc = self.gravity(el)
			physics_acc = self.physics(el)
			
			World.Log_Data("{}: impulse pre:{}".format(i,el))

			el.acceleration = Vector3dm.zero_vector().add(brain_acc).add(aero_acc).add(gravity_acc).add(physics_acc)
			
			World.Log_Data("{}: impulse post:{}".format(i,el))

			el.velocity = el.velocity.add(el.acceleration)
			el.position = el.position.add(el.velocity)

			self.constraints(el) # change the particle based on wall/space constraints
			World.Log_Data("{}: impulse new: {}".format(i,el))
			
		self.collisions()
		self.sim_time += self.impulse_duration
		World.Log_Data("time: {}".format(self.sim_time))
 
	def collisions(self):
		for el1_idx in range(1,len(self.particles)):
			for el2_idx in range(0,el1_idx):
				el1 = self.particles[el1_idx]
				el2 = self.particles[el2_idx]
				if self.collision(el1,el2):
					el1.flash_color = (255,24,24)
					World.Log_Data("collision {} and {}".format(el1,el2))

	def distance_squared(self,el1,el2):
		diff = el1.position.sub(el2.position)
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
	w = World(100,1000,1000,1000)
#	print(w.random_position())
#	print(w.random_position())
#	print(w.random_position())
#	print(w)
#	for p in w.particles:
#		print(p)
#	input("press return; esc ends")
	w.run()
	