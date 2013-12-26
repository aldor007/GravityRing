"""Modul for resolving Verlet"""
from simulation.numericmethods.base import NumericMethod

class VerletVelocity(NumericMethod):
    """Solving equation using method RungaKutta 4 degrea"""
    def __init__(self):
        super(VerletVelocity, self).__init__()

    def calculate(self, system, dt=1):
        """Main function returning dict of new system

        :param system: list of spaceobjects.
        :param dt: time step.
        :returns: new list of spaceobjects.
        """
        self.system = system
        new_system = list()
        oldacc_x, oldacc_y = 0, 0
        for planet in self.system:
            ax, ay = self.acceleration(planet)
            planet.x += planet.velocity_x * dt + 0.5 * oldacc_x * dt * dt
            planet.y += planet.velocity_y * dt + 0.5 * oldacc_y * dt * dt
            planet.velocity_x += 0.5 * (ax + oldacc_x) * dt
            planet.velocity_y += 0.5 * (ay + oldacc_y) * dt
            new_system.append(planet)
        return new_system
