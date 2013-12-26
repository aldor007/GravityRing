""" Base module for numeric calculations"""
import math

class NumericMethod(object):
    """ Base class for solving equestion"""

    def __init__(self, system=list()):
        self.system = system

    def calculate(self, system, dt=1):
        """ Main fuction for calculate new postion of all object in  system"""
        raise NotImplemented("Virtual method")

    def acceleration(self, planet1):
        """method for calculate acceleration"""
        ax, ay = 0.0, 0.0
        for planet2 in self.system:
            if planet1.spaceid == planet2.spaceid:
                continue
            force, radius = planet2.interactions(planet1)
            dx = planet2.x - planet1.x
            dy = planet2.y - planet1.y
            ax += force/planet1.mass*(dx)/radius
            ay += force/planet1.mass*(dy)/radius
        return (ax, ay)


class Coefficient(object):
    """Store date for coeffcient """

    def __init__(self, dx, dy, dvx, dvy):
        self.dx, self.dy = dx, dy
        self.dvx, self.dvy = dvx, dvy
