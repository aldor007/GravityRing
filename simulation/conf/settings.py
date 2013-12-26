from utils import Singleton
from kivy.logger import Logger

class Settings(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.__settings = {
                'dt_in_numericmethod': 1.0,
                'numericmethod': 'RungeKutta',
                'gravity': 14.0,
                'density': 0.001,
                'calculation_speed': 100,
                'zoom': 1.0
                }

    def get(self, key, default=None):
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
