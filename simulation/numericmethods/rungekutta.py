"""Implemation of RK4 module"""
import copy
from simulation.numericmethods.base import NumericMethod
from simulation.numericmethods.base import Coefficient

class RungeKutta(NumericMethod):
    """Solving equation using method RungeKutta 4 degrea"""
    def __init__(self):
        super(RungeKutta, self).__init__()

    def calculate(self, system, dt=0.1):
        """Main function returning dict of new system
        :param system: list of spaceobjects.
        :para dt: time step.
        :returns: new list of spaceobjects."""
        self.system = system
        # self.updateAcceleration()
        new_system = list()
        for planet in self.system:
            # if planet.spaceid != 0:
                # Logger.info(str(planet))
            intermediate = self.intermediate(planet, dt)

            dervative = self.growth(*intermediate, dt=dt)
            planet.x += dervative[0] * dt
            planet.y += dervative[1] * dt
            planet.velocity_x += dervative[2]*dt
            planet.velocity_y += dervative[3]*dt
            new_system.append(planet)
        return new_system



    def evaluate(self, planet, coefficient,  dt):
        """ calculate new coefficient

        :param planet: SpaceObject.
        :param coefficient: Coefficient  for calculations.
        :param dt: time step.
        :returns:  Coefficient.
        """
        tmpplanet = copy.deepcopy(planet)
        tmpplanet.x = planet.x + coefficient.dx*dt
        tmpplanet.y = planet.y + coefficient.dy*dt
        tmpplanet.velocity_x = planet.velocity_x + coefficient.dvx*dt
        tmpplanet.velocity_y = planet.velocity_y + coefficient.dvy*dt
        ax, ay = self.acceleration(tmpplanet)
        return Coefficient(tmpplanet.velocity_x, tmpplanet.velocity_y, ax, ay)

    def intermediate(self, planet,  dt):
        """caclculate iAntermediate

        :param planet: SpaceObject.
        :param dt: time step.
        :returns: touple of Coefficient.
        """
        k1 = self.evaluate(planet, Coefficient(0., 0., 0., 0.), 0)
        k2 = self.evaluate(planet, k1, dt*0.5)
        k3 = self.evaluate(planet, k2, dt*0.5)
        k4 = self.evaluate(planet, k3, dt)
        return k1, k2, k3, k4

    def growth(self, k1, k2, k3, k4, dt):
        """Calculate change of position and velocity

        :param k1: Coefficient.
        :param k2: Coefficient.
        :param k3: Coefficient.
        :param k4: Coefficient.
        :param dt: time steep.

        :returns: toupe of changes postion and velocity.
        """
        dxdt = dt/6.0 * (k1.dx + 2. * (k2.dx + k3.dx) + k4.dx)
        dydt = dt/6.0 * (k1.dy + 2. * (k2.dy + k3.dy) + k4.dy)
        dvxdt = dt/6. * (k1.dvx + 2. * (k2.dvx + k3.dvx) + k4.dvx)
        dvydt = dt/6. * (k1.dvy + 2. * (k2.dvy + k3.dvy) + k4.dvy)
        return dxdt, dydt, dvxdt, dvydt
