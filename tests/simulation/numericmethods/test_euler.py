import unittest
from simulation.numericmethods.euler import Euler
from simulation.system.spacesystem import SpaceObject
from mock import patch, MagicMock
class EulerTest(unittest.TestCase):
    """Test case docstring"""

    def setUp(self):
        pass

    def test_calculate_empty(self):
        euler = Euler()
        emptylist = list()
        ret = euler.calculate(emptylist)
        self.assertEqual(ret, emptylist)
    def test_calculate_one(self):
        method = Euler()
        syslist = list()
        syslist.append(SpaceObject(pos=[10, 10]))
        ret = method.calculate(syslist)
        self.assertEqual(ret, syslist)
        pass
