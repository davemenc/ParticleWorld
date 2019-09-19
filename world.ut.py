import  unittest
import math
from particle import Particle
from world import World
import sys
sys.path.insert(0, '../vector3dm')
from vector3dm import Vector3dm

class test_world(unittest.TestCase):
	def test_create_world(self):
		w = World(1000,1000,1000,wall_type=0)
		self.assertEqual(w.width, 1000)
		self.assertEqual(w.height, 1000)
		self.assertEqual(w.depth, 1000)
		
if __name__ == '__main__':
	unittest.main()