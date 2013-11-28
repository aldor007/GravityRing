import kivy
kivy.require('1.0.9')
from random import random
from kivy.graphics import Color, Ellipse, Line
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.properties import ReferenceListProperty
from kivy.properties import ObjectProperty

import math
import copy
from random import randint
from libs.numericmethods.rungakutta import RungaKutta
GRAVITYSTRENGTH = 1e10
DENSITY = 0.01

GRAVITYSTRENGTH = 1e10
DENSITY = 0.01


class Force(Widget):
    length = 0
    gravitystrength = GRAVITYSTRENGTH

    def calulate(self, mass1, mass2, distance):
        self.value = GRAVITYSTRENGTH * mass1*mass2/distance
        return self.value
    def __init__(self, spaceobject1, spaceobject2,distancesqured, **kwargs):
        super(Widget, self).__init__(**kwargs)
        self.vector = (spaceobject1.x - spaceobject2.x, spaceobject1.y - spaceobject2.y )
        self.value = self.calulate(spaceobject1.mass, spaceobject2.mass, distancesqured)
    def draw(self, canvas, startpos):
        with canvas:
            Line(pos=[self.endpos, startpos], widht=5)




class SpaceObject(object):

    objectcount = -1
    mergedforces = list()
    def __init__(self, pos, radius = 10, **kwargs):
        self.spaceid = SpaceObject.objectcount + 1
        SpaceObject.objectcount += 1
        self.pos = list(pos)
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
        self.merged = False
        # Widget.__init__(self, **kwargs)
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
    def interactions(self, other):
        """ Returns force, distance betwen two objects"""
        distancex = self.x - other.x
        distancey = self.y - other.y
        distancesqured = distancex*distancex + distancey*distancey
        distance = math.sqrt(distancesqured)
        self.calcutateforces(distancesqured, other)
        return self.forces[other.spaceid].value, distance
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
            c = Color(
                    self.color, mode='hsv')
            Ellipse(pos=self.pos, size=(self.radius, self.radius))
    
    def merge(self, other):
        self.mass = other.mass
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
        for item in self.system:
            # tmp = copy.deepcopy(self.system)
            # del tmp[self.system.index(item)]
            for item2 in self.system:
                if item.collision(item2):
                    print item.pos,item2.pos
                    item.merge(item2)
                    items_merged.append(item2.spaceid)
        for todelete in items_merged:
            del self.system[todelete]


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

