import sys
import math
import time
import random

sys.path.insert(0, '../vector3dm')
from vector3dm import Vector3dm
		

def rand_vector(v,min_dist,max_dist):

	min_x = -500
	max_x = 500	
	min_y = -500
	max_y = 500	
	min_z = 0
	max_z = 1000

	dist = random.random()*(max_dist-min_dist)+min_dist	
	theta = random.random()*2*math.pi
	phi = random.random()*math.pi
	
	old_v = Vector3dm(dist,theta,phi,"s").add(v)
	v = old_v.convert_to_cartesian()
	x,y,z = v.vals
	#print(v,x,y,z)
	#bad_vec = False
	#if x>max_x or x<min_x or y>max_y or y<min_y or z>max_z or z<min_z:
	#	bad_vec = True
	if x>max_x:
		v.set_x(max_x)
	elif x<min_x:
		v.set_x(min_x)
	if y>max_y:
		v.set_y(max_y)
	elif y<min_y:
		v.set_y(min_y)
	if z>max_z:
		v.set_z(max_z)
	elif z<min_z:
		v.set_z(min_z)
	#if bad_vec:
	#	print("bad vec",dist,old_v.convert_to_cartesian(),v)
	return v
v = Vector3dm.zero_vector()

for i in range(0,3000):
	print("{}\t{}".format(v.get_x(),v.get_z()))
	v = rand_vector(v,90,150)

	
	#print(rand_vector(300))
#for phi_deg in range(0,91,1):
#	for theta_deg in range(0,361,1):
#		phi = math.radians(phi_deg)
#		theta = math.radians(theta_deg)
#		v = Vector3dm(300,theta,phi,"s")
#		if v.convert_to_cartesian().get_z() < 0:
#			print(theta_deg,phi_deg,"||",v,"||",v.convert_to_cartesian())