import unittest
import random
from mock import MagicMock, patch
import copy
from simulation.system.solarsystem import SpaceObject

class  SpaceObjectTest(unittest.TestCase):
    """Test case docstring"""
    def test_clear_init(self):
        test = SpaceObject(pos=(0,0))
        setters = ('x', 'y', 'velocity_x', 'velocity_y')
        for item in setters:
            self.assertEqual(getattr(test, item), 0)

    def test_property(self):
        test = SpaceObject(pos=(1, 1))
        setters = ('x', 'y', 'velocity_x', 'velocity_y')
        for item in setters:
            value = 5 * 5 + random.randint(0,5)
            setattr(test, item, value)
            ret_val = getattr(test, item)
            self.assertEqual(value, ret_val)
    def test_str(self):
        test = SpaceObject(pos=(0,0))
        ret_val = str(test)
        self.assertTrue(isinstance(ret_val, str))
    def test_eq(self):
        test1 = SpaceObject(pos=(1,1))
        test2 = SpaceObject(pos=(1,1))
        self.assertTrue(test1 == test2)
    def test_noteq(self):
        test1 = SpaceObject(pos=(3,3))
        test2 = SpaceObject(pos=(1,1))
        self.assertTrue(test1 != test2)
    def test_collision(self):
        test1 = SpaceObject(pos=(3,3))
        test2 = SpaceObject(pos=(3,3))
        self.assertTrue(test1.collision(test2))
    def test_no_collision(self):
        test1 = SpaceObject(pos=(3,3))
        test2 = SpaceObject(pos=(30,30))
        self.assertFalse(test1.collision(test2))
    def test_collision2(self):
        test1 = SpaceObject(pos=(0,0))
        test2 = SpaceObject(pos=(0,10))
        self.assertTrue(test1.collision(test2))
    def test_merge(self):
        test2 = SpaceObject(pos=(0,10))
        test1 = SpaceObject(pos=(0,0))
        test1.merge(test2)
        self.assertEqual(len(SpaceObject.mergedforces), 1)
        self.assertTrue(test2.merged)
    def test_merge_cleanup(self):
        test1 = SpaceObject(pos=(3,3))
        test2 = SpaceObject(pos=(30,30))
        test1.interactions(test2)
        self.assertEqual(len(test1.forces.keys()), 1)
        test1.merge(test2)
        self.assertEqual(len(test1.forces.keys()), 0)
    def test_draw_noforces(self):
        mock_draw = MagicMock()
        patch_draw = patch('simulation.system.solarsystem.Ellipse', mock_draw)
        patch_draw.start()
        test = SpaceObject(pos=(0,0))
        test.draw(None, 2, 3, 4)
        patch_draw.stop()
        self.assertTrue(mock_draw.called)
    def test_draw_forces(self):
        mock_draw = MagicMock()
        mock_forces = MagicMock()
        mock_forces.draw = MagicMock()
        mock_forces.draw.return_value = True

        patch_draw = patch('simulation.system.solarsystem.Ellipse', mock_draw)
        patch_draw.start()
        test = SpaceObject(pos=(0,0))
        test.forces[1] = mock_forces
        test.draw(None, 2, 3, 4)
        patch_draw.stop()
        self.assertTrue(mock_draw.called)
        self.assertTrue(mock_forces.draw.called)
    def test_copy(self):
        test1 = SpaceObject(pos=(10., 10), radius=100)
        testcopy = copy.deepcopy(test1)
        setters = ('x', 'y', 'velocity_x', 'velocity_y')
        for item in setters:
            ret_val = getattr(test1, item)
            self.assertEqual(ret_val,getattr(testcopy, item))
