import unittest
from simulation.system.spacesystem import SpaceObjectBase
import random

class  SpaceObjectBaseTest(unittest.TestCase):
    """Test case docstring"""
    def test_clear_init(self):
        test = SpaceObjectBase()
        setters = ('x', 'y', 'velocity_x', 'velocity_y')
        for item in setters:
            self.assertEqual(getattr(test, item), 0)

    def test_property(self):
        test = SpaceObjectBase()
        setters = ('x', 'y', 'velocity_x', 'velocity_y','position')
        for item in setters:
            value = 5 * 5 + random.randint(0,5)
            setattr(test, item, value)
            ret_val = getattr(test, item)
            self.assertEqual(value, ret_val)
    def test_str(self):
        test = SpaceObjectBase()
        ret_val = str(test)
        self.assertTrue(isinstance(ret_val, str))
