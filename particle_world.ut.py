import  unittest
import math
import sys
from particle_world import World
from particle_world import Particle
sys.path.insert(0, '../vector3dm')
from vector3dm import Vector3dm

class test_world(unittest.TestCase):
	def test_aero_acc(self):
		p = Particle(Vector3dm(10,10,10,"c"),Vector3dm(0,10,0,"c"))
		drag = p.aero_acc().convert_to_cartesian()
		self.assertAlmostEqual(drag.get_y(),-5),"aero drag: drag wrong: is {} should be {}".format(drag,-5)
		
	def	test_random_position(self):
		max = 20
		w = World(1,max,max,max)
		v = w.random_position()
		x = v.get_x()
		y = v.get_y()
		z = v.get_z()
		self.assertLessEqual(x,max)
		self.assertGreaterEqual(x,-max)
		self.assertLessEqual(y,max)
		self.assertGreaterEqual(y,-max)
		self.assertLessEqual(z,max)
		self.assertGreaterEqual(z,-max)
		
	def test_create_world(self):
		w = World(10,1000,1000,1000,wall_type=0)
		self.assertEqual(w.width, 1000)
		self.assertEqual(w.height, 1000)
		self.assertEqual(w.depth, 1000)
		self.assertEqual(len(w.particles), 10),"world creation wrong particle count"
		self.assertEqual(w.wall_type,0),"world creation wrong wall type"

	def test_create_particle(self):
		p = Particle(Vector3dm(1,2,3,"c"),Vector3dm(4,5,6,"c"))
		self.assertAlmostEqual(p.position.get_x(),1),"particle init: x pos bad result: is {} should be {}".format(p.position.get_x(),1)
		self.assertAlmostEqual(p.position.get_y(),2),"particle init: y pos bad result: is {} should be {}".format(p.position.get_y(),2)
		self.assertAlmostEqual(p.position.get_z(),3),"particle init: z pos bad result: is {} should be {}".format(p.position.get_z(),3)
		self.assertAlmostEqual(p.velocity.get_x(),4),"particle init: x vel bad result: is {} should be {}".format(p.position.get_x(),4)
		self.assertAlmostEqual(p.velocity.get_y(),5),"particle init: y vel bad result: is {} should be {}".format(p.position.get_y(),5)
		self.assertAlmostEqual(p.velocity.get_z(),6),"particle init: z vel bad result: is {} should be {}".format(p.position.get_z(),6)

	def test_random_goal(self):
		w = World(1,40,40,40)
		pos = Vector3dm(0,0,0,"c")
		goal = w.random_goal(pos,100,500)
		x,y,z = goal.convert_to_cartesian().vals
		self.assertLessEqual(x,20)
		self.assertLessEqual(y,20)
		self.assertLessEqual(z,40)
		self.assertGreaterEqual(x,-20)
		self.assertGreaterEqual(y,-20)
		self.assertGreaterEqual(z,0)
		

if __name__ == '__main__':
	unittest.main()		

