import math
import time
from particle import Particle
import pygame
import random
from pygame.locals import *
from pygame.compat import geterror
import sys
sys.path.insert(0, '../vector3dm')
from vector3dm import Vector3dm

BLUE = (45,70,255)
RED = (255,24,24)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (  0, 255,   0)
YELLOW = ( 255, 255, 0)
GREY = (128,128,128)
COLLISION_COLOR = RED


class World:
	def __init__(self,particle_count=10,width=1000,depth=1000,height=1000,wall_type=0):
		self.world_log = "log1.txt"
		f = open(self.world_log,"wt")
		f.close() #clear the file

		self.log_pointer = None
		self.log_pointer = open(self.world_log,"at")
		self.log_data("=======================================================\n")
		self.clock = None
		#self.log_pointer.write("==================== {} ====================\n".format(now_str))
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
		
		self.particles = [] # list of particles
		self.collision_list = [] # list of collisions in this impulse
		self.sections = [] # list of sections
		self.gravity = 9.8 # m/sec/sec
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
			self.log_pointer = open(self.world_log,"at")
			#self.log_data("=======================================================\n")
			self.log_pointer.write("==================== {} ====================\n".format(now_str))
		self.log_pointer.write("{}: {}\n".format(now_str,text))

	def __repr__(self):
		return "width: {}; depth: {}; height: {}; type: {}; particle count: {}".format(self.width,self.depth,self.height,self.wall_type_desc[self.wall_type],len(self.particles))

	def create_world(self,particle_count):
		for i in range(0,particle_count):
			position = Vector3dm(random.randrange(int(self.min_x),int(self.max_x)),random.randrange(int(self.min_y),int(self.max_y)),random.randrange(int(self.min_z),int(self.max_z)),"c")
			position = Vector3dm(50,300,200,"c")
			self.particles.append(Particle(position))
	def check_position(self,s):
		pass
	def init_screen(self):
		# how big is the screen & what is it's relationship to the world

		pygame.init()
		self.displaysurf = pygame.display.set_mode(( self.screen_size_width, self.screen_size_height),pygame.FULLSCREEN)
		self.displaysurf.fill(BLACK)
		pygame.display.set_caption('Particle World')
		pygame.mouse.set_visible(0)
		self.clock = pygame.time.Clock()
		pygame.display.update()
		
		
	def display_stats(self):
		pass
		
	def display_world(self):
		self.log_data("DISPLAY WORLD")
		self.displaysurf.fill(BLACK)
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
			if (self.real_millis() - start_real_millis) >= self.sim_time//100: #choke sim time to real time
				# Do sim
				self.impulse()
			
			if (self.real_millis() - start_real_millis) >= screens*50 : # display 20 times a second, real time
				screens+=1
				#Draw Everything
				self.display_world()

		pygame.quit()
		#write_gameschema()

		self.display_stats()
		
	def impulse(self):
		for el in self.particles:
			el.acceleration = Vector3dm.zero_vector()
			self.log_data("impulse old: {}".format(el))
			el.flash_color = el.color
			
			el.p_vel = el.velocity
			el.p_pos = el.position
			
			el.brain()
			self.physics(el)
			el.p_vel = el.p_vel.add(el.acceleration)
			el.p_pos = el.p_pos.add(el.p_vel)
			el.velocity = el.p_vel
			el.position = el.p_pos
			self.log_data("impulse new: {}".format(el))
			
		self.collisions()
		self.sim_time += self.impulse_duration

	def physics(self,particle):
		if particle.p_pos.get_z() >= self.max_z:
			self.log_data("Rock bottom pre:{}".format(particle))
			particle.p_vel = Vector3dm.zero_vector()
			particle.p_pos = Vector3dm(particle.p_pos.get_x(),particle.p_pos.get_y(),self.max_z,"c")
			self.log_data("Rock bottom post:{}".format(particle))
			
		else:
			physics_acc = self.gravity * float(self.impulse_duration) / 1000000.0
			self.log_data("physics_acc:{}".format(physics_acc))
			self.log_data("physics particle.acceleration before:{}".format(particle.acceleration))
			particle.acceleration = particle.acceleration.add(Vector3dm(0,0,physics_acc,"c"))
			self.log_data("physics particle.acceleration after:{}".format(particle.acceleration))
		
 
	def collisions(self):
		for el1 in self.particles:
			for el2 in self.particles:
				if self.collision(el1,el2):
					el1.flash_color = COLLISION_COLOR

	def distance_squared(self,el1,el2):
		diff = el1.p_pos.sub(el2.p_pos)
		return (diff.get_x()**2+diff.get_y()**2+diff.get_z()**2)

	def collision(self,el1,el2):
		safe_dist = (el1.size+el2.size)**2
		return self.distance_squared(el1,el2)<safe_dist		

	def draw_text(self,str,font,position):
		global gamedata
		text = font.render(str,1,BLACK)
		gamedata['self.displaysurf'].blit(text,position)
if __name__ == "__main__":
	w = World(1)
	print(w)
	for p in w.particles:
		print(p)
#	input("press return; esc ends")
	w.run()

	