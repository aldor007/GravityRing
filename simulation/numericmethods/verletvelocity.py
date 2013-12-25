"""Modul for resolving Verlet"""
import copy
from kivy.logger import Logger
from simulation.numericmethods.base import NumericMethod

class VerletVerlocity(NumericMethod):
    """Solving equation using method RungaKutta 4 degrea"""
    def __init__(self):
        self.system = list()

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


