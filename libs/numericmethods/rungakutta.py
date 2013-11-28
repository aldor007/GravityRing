from  libs.numericmethods.base import Numeric
from  libs.numericmethods.base import Coeffcient
from  libs.numericmethods.base import Derivative

class RungaKutta(Numeric):
    def __init__(self):
        self.h = 1.0

    def calculate(self, system, dt=0):
        self.system = system
        self.updateAcceleration(system)
        for planet in system:
            intermediate = self.intermediate(planet, 0, 1)
            dervative = self.growth(*intermediate)
            planet.x += dervative[0]*dt
            planet.y += dervative[1]*dt
            planet.velocity_x += dervative[2]*dt
            planet.velocity_y += dervative[3]*dt
        return system

    def updateAcceleration(self, system):
        for planet1 in system:
            ax, ay = 0, 0
            for planet2 in system:
                if planet1 is planet2:
                    continue
                force, radius = planet1.interactions(planet2)
                ax += (force*planet1.x-planet2.x)/radius
                ay += (force*planet1.y-planet2.y)/radius
            planet1.accelation_x = ax
            planet1.accelation_y = ay
    
    def initCoeffcients(self, planet, t, dt):
        return Coeffcient(planet.accelation_x, planet.accelation_y, planet.velocity_x, planet.velocity_y)
    def Coeffcient(self, planet, coeffcient,t, dt):
        x = planet.x + coeffcient._dx*dt
        y = planet.y + coeffcient._dy*dt
        vx = planet.velocity_x + int(coeffcient._dvx*dt)
        vy = planet.velocity_y + int(coeffcient._dvy*dt)
        
        ax, ay = planet.accelation_x, planet.accelation_y
        return Coeffcient(vx, vy, ax, ay)
    
    def intermediate(self, planet, t, dt):
        k1 = self.initCoeffcients(planet, t, dt)
        k2 = self.Coeffcient(planet, k1, t, dt*self.h/2.)
        k3 = self.Coeffcient(planet, k2, t, dt*self.h/2.)
        k4 = self.Coeffcient(planet, k3, t, dt)
        return k1, k2, k3, k4
    
    def growth(self, k1, k2, k3, k4):
        dxdt = self.h/6.0 * (k1._dx + 2.* (k2._dx + k3._dx) + k4._dx)
        dydt = self.h/6.0 * (k1._dx + 2.* (k2._dx + k3._dx) + k4._dx)
        dvxdt = self.h/6. *(k1._dvx + 2. * (k2._dvx + k3._dvx) + k4._dvx)
        dvydt = self.h/6. *(k1._dvy + 2. * (k2._dvy + k3._dvy) + k4._dvy)
        return dxdt, dydt, dvxdt, dvydt
