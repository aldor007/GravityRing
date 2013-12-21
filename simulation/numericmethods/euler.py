"""Euler method for solving statment"""
import math
import copy
from kivy.logger import Logger
from simulation.numericmethods.base import NumericMethod
from simulation.numericmethods.base import Coeffcient
from simulation.numericmethods.base import Derivative

class Euler(NumericMethod):
    """Solving equation using method RungaKutta 4 degrea"""
    def __init__(self):
        self.h = 1.0
        self.system = list()
    # def calculate(self, system):
    #     self.system = system
    #     for planet in self.system:


    # def initialCoefficent(self, planet):

    # def accceleration(self, planet1):
    #     ax, ay = 0.0, 0.0
    #     for planet2 in self.system:
    #         if planet1.spaceid != planet2.spaceid:
    #             force, radius = planet1.interactions(planet2)
    #             try:
    #                 ax += planet2.mass / math.fabs(planet1.x-planet2.x)**3 *  (planet1.x -planet2.x)
    #                 ay += planet2.mass / math.fabs(planet1.y-planet2.y)**3 *  (planet1.y -planet2.y)
    #             except ZeroDivisionError:
    #                 ax += 0
    #                 ay += 0

    #     return ax, ay

    # def accceleration(self, planet1):
    #     ax, ay = 0.0, 0.0
    #     for planet2 in self.system:
    #         if planet1.spaceid != planet2.spaceid:
    #             force, radius = planet1.interactions(planet2)
    #             ax += force*(planet1.x-planet2.x)/radius
    #             ay += force*(planet1.y-planet2.y)/radius
    #     return ax, ay

    def calculate(self, system, dt=0.1):
        """Main function returning dict of new system"""
        self.system = system
        new_system = list()
        for planet in self.system:
            if planet.spaceid != 0:
                axold, ayold = self.acceleration(planet)
                planet.x += planet.velocity_x * self.h * dt
                planet.y += planet.velocity_y  * self.h * dt
                planet.velocity_x += axold  * self.h * dt
                planet.velocity_y += ayold * self.h * dt
            new_system.append(planet)

        return new_system
