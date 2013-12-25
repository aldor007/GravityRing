"""Euler method for solving statment"""
import math
import copy
from kivy.logger import Logger
from simulation.numericmethods.base import NumericMethod

class Euler(NumericMethod):
    """Solving equation using method RungaKutta 4 degrea"""
    def __init__(self):
        self.system = list()

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
