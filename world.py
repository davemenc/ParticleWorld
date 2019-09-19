import math
from particle import Particle
import pygame

import sys
sys.path.insert(0, '../vector3dm')
from vector3dm import Vector3dm

class World:
	def __init__(self,width,depth,height,wall_type=0):
		# world dimensions
		self.width = float(width) # total x dimension
		self.depth = float(depth) # total y dimension
		self.height = float(height) # total z dimension
		self.min_x = -width/2 # x coordinate of left wall
		self.min_y = -depth/2 # y coordinate of back wall
		self.min_z = 0.0 #z coordinate of floor
		self.max_x = width - self.min_x
		self.max_y = depth - self.min_y
		self.max_z = depth - self.min_z

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
		
		self.objects = [] # list of objects
		self.collisions = [] # list of collisions in this impulse
		self.sections = [] # list of sections
		
		# Display Parameters
		self.screen_size_width = 1600 
		self.screen_size_height = 1000
		self.display_world_width = self.width #allows you to clip off the edges
		self.left_clip = 0
		self.right_clip = 0
		self.world_height = self.height #allows you to clip off the top
		self.top_clip = 0
		self.display = None
		self.pixel_width_ratio = None
		self.pixel_height_ratio = None

	def __repr__(self):
		return "width: {}; depth: {}; height: {}; type: {}".format(self.width,self.depth,self.height,self.wall_type_desc)
		
	def init_screen(self,screen_width=None,screen_height=None,world_width=None,world_height=None):
		""" Set up the screen based on parameters; optionally, can be changed."""
		
		# how big is the screen & what is it's relationship to the world
		if screen_width is not None:
			self.screen_size_width = screen_width
		if screen_height is not None:
			self.screen_size_height - screen_height
		if world_width is not None:
			self.world_width = world_width
		if world_height is not None:
			self.world_height = world_height
		
if __name__ == "__main__":
	print(World(1000,1000,1000,wall_type=0))
	