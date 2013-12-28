import unittest
from simulation.numericmethods.rungekutta import RungeKutta
from simulation.system.spacesystem import SpaceObject
from mock import patch, MagicMock

class RungeKuttaTest(unittest.TestCase):
    """Test case docstring"""

    def setUp(self):
        pass

    def test_calculate_empty(self):
        method = RungeKutta()
        emptylist = list()
        ret = method.calculate(emptylist)
        self.assertEqual(ret, emptylist)
    def test_calculate_one(self):
        method = RungeKutta()
        syslist = list()
        syslist.append(SpaceObject(pos=[10, 10]))
        ret = method.calculate(syslist)
        self.assertEqual(ret, syslist)
