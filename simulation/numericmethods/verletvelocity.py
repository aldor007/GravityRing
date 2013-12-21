"""Modul for resolving Verlet"""
import copy
from kivy.logger import Logger
from simulation.numericmethods.base import NumericMethod
from simulation.numericmethods.base import Coeffcient
from simulation.numericmethods.base import Derivative

class VerletVerlocity(NumericMethod):
    """Solving equation using method RungaKutta 4 degrea"""
    def __init__(self):
        self.h = 1.0
        self.system = list()
    # def calculate(self, system):
    #     self.system = system
    #     for planet in self.system:


    # def initialCoefficent(self, planet):
        



    def calculate(self, system, dt=1):
        """Main function returning dict of new system"""
        self.system = system
        # self.updateAcceleration()
        new_system = list()
        oldacc_x, oldacc_y = 0, 0
        for planet in self.system:
            # if planet.spaceid != 0:
                # Logger.info(str(planet))

            ax, ay = self.acceleration(planet)
            planet.x += planet.velocity_x * dt + 0.5 * oldacc_x * dt * dt
            planet.y += planet.velocity_y * dt + 0.5 * oldacc_y * dt * dt
            planet.velocity_x += 0.5 * (ax + oldacc_x) * dt
            planet.velocity_y += 0.5 * (ay + oldacc_y) * dt
            new_system.append(planet)
        return new_system




    def evaluate(self, planet, coeffcient, t, dt):
        """ calculate new coeffcient"""
        tmpplanet = copy.deepcopy(planet)
        tmpplanet.x = planet.x + coeffcient.dx*dt
        tmpplanet.y = planet.y + coeffcient.dy*dt
        tmpplanet.velocity_x = planet.velocity_x + coeffcient.dvx*dt
        tmpplanet.velocity_y = planet.velocity_y + coeffcient.dvy*dt
        ax, ay = self.acceleration(tmpplanet)
        return Coeffcient(tmpplanet.velocity_x, tmpplanet.velocity_y, ax, ay)

    def intermediate(self, planet, t, dt):
        """caclculate intermediate"""
        tmp = copy.deepcopy(planet)
        k1 = self.evaluate(planet, Coeffcient(0., 0., 0., 0.), t, 0)
        k2 = self.evaluate(planet, k1, t, dt*0.5)
        k3 = self.evaluate(planet, k2, t, dt*0.5)
        k4 = self.evaluate(planet, k3, t, dt)
        return k1, k2, k3, k4

    def growth(self, k1, k2, k3, k4):
        """Calculate change of position and velocity"""
        dxdt = self.h/6.0 * (k1.dx + 2. * (k2.dx + k3.dx) + k4.dx)
        dydt = self.h/6.0 * (k1.dy + 2. * (k2.dy + k3.dy) + k4.dy)
        dvxdt = self.h/6. * (k1.dvx + 2. * (k2.dvx + k3.dvx) + k4.dvx)
        dvydt = self.h/6. * (k1.dvy + 2. * (k2.dvy + k3.dvy) + k4.dvy)
        return dxdt, dydt, dvxdt, dvydt
