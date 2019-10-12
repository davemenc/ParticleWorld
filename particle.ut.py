import  unittest
import math
from particle import Particle
import sys
sys.path.insert(0, '../vector3dm')
from vector3dm import Vector3dm

class test_particle(unittest.TestCase):
	def test_create_particle(self):
		p = Particle(Vector3dm(1,2,3,"c"),Vector3dm(4,5,6,"c"))
		self.assertAlmostEqual(p.position.get_x(),1),"particle init: x pos bad result: is {} should be {}".format(p.position.get_x(),1)
		self.assertAlmostEqual(p.position.get_y(),2),"particle init: y pos bad result: is {} should be {}".format(p.position.get_y(),2)
		self.assertAlmostEqual(p.position.get_z(),3),"particle init: z pos bad result: is {} should be {}".format(p.position.get_z(),3)
		self.assertAlmostEqual(p.velocity.get_x(),4),"particle init: x vel bad result: is {} should be {}".format(p.position.get_x(),4)
		self.assertAlmostEqual(p.velocity.get_y(),5),"particle init: y vel bad result: is {} should be {}".format(p.position.get_y(),5)
		self.assertAlmostEqual(p.velocity.get_z(),6),"particle init: z vel bad result: is {} should be {}".format(p.position.get_z(),6)
	def test_impulse(self):
		p = Particle(Vector3dm(1,2,3,"c"),Vector3dm(4,5,6,"c"))
		p.acceleration = Vector3dm(8,9,10,"c")
		p.impulse()
		self.assertAlmostEqual(p.velocity.get_x(),12),"particle init: x vel bad result: is {} should be {}".format(p.position.get_x(),12)
		self.assertAlmostEqual(p.velocity.get_y(),14),"particle init: y vel bad result: is {} should be {}".format(p.position.get_y(),14)
		self.assertAlmostEqual(p.velocity.get_z(),16),"particle init: z vel bad result: is {} should be {}".format(p.position.get_z(),16)
		self.assertAlmostEqual(p.position.get_x(),13),"particle init: x pos bad result: is {} should be {}".format(p.position.get_x(),13)
		self.assertAlmostEqual(p.position.get_y(),16),"particle init: y pos bad result: is {} should be {}".format(p.position.get_y(),16)
		self.assertAlmostEqual(p.position.get_z(),19),"particle init: z pos bad result: is {} should be {}".format(p.position.get_z(),19)
		
if __name__ == '__main__':
	unittest.main()		