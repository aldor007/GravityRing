"""Module containing class for settings of simulation"""
from utils import Singleton
from utils import ListBase

class Settings(ListBase):
    """Class containing settings of simulation"""
    __metaclass__ = Singleton

    def __init__(self):
        """Set default value of settings """
        self.__settings = {
                'dt_in_numericmethod': 1.0,
                'numericmethod': 'RungeKutta',
                'gravity': 14.0,
                'density': 0.001,
                'calculation_speed': 100,
                'zoom': 1.0
                }

    @property
    def data(self):
        """Basic property getter"""
        return self.__settings

    @data.setter
    def data(self, value):
        """Basic property setter"""
        if type(value) is list:
            raise ValueError("Unsuported type")

        self.__settings = value

    def get(self, key, default=None):
        """ Return value of key
        :param key: string
        :param default: default value if key doesn't exist
        :returns: value of key
        """
        try:
            return self.__settings[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        return self.__settings[key]

    # def __getattr__(self, key):
    #     return self.__settings[key]

    # def __setattr__(self, value):
    #     self.__settings = float(value)

    def __setitem__(self, key, value):
        try:
            self.__settings[key] = float(value)
        except ValueError:
            self.__settings[key] = value


appsettings = Settings()
