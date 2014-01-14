import unittest
import math
from simulation.numericmethods.base import NumericMethod
from  simulation.system.spacesystem import SpaceObject, SpaceSystem
from simulation.conf.settings import appsettings

class NumericMethodTest(unittest.TestCase):
    """Test case docstring"""

    def setUp(self):
        self.base_num = NumericMethod()

    def test_calculate(self):
        self.assertRaises(Exception, self.base_num.calculate, system = SpaceSystem())
    def test_accelaration(self):
        system = SpaceSystem()
        p1 = SpaceObject(pos=(10.0, 10.0))
        p1.mass = 100.0
        p1.radius_val = 100.0

        p2 = SpaceObject(pos=(100.0, 100.0))
        p2.mass = 100.0
        p2.radius_val = 100.0
        system.append(p1)
        system.append(p2)
        appsettings['gravity'] = 10.0
        self.base_num.system = system
        ret_val = self.base_num.acceleration(p1)
        result = list()
        result.append(10. * 100.0/math.sqrt((90.0**2.0 + 90.0**2.0))**3 *90.0 )
        result.append(10. * 100.0/math.sqrt((90.0**2.0 + 90.0**2.0))**3 *90.0 )
        self.assertEqual(ret_val[0], result[0])
        self.assertEqual(ret_val[1], result[1])
    def test_accelaration_zerp(self):
        system = SpaceSystem()
        p1 = SpaceObject(pos=(10.0, 10.0))
        p1.mass = 0
        p1.radius_val = 100.0

        p2 = SpaceObject(pos=(100.0, 100.0))
        p2.mass = 100.0
        p2.radius_val = 100.0
        system.append(p1)
        system.append(p2)
        appsettings['gravity'] = 10.0
        self.base_num.system = system
        ret_val = self.base_num.acceleration(p1)
        self.assertEqual(ret_val[0], 0)
        self.assertEqual(ret_val[1], 0)
