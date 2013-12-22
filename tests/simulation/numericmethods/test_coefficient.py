import unittest
from simulation.numericmethods.base import Coefficient
class CoefficentTest(unittest.TestCase):
    """Test case docstring"""


    def test_set(self):
        test = Coefficient(1.0, 2.0, 3.0, 4.0)
        self.assertEqual(test.dx, 1.0)
        self.assertEqual(test.dy, 2.0)
        self.assertEqual(test.dvx, 3.0)
        self.assertEqual(test.dvy, 4.0)
