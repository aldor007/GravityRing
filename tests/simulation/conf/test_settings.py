import unittest
from simulation.conf.settings import Settings

class SettingsTest(unittest.TestCase):
    """Test case docstring"""

    def test_get(self):
        settings = Settings()
        ret = settings.get('niema', 2)
        self.assertEqual(ret , 2)
    def test_get_ex(self):
        settings = Settings()
        settings['density'] = 0.001
        ret = settings.get('density')
        self.assertEqual(0.001, ret)
    def test_set_valuerr(self):
        settings = Settings()
        settings['density1'] = 'ala1'
        ret = settings.get('density1')
        self.assertEqual('ala1', ret)
    def test_set_tofloat(self):
        settings = Settings()
        settings['densitystr'] = '0.001'
        ret = settings.get('densitystr')
        self.assertEqual(float('0.001'), ret)

