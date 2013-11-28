# 
import kivy
kivy.require('1.0.9')
from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import NumericProperty
from kivy.properties import ReferenceListProperty
from kivy.properties import ObjectProperty
from kivy.vector import Vector
from random import randint
from kivy.clock import Clock
from kivy.logger import Logger
import math
import copy

GRAVITYSTRENGTH = 1e10
DENSITY = 0.01

class Numeric(object):
    def calculate(self, system, dt=1 ):
        raise NotImplemented("Virtual method")
class Derivative(object):
    def __init__(self, vx, vy, ax, ay):
        self._dvx, self._dvy = vx, vy
        self._dax, self._day = ax, ay
class Coeffcient(object):
    def __init__(self, x, y, vx, vy):
        self._dx, self._dy = x, y
        self._dvx, self._dvy = vx, vy
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
                ax += (force*planet.x-planet.x)/radius
                ay += (force*planet.y-planet.y)/radius
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

class Force(Widget):
    length = 0
    gravitystrength = GRAVITYSTRENGTH

    def calulate(self, mass1, mass2, distance):
        self.value = GRAVITYSTRENGTH * mass1*mass2/distance
        return self.value
    def __init__(self, spaceobject1, spaceobject2, **kwargs):
        super(Widget, self).__init__(**kwargs)
        self.vector = (spaceobject1.x - spaceobject2.x, spaceobject1.y - spaceobject2.y )
        self.value = self.calulate(mass1, mass2, distancesqured)
    def draw(self, canvas, startpos):
        with canvas:
            Line(pos=[self.endpos, startpos], widht=5)




class SpaceObject(object):

    objectcount = 0
    mergedforces = list()
    def __init__(self, radius = 10, **kwargs):
        self.spaceid = SpaceObject.objectcount + 1
        SpaceObject.objectcount += 1
        self.forces = {}
        self.radius = radius
        self.color = (randint(0, 1), randint(0, 1), randint(0, 1) )
        self.mass = DENSITY*4.*math.pi*(self.radius**3.)/3.
        self.accelation_x = 0
        self.accelation_y = 0
        self.accelation = ReferenceListProperty(self.accelation_x, self.accelation_y)
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity = ReferenceListProperty(self.velocity_x, self.velocity_y)
        self.merge = False
        # Widget.__init__(self, **kwargs)

    def interactions(self, other):
        """ Returns force, distance betwen two objects"""
        distancex = self.x - other.x
        distancey = self.y - other.y
        distancesqured = distancex*distancex + distancey*distancey
        distance = math.sqrt(distancesqured)
        self.calcutateforces(distancesqured, other.spaceid)
        return self.forces[other.spaceid], distance
        # self.__cleanup()
        # distancex = self.x - other.x
        # distancey = self.y - other.y
        # self.calcutateforces( distancex, distancey, other.spaceid)
        
    def __cleanup(self):
        for item in mergedforces:
            if item in self.forces.keys():
                del self.forces[item]
    def draw(self, canvas):
        with canvas:
            c = Color(self.color, mode='hsv')
            Ellipse(pos=self.pos, size=(self.radius, self.radius))
    
    def merge(self, other):
        self.mass = other.mass
        self.radius = (3. * self.mass/(DENSITY *4. * math.pi))**(1./3.)
        other.merged = True
        del self.forces[other.spaceid]
        SpaceObject.mergedforces.append(other.spaceid)

    def calcutateforces(self, distancesqured, other):
        # self.forces[other.spaceid] = 
        # distancesqured = distancex*distancex + distancey*distancey
        self.forces[other.spaceid] = Force(other.pos, other.mass, self.mass, distancesqured)
        return self.forces[other.spaceid].value


    def collision(self, other):
        distancex = self.x - other.x
        distancey = self.y - other.y
        distance = math.sqrt(distancex**2 + distancey**2)
        return distance <= (self.radius - other.radius)
    # def __eq__(self, other):
    #     return self.x == other.x and self.y == other.y

class SolarSystem(object):
    
    def __init__(self, speed = 1):
        self.gravity = GRAVITYSTRENGTH
        self.system = list()
        self.matmethod = RungaKutta()
    def update(self):
        items_merged = list()
        self.system = self.matmethod.calculate(self.system)
        
        # for item in self.system:
        #     tmp = copy.deepcopy(self.system)
        #     del tmp[self.system.index(item)]
        #     for item2 in tmp:
        #         if item.collision(item2):
        #             #TODO
        #             pass
        # for todelete in items_merged:
        #     del self.system[todelete]


    def append(self, spaceobject):
        self.system.append(spaceobject)
    
    def get_system(self):
        return self.system

    def __len__(self):
        return len(self.system)
    
    def __getitem__(self, key):
        return self.system[key]
    
    def __setitem__(self, key, value):
        self.system[key] = value
    
    def __delitem__(self, key):
        del self.system[key]
    
    def __iter__(self):
        return self.system.__iter__()

class GravityRing(Widget):
    solarsystem = SolarSystem()
    # def on_touch_down(self, touch):
    #     color = (random(), random(), random())
    #     newobject = SpaceObject(pos=(touch.x, touch.y))
    #     newobject.draw(self.canvas)
    #     self.spaceobjects.append(newobject)

    def on_touch_down(self, touch):
        touch.grab(self)
        self.radius = 1
    def on_touch_move(self, touch):
        if touch.grab_current is self:
            dxy = 1
            if touch.dx:
                dxy = touch.dx
            else:
                dxy = touch.dy
            self.radius += dxy
            # I received my grabbed touch
        # else:
        # it's a normal touch

    def on_touch_up(self, touch):
        if touch.grab_current is self:
        # I receive my grabbed touch, I must ungrab it!
            newobject = SpaceObject(pos=(touch.x, touch.y), radius = self.radius)
            self.solarsystem.append(newobject)
            touch.ungrab(self)
        else:
        # it's a normal touch
            pass

    def update(self, dt):
        self.solarsystem.update()

    def draw(self, dt):
        for item in self.solarsystem:
            item.draw(self.canvas)

    def start_space(self):
        self.solarsystem.append(SpaceObject(pos=(0, 0)))
        self.solarsystem[0].center = self.center
        self.solarsystem[0].velocity = Vector(4, 0).rotate(randint(0, 360))


class GravityRingApp(App):

    def build(self):
        self.gravity = GravityRing()
        self.gravity.start_space()
        # gravity.update(1)
        Clock.schedule_interval(self.gravity.draw, 1. / 60)
        Clock.schedule_interval(self.gravity.update, 1. / 60)
        return self.gravity

if __name__ == '__main__':
    GravityRingApp().run()

