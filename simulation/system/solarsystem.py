import kivy
kivy.require('1.0.9')
from random import random
from kivy.graphics import Color, Ellipse, Line
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.properties import ReferenceListProperty
from kivy.properties import ObjectProperty

from kivy.logger import Logger
import math
import copy
from random import randint
from simulation.numericmethods.rungekutta import RungeKutta
from simulation.numericmethods.euler import Euler
from simulation.numericmethods.verletvelocity import VerletVerlocity
from utils import Singleton

GRAVITYSTRENGTH =  14
DENSITY = 0.001



class Force(Widget):
    length = 0
    gravitystrength = GRAVITYSTRENGTH

    def calulate(self, mass1, mass2, distance):
        self.value = GRAVITYSTRENGTH * mass1*mass2/distance if distance>1e-5 else 0.0
        return self.value
    def __init__(self, spaceobject1, spaceobject2,distancesqured, **kwargs):
        super(Widget, self).__init__(**kwargs)
        self.vector = (spaceobject1.x - spaceobject2.x, spaceobject1.y - spaceobject2.y )
        self.value = self.calulate(spaceobject1.mass, spaceobject2.mass, distancesqured)
    def draw(self, canvas, startpos):
        with canvas:
            Line(pos=[self.endpos, startpos], width=5)

class SpaceObjectBase(object):

    def __init__(self):
        self.pos = [0.0, 0.]
        self.velocity = [0., 0.]
        self.acceleration = [0., 0.]
        self.mass = None
        self.radius = None

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, value):
        self.pos[0] = value

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, value):
        self.pos[1] = value

    @property
    def acceleration_x(self):
        return self.acceleration[0]

    @property
    def acceleration_y(self):
        return self.acceleration[1]

    @acceleration_x.setter
    def acceleration_x(self, value):
        self.acceleration[0] = value

    @acceleration_y.setter
    def acceleration_y(self, value):
        self.acceleration[1] = value

    @property
    def velocity_x(self):
        return self.velocity[0]

    @property
    def velocity_y(self):
        return self.velocity[1]

    @velocity_x.setter
    def velocity_x(self, value):
        self.velocity[0] = value

    @velocity_y.setter
    def velocity_y(self, value):
        self.velocity[1] = value

    def __str__(self):
        return "postion=%s velocity=%s mass=%s acceleration=%s radius=%s" %(self.pos, self.velocity,self.mass,self.acceleration, self.radius)



class SpaceObject(SpaceObjectBase):

    objectcount = 0
    mergedforces = list()
    def __init__(self, pos, radius = 10, **kwargs):
        super(SpaceObject, self).__init__()
        self.spaceid = SpaceObject.objectcount
        SpaceObject.objectcount += 1
        self.pos = list(pos)
        self.forces = {}
        self.radius = int(radius)
        self.color = (randint(0, 1), randint(0, 1), randint(0, 1), randint(0,1) )
        self.mass = DENSITY*4.*math.pi*(self.radius**3.)/3.
        # self.mass *= 10
        self.merged = False
        self.velocity = [0., 0.]
    
    def __deepcopy__(self, memo):
        dpcpy = SpaceObject((0,0))
        SpaceObject.objectcount -= 1
        dpcpy.spaceid = self.spaceid
        dpcpy.pos = list(self.pos)
        dpcpy.forces = copy.deepcopy(self.forces)
        dpcpy.color = list(self.color)
        dpcpy.mass = self.mass
        dpcpy.velocity = list(self.velocity)
        dpcpy.radius = int(self.radius)
        dpcpy.merged = self.merged
        memo[id(dpcpy)] = dpcpy
        return dpcpy

    def interactions(self, other):
        """ Returns force, distance betwen two objects"""
        distancex = self.x - other.x
        distancey = self.y - other.y
        distancesqured = distancex*distancex + distancey*distancey
        distance = math.sqrt(distancesqured)
        return self.calcutateforces(distancesqured, other), distance
        # self.__cleanup()
        # distancex = self.x - other.x
        # distancey = self.y - other.y
        # self.calcutateforces( distancex, distancey, other.spaceid)
    def __cleanup(self):
        for item in mergedforces:
            if item in self.forces.keys():
                del self.forces[item]
    def draw(self, canvas, width, height, zoom):
        with canvas:
            Color(
                    self.color)
            width = width / 2.
            height = height / 2.
            tmpposx = width + self.x
            tmpposy = height +self.y 
            Ellipse(pos=( self.x, self.y ), size=(zoom * self.radius,zoom * self.radius))

    
    def merge(self, other):
        self.mass += other.mass
        self.radius = (3. * self.mass/(DENSITY *4. * math.pi))**(1./3.)
        other.merged = True
        try:
            del self.forces[other.spaceid]
        except KeyError:
            pass
        SpaceObject.mergedforces.append(other.spaceid)

    def calcutateforces(self, distancesqured, other):
        # self.forces[other.spaceid] = 
        # distancesqured = distancex*distancex + distancey*distancey
        self.forces[other.spaceid] = Force(other, self, distancesqured)
        return self.forces[other.spaceid].value


    def collision(self, other):
        distancex = self.x - other.x
        distancey = self.y - other.y
        distance = math.sqrt(distancex**2 + distancey**2)
        return distance <= (self.radius + other.radius)
    
    def __str__(self):
        reprstr = super(SpaceObject, self).__str__()
        reprstr += ' spaceid = %s' % self.spaceid
        return reprstr
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and  self.radius == self.radius
class SolarSystem(object):
    # __metaclass__ = Singleton

    def __init__(self, speed = 1):
        self.gravity = GRAVITYSTRENGTH
        self.system = list()
        self.matmethod = VerletVerlocity()
    def update(self):
        items_merged = list()
        tmp = list(self.system)
        for item in self.system:
            for item2 in self.system:
                if item is item2:
                    continue
                else:

                    if item.collision(item2) and item2.spaceid not in items_merged and item.spaceid not in items_merged:
                        Logger.debug("Merge")
                        if item.mass > item2.mass:
                            item.merge(item2)
                            items_merged.append(item2.spaceid)
                            tmp.remove(item2)
                        else:
                            item2.merge(item)
                            items_merged.append(item.spaceid)
                            tmp.remove(item)
                        # if item.spaceid == 0:
                        #     item.merge(item2)
                        #     items_merged.append(item2.spaceid)
                        #     tmp.remove(item2)
                        # elif item2.spaceid == 0:
                        #     item2.merge(item)
                        #     items_merged.append(item.spaceid)
                        #     tmp.remove(item)
                        # else:
                        #     item.merge(item)
                        #     items_merged.append(item2.spaceid)
                        #     tmp.remove(item2)
        self.system = tmp
        self.system = self.matmethod.calculate(self.system)
        return self
    def clear(self):
        self.system = list()

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

