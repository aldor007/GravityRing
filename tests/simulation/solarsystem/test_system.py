import unittest
import random
from simulation.system.solarsystem import SolarSystem, Force

class SolarSystemTest(unittest.TestCase):
    """Test case docstring"""
    def test_point_not_in(self):
        system = SolarSystem()
        self.assertFalse(system.points_in_system(0, 0))
    def test_clear(self):
        system = SolarSystem()
        system.append("ala")
        system.clear()
        self.assertEqual(system.system,list())
    def test_get_system(self):
        system = SolarSystem()
        system.append("ala")
        self.assertEqual(system.system,system.get_system())

    def test_len(self):
        system = SolarSystem()
        system.append("ala")
        self.assertEqual(len(system), 1)

    def test_setdata(self):
        test = SolarSystem()
        value_set = list("aldor")
        test.data = value_set
        self.assertEqual(test.data, value_set)

