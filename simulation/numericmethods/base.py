""" Base module for numeric calculations"""

class NumericMethod(object):
    """ Base class for solving equestion"""

    def __init__(self,):
        self.system = []

    def calculate(self, system, dt=1):
        """ Main fuction for calculate new postion of all object in  system

            :raises: NotImplementedError
        """
        raise NotImplementedError("Virtual method")

    def acceleration(self, planet1):
        """method for calculate acceleration
        :param planet1: SpaceObject for what there will be calcuations
        :returns: (ax, ay)
        """
        ax, ay = 0.0, 0.0
        for planet2 in self.system:
            if planet1.spaceid == planet2.spaceid:
                continue
            force, radius = planet2.interactions(planet1)
            dx = planet2.x - planet1.x
            dy = planet2.y - planet1.y
            try:
                ax += force/planet1.mass*(dx)/radius if radius > 0 else 0
                ay += force/planet1.mass*(dy)/radius if radius > 0 else 0
            except ZeroDivisionError:
                ax, ay = 0, 0
        return (ax, ay)


class Coefficient(object):
    """Store date for coeffcient """

    def __init__(self, dx, dy, dvx, dvy):
        self.dx, self.dy = dx, dy
        self.dvx, self.dvy = dvx, dvy
