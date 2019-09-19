import  unittest
import math
from particle import Particle
import sys
sys.path.insert(0, '../vector3dm')
from vector3dm import Vector3dm

class test_particle(unittest.TestCase):
	def test_create_particle(self):
		p = Particle(Vector3dm(1,2,3,"c"))
if __name__ == '__main__':
	unittest.main()		