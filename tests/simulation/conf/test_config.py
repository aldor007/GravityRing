import unittest
from simulation.conf import Config

class ConfigTest(unittest.TestCase):
    """Test case docstring"""

    def setUp(self):
        self.data = """
gravityring: 0.1.1 
numericmethod: "RungaKutta"
gravitystrength: 0.0001
density: 0.001
definitions:
    mass:
        big: 4000
        small: 100
    distance:
        big: 200
        small: 300
spacesystem:
    space:
        mass: "mass.big"
        position: "center"
        radius: 20
    planet1:
        mass: "space.mass * 2"
        position: "space.position + 400"
    planet2:
        mass: "planet1.mass + 223"
        x: "distance.big + 100"
        y: 40 
    planet3:
        mass: "planet2.mass + mass.big"
        x: "space.x + 44"
        y: "space.y - 88"

        """
    def test_singelton(self):
        test1 = Config()
        test2 = Config()
        test1['test'] = 1
        self.assertEqual(test1, test2)
    def test_loadfromstring(self):
        test = Config()
        test.loadfromstring(self.data)
        print(test.data)
    def test_get(self):
        test = Config()
        test['jakis'] = 2
        self.assertEqual(test.get('jakis'), 2)
        self.assertEqual(test['jakis'], 2)
    def test_getdefinitions(self):
        test = Config()
        test.loadfromstring(self.data)
        definition = test.get_definitions()
        self.assertTrue('mass' in definition.keys())
    def test_getspacesystem(self):
        test = Config()
        test.loadfromstring(self.data)
        items = test.get_system()
        self.assertTrue('space' in items.keys())
    def test_getspacesystem_err(self):
        test = Config()
        test.data = {}
        items = test.get_system()
        self.assertTrue(len(items.keys()))
        test.loadfromstring(self.data)
    def test_setdata(self):
        test = Config()
        value_set = {"aldor": "dwa"}
        test.data = value_set
        self.assertEqual(test.data, value_set)
    def test_setdataerr(self):
        test = Config()
        value_set = ["aldor", "dwa"]
        self.assertRaises(ValueError, setattr,test, 'data',  value_set)


