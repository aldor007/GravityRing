import unittest
from simulation.numericmethods.verletvelocity import VerletVelocity
from simulation.system.solarsystem import SpaceObject
from mock import patch, MagicMock
class VerletVelocityTest(unittest.TestCase):
    """Test case docstring"""

    def setUp(self):
        pass

    def test_calculate_empty(self):
        method = VerletVelocity()
        emptylist = list()
        ret = method.calculate(emptylist)
        self.assertEqual(ret, emptylist)
    def test_calculate_one(self):
        method = VerletVelocity()
        syslist = list()
        syslist.append(SpaceObject(pos=[10, 10]))
        ret = method.calculate(syslist)
        self.assertEqual(ret, syslist)
