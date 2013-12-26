"""Implemation of RK4 module"""
import math
import copy
from kivy.logger import Logger
from simulation.numericmethods.base import NumericMethod
from simulation.numericmethods.base import Coefficient

class RungeKutta(NumericMethod):
    """Solving equation using method RungaKutta 4 degrea"""
    def __init__(self):
        self.dt = 1.0
        self.system = list()

    def calculate(self, system, dt=0.1):
        """Main function returning dict of new system"""
        self.system = system
        # self.updateAcceleration()
        new_system = list()
        for planet in self.system:
            # if planet.spaceid != 0:
                # Logger.info(str(planet))
            intermediate = self.intermediate(planet, 0, dt)

            dervative = self.growth(*intermediate, dt=dt)
            planet.x += dervative[0]*dt
            planet.y += dervative[1]*dt
            planet.velocity_x += dervative[2]*dt
            planet.velocity_y += dervative[3]*dt
            new_system.append(planet)
        return new_system



    def evaluate(self, planet, coefficient, t, dt):
        """ calculate new coefficient"""
        tmpplanet = copy.deepcopy(planet)
        tmpplanet.x = planet.x + coefficient.dx*dt
        tmpplanet.y = planet.y + coefficient.dy*dt
        tmpplanet.velocity_x = planet.velocity_x + coefficient.dvx*dt
        tmpplanet.velocity_y = planet.velocity_y + coefficient.dvy*dt
        ax, ay = self.acceleration(tmpplanet)
        return Coefficient(tmpplanet.velocity_x, tmpplanet.velocity_y, ax, ay)

    def intermediate(self, planet, t, dt):
        """caclculate intermediate"""
        tmp = copy.deepcopy(planet)
        k1 = self.evaluate(planet, Coefficient(0., 0., 0., 0.), t, 0)
        k2 = self.evaluate(planet, k1, t, dt*0.5)
        k3 = self.evaluate(planet, k2, t, dt*0.5)
        k4 = self.evaluate(planet, k3, t, dt)
        return k1, k2, k3, k4

    def growth(self, k1, k2, k3, k4, dt):
        """Calculate change of position and velocity"""
        dxdt = dt/6.0 * (k1.dx + 2. * (k2.dx + k3.dx) + k4.dx)
        dydt = dt/6.0 * (k1.dy + 2. * (k2.dy + k3.dy) + k4.dy)
        dvxdt = dt/6. * (k1.dvx + 2. * (k2.dvx + k3.dvx) + k4.dvx)
        dvydt = dt/6. * (k1.dvy + 2. * (k2.dvy + k3.dvy) + k4.dvy)
        return dxdt, dydt, dvxdt, dvydt
