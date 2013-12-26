import kivy
kivy.require('1.0.9')
from random import random
from kivy.graphics import Color, Ellipse, Line
from kivy.core.image import Image
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.properties import ReferenceListProperty
from kivy.properties import ObjectProperty
from kivy.utils import get_random_color
from kivy.logger import Logger
import math
import copy
from random import randint
from simulation.numericmethods.rungekutta import RungeKutta
from simulation.numericmethods.euler import Euler
from simulation.numericmethods.verletvelocity import VerletVerlocity
from utils import Singleton
from simulation.conf.settings import appsettings



class Force(object):
    """Class containg force value"""


    def __init__(self, spaceobject2, spaceobject1, distancesqured):
        self.vector = (spaceobject2.x - spaceobject1.x, spaceobject2.y - spaceobject1.y )
        self.startpos = [spaceobject1.x +spaceobject1.radius/4., spaceobject1.y + spaceobject1.radius/4]
        self.endpos = [0, 0]
        self.value = self.calculate(spaceobject1.mass, spaceobject2.mass, distancesqured)
        self.endpos[0] = self.startpos[0] + self.vector[0]/ (10 * appsettings['gravity']) * 0.1 * math.fabs(self.value)
        self.endpos[1] = self.startpos[1] + self.vector[1]/ (10 * appsettings['gravity']) * 0.1 *  math.fabs(self.value)

    def calculate(self, mass1, mass2, distance):
        """Calculate value of force on object"""
        self.value = float(appsettings['gravity']) * float(mass1)*float(mass2)/float(distance) if distance>1e-5 else 0.0
        return self.value

    def draw(self, canvas, shift, radius):
        Color(1,1,0)
        Line(points=(self.startpos[0] + shift[0] , self.startpos[1] + shift[1], self.endpos[0] + shift[0], self.endpos[1] + shift[1]), width=1)
            # Line(points=(420,220 ,880, 400), width=1
            # Triangle()
    def __str__(self):
        return " start %s endpod %s value %s " % (self.startpos, self.endpos, self.value)
class SpaceObjectBase(Widget):

    def __init__(self):
        super(SpaceObjectBase, self).__init__()
        self.pos = [0.0, 0.]
        self.velocity = [0., 0.]
        self.mass_val = None
        self.radius_val = None
        self.name = None
    @property
    def position(self):
        return self.pos

    @position.setter
    def position(self, value):
        if type(value) is tuple:
            self.pos = list(value)
        else:
            self.pos = value
    # @property
    # def x(self):
    #     return self.pos[0]

    # @x.setter
    # def x(self, value):
    #     self.pos[0] = value

    @property
    def mass(self):
        return self.mass_val
    @mass.setter
    def mass(self, value):
        self.mass_val = value
        self.radius_val= (3. * self.mass/(appsettings['density'] *4. * math.pi))**(1./3.)

    @property
    def radius(self):
        return self.radius_val

    @radius.setter
    def radius(self, value):
        self.radius_val = value
        self.mass_val = appsettings['density']*4.*math.pi*(self.radius_val**3.)/3.
    # @property
    # def y(self):
    #     return self.pos[1]

    # @y.setter
    # def y(self, value):
    #     self.pos[1] = value

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

    # def __repr__(self):
    #     return "Space postion=%s velocity=%s mass=%s  radius=%s" %(self.pos, self.velocity,self.mass, self.radius)




class SpaceObject(SpaceObjectBase):

    objectcount = 0
    mergedforces = list()
    def __init__(self, pos, radius=10, **kwargs):
        super(SpaceObject, self).__init__()
        self.spaceid = SpaceObject.objectcount
        SpaceObject.objectcount += 1
        self.pos = list(pos)
        self.forces = {}
        self.radius = int(radius)
        self.color = get_random_color()
        self.mass = appsettings['density']*4.*math.pi*(self.radius**3.)/3.
        # self.mass *= 10
        self.merged = False
        self.velocity = [0., 0.]
        self.name = 'spaceobject_' + str(self.spaceid)
        self.show_label = False
        self.label = None

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
        dpcpy.show_label = self.show_label
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
    def cleanup(self):
        forcescopy = copy.deepcopy(self.forces)
        for item in SpaceObject.mergedforces:
            print "merged", item, self.forces
            if item in self.forces.keys():
                try:
                    del forcescopy[item]
                except KeyError:
                    pass
        self.forces = copy.deepcopy(forcescopy)

    def return_label(self ):
        # self.canvas.clear()
        # if self.show_label:
        tmp = [0, 0]
        tmp[0] = self.x + self.radius
        tmp[1] = self.y + self.radius
        return Label(pos=tmp, text="Name  %s\n postion=[%2.f, %2.f] velocity=[%2.f, %2.f] radius=%2.f mass=%2.f showlabel=%s" \
                        %(self.name, self.x, self.y, self.velocity_x, self.velocity_y,
                            self.radius, self.mass, self.show_label))

            # self.add_widget(self.label)
    def draw(self, canvas, shift, width, height, zoom):
        # self.__cleanup()

        width = width / 2.
        height = height / 2.
        tmpposx = width + self.x
        tmpposy = height +self.y
        Color(*self.color)
        ellipse = Ellipse(pos=(self.x + shift[0], self.y + shift[1]), size=(zoom * self.radius, zoom * self.radius))
        for force in self.forces.values():
            # if force.value > 1e-5: 
            force.draw(canvas, shift, self.radius)
        
    def merge(self, other):
        self.mass_val += other.mass
        self.radius_val = (3. * self.mass/(appsettings['density'] *4. * math.pi))**(1./3.)
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
        other.forces[self.spaceid] = self.forces[other.spaceid]
        # other.forces[self.spaceid].value *= -1.
        return self.forces[other.spaceid].value


    def collision(self, other):
        distancex = self.x - other.x
        distancey = self.y - other.y
        distance = math.sqrt(distancex**2 + distancey**2)
        return distance <= (self.radius + other.radius)

    # def __str__(self):
    #     reprstr = super(SpaceObject, self).__str__()
    #     reprstr += ' spaceid = %s' % self.spaceid
    #     return reprstr
    # def __eq__(self, other):
    #     return self.x == other.x and self.y == other.y and  self.radius == self.radius

    def decrease(self):
        Logger.debug("Odejmowanie")
        SpaceObject.objectcount = SpaceObject.objectcount - 1
        if SpaceObject.objectcount < 0:
            SpaceObject.objectcount = 0
class SolarSystem(object):
    # __metaclass__ = Singleton

    def __init__(self, speed = 1):
        self.system = list()
        self.matmethods = { 'RungeKutta': RungeKutta(), 'VerletVerlocity': VerletVerlocity(), 'Euler': Euler()} 
        VerletVerlocity()
    @property
    def gravity(self):
        return self.gravity_val

    @gravity.setter
    def gravity(self, value):
        appsettings['gravity'] = float(value)

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
                        if math.fabs(item.x) > 3000 or math.fabs(item.y) > 3000:
                            items_merged.append(item.spaceid)
                            tmp.remove(item)
                        item.cleanup()
        self.system = tmp
        SpaceObject.mergedforces = list()
        try:
            matmethod = self.matmethods[appsettings['numericmethods']]
        except KeyError:
            matmethod = self.matmethods['RungeKutta']

        self.system = matmethod.calculate(self.system, appsettings['dt_in_numericmethod'])
        return self
    def points_in_system(self, x, y):
        tmp = SpaceObjectBase()
        tmp.x = x
        tmp.y = y
        tmp.radius = 1
        for item in self.system:
            if item.collision(tmp):
                return True
        return False
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

