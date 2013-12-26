import unittest
from simulation.system.solarsystem import Force
from simulation.system.solarsystem import SpaceObjectBase
from simulation.conf.settings import appsettings
from mock import MagicMock, patch
class ForceTest(unittest.TestCase):
    """Test case docstring"""

    def setUp(self):
        self.p1 = SpaceObjectBase()
        self.p2 = SpaceObjectBase()
        self.data = { 'p1': {
                    'pos': (10., 10.),
                    'mass': 100.
                    }, 
                'p2': {
                    'pos': (100., 100),
                    'mass': 100.
                    }
                }
        self.p1.pos = self.data['p1']['pos']
        self.p1.mass = self.data['p1']['mass']
        self.p2.pos = self.data['p2']['pos']
        self.p2.mass = self.data['p2']['mass']
        self.p1.radius_val = 19
        self.p2.radius_val = 19
        self.distance = (self.p1.x - self.p2.x)**2 + (self.p1.y - self.p2.y)**2

    def test_draw(self):
        mock_draw = MagicMock()
        patch_draw = patch('simulation.system.solarsystem.Line', mock_draw)
        patch_draw.start()
        test = Force(self.p1, self.p2, 1)
        test.draw([0, 0], 2)
        patch_draw.stop()
        self.assertTrue(mock_draw.called)
    def test_str(self):
        test = Force(self.p1, self.p2, 1)
        ret_val = str(test)
        self.assertTrue(isinstance(ret_val, str))
    def test_zerodistance(self):
        test = Force(self.p1, self.p2, 0)
        self.assertEqual(test.value, 0)

    def test_init_calculate(self):
        appsettings['gravity'] = 10
        test = Force(self.p1, self.p2, self.distance)
        result = appsettings['gravity'] * self.data['p1']['mass'] * self.data['p2']['mass']/self.distance
        self.assertEqual(test.value, result)
        self.assertEqual(test.calculate(self.p1.mass, self.p2.mass, self.distance), result)
