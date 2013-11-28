""" Base module for numeric calculations"""

class Numeric(object):
    
    def calculate(self, system, dt=1):
        raise NotImplemented("Virtual method")


class Derivative(object):

    def __init__(self, vx, vy, ax, ay):
        self._dvx, self._dvy = vx, vy
        self._dax, self._day = ax, ay

class Coeffcient(object):

    def __init__(self, x, y, vx, vy):
        self._dx, self._dy = x, y
        self._dvx, self._dvy = vx, vy
