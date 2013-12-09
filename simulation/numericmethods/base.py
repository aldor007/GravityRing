""" Base module for numeric calculations"""

class NumericMethod(object):
    """ Base class for solving equestion"""
    def __inti__(self):
        self.classname = type(self).__name__

    def calculate(self, system, dt=1):
        """ Main fuction for calculate new postion of all object in  system"""
        raise NotImplemented("Virtual method")


class Derivative(object):
    """Store date for detricatie """
    def __init__(self, vx, vy, ax, ay):
        self._dvx, self._dvy = vx, vy
        self._dax, self._day = ax, ay
#TODO: Check typ in names

class Coeffcient(object):
    """Store date for coeffcient """

    def __init__(self, dx, dy, dvx, dvy):
        self.dx, self.dy = dx, dy
        self.dvx, self.dvy = dvx, dvy
