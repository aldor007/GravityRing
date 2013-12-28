import unittest
from simulation.conf import Config
from simulation.conf.configparser import ConfigParser
from mock import MagicMock, patch

class ConfigParserTest(unittest.TestCase):
    """Test case docstring"""

    def setUp(self):
        mock_logger = MagicMock()
        self.patch_logger = patch('simulation.conf.configparser.Logger', mock_logger)
        self.patch_logger.start()
        config = Config()
        config.loadfromstring("""
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
system:
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

""")
        self.confparser = ConfigParser(config)

    def tearDown(self):
        self.patch_logger.stop()
    def test_parse(self):
        result = self.confparser.parse()
        for item in result:
            if item.name == 'space':
                self.assertEqual(item.mass, 4000)
