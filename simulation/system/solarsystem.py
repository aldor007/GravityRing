"""Module containing main object for simulations"""

import kivy
kivy.require('1.0.9')
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.label import Label
from kivy.utils import get_random_color
from kivy.logger import Logger
import math
import copy
from simulation.numericmethods.rungekutta import RungeKutta
from simulation.numericmethods.euler import Euler
from simulation.numericmethods.verletvelocity import VerletVelocity
from simulation.conf.settings import appsettings
from utils import ListBase



class Force(object):
    """Class containing force value"""


    def __init__(self, spaceobject2, spaceobject1, distancesqured):
        """ Init method for force class

        :param spaceobject2: object in what direction force is facing.
        :param spaceobject1: start object for force.
        :param distancesqured: sqrt from distance^2.
        """
        self.vector = (spaceobject2.x - spaceobject1.x, spaceobject2.y - spaceobject1.y )
        self.startpos = [spaceobject1.x +spaceobject1.radius/4., spaceobject1.y + spaceobject1.radius/4]
        self.endpos = [0, 0]
        self.value = self.calculate(spaceobject1.mass, spaceobject2.mass, distancesqured)
        self.endpos[0] = self.startpos[0] + self.vector[0] / (10 * appsettings['gravity']) * 0.1 * math.fabs(self.value)
        self.endpos[1] = self.startpos[1] + self.vector[1] / (10 * appsettings['gravity']) * 0.1 *  math.fabs(self.value)

    def calculate(self, mass1, mass2, distancesqured):
        """Calculate value of force on object.
        If distance smaller then 1e-4 returns 0

        :param mass1: mass first object.
        :param mass2: mass second object.
        :return: value of force.
        """
        self.value = float(appsettings['gravity']) * float(mass1) * float(mass2) /float(distancesqured) if distancesqured>1e-4 else 0.0
        return self.value

    def draw(self, shift):
        """Method draw force on canvas

        :param shift: shift ftom start point(0,0),
        """
        Color(1, 0, 0)
        Line(points=(self.startpos[0] + shift[0] , self.startpos[1] + shift[1], self.endpos[0] + shift[0], self.endpos[1] + shift[1]), width=1)
            # Line(points=(420,220 ,880, 400), width=1
            # Triangle()
    def __str__(self):
        return " start %s endpod %s value %s " % (self.startpos, self.endpos, self.value)

class SpaceObjectBase(object):
    """Abstraction for SpaceObject"""
    def __init__(self):
        # super(SpaceObjectBase, self).__init__()
        self.pos = [0.0, 0.]
        self.velocity = [0., 0.]
        self.mass_val = None
        self.radius_val = None
        self.name = None

    @property
    def position(self):
        """ Return position list"""
        return self.pos

    @position.setter
    def position(self, value):
        """ set  position list"""
        if type(value) is tuple:
            self.pos = list(value)
        else:
            self.pos = value
    @property
    def x(self):
        # pylint: disable=C0103
        """Return x of postion"""
        return self.pos[0]

    @x.setter
    def x(self, value):
        # pylint: disable=C0103
        """set x of postion"""
        self.pos[0] = value

    @property
    def mass(self):
        """Return object mass"""
        return self.mass_val

    @mass.setter
    def mass(self, value):
        """Set mass and calcutate for it radius"""
        self.mass_val = value
        self.radius_val = (3. * self.mass/(appsettings['density'] *4. * math.pi))**(1./3.)

    @property
    def radius(self):
        """Return radius of object"""
        return self.radius_val

    @radius.setter
    def radius(self, value):
        """Set radius and calcuate mass for radius"""
        self.radius_val = value
        self.mass_val = appsettings['density']*4.*math.pi*(self.radius_val**3.)/3.

    @property
    def y(self):
        """return y of pos"""
        # pylint: disable=C0103
        return self.pos[1]

    @y.setter
    def y(self, value):
        """set y of pos"""
        # pylint: disable=C0103
        self.pos[1] = value

    @property
    def velocity_x(self):
        """return velocity_x"""
        return self.velocity[0]

    @property
    def velocity_y(self):
        """return velocity_y"""
        return self.velocity[1]

    @velocity_x.setter
    def velocity_x(self, value):
        """set velocity_x"""
        self.velocity[0] = value

    @velocity_y.setter
    def velocity_y(self, value):
        """set velocity_y"""
        self.velocity[1] = value

    def __repr__(self):
        return "Space postion=%s velocity=%s mass=%s  radius=%s" % (self.pos, self.velocity, self.mass, self.radius)




class SpaceObject(SpaceObjectBase):
    """Class represetn space object"""

    objectcount = 0
    mergedforces = list()
    def __init__(self, pos, radius=10):
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
        dpcpy = SpaceObject((0, 0))
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
        """ Returns force, distance betwen two objects

        :param other: other spaceobject.
        :returns: value of force, distance.
        """
        distancex = self.x - other.x
        distancey = self.y - other.y
        distancesqured = distancex*distancex + distancey*distancey
        distance = math.sqrt(distancesqured)
        return self.calcutateforces(distancesqured, other), distance

    def cleanup(self):
        """Method for removing forces from merged spaceobjects"""
        forcescopy = copy.deepcopy(self.forces)
        for item in SpaceObject.mergedforces:
            print "merged", item, self.forces
            if item in self.forces.keys():
                try:
                    del forcescopy[item]
                except KeyError:
                    pass
        self.forces = copy.deepcopy(forcescopy)

    def return_label(self):
        """Method genereting label containing useful information
        about postion, velocity, radius, mass"""
        tmp = [0, 0]
        tmp[0] = self.x + self.radius
        tmp[1] = self.y + self.radius
        return Label(pos=tmp, text="Name  %s\n postion=[%2.f, %2.f] velocity=[%2.f, %2.f] radius=%2.f mass=%2.f showlabel=%s" \
                        %(self.name, self.x, self.y, self.velocity_x, self.velocity_y,
                            self.radius, self.mass, self.show_label))

    def draw(self, shift, width, height, zoom):
        """Method draw SpaceObject on canvas"""
        width = width / 2.
        height = height / 2.
        #TODO: work on zoom
        # tmpposx = width + self.x
        # tmpposy = height +self.y
        Color(*self.color)
        Ellipse(pos=(self.x + shift[0], self.y + shift[1]), size=(zoom * self.radius, zoom * self.radius))
        for force in self.forces.values():
            force.draw(shift)

    def merge(self, other):
        """ Method for merging space objece
        when they collide"""
        self.mass_val += other.mass
        self.radius_val = (3. * self.mass/(appsettings['density'] *4. * math.pi))**(1./3.)
        other.merged = True
        try:
            del self.forces[other.spaceid]
        except KeyError:
            pass
        SpaceObject.mergedforces.append(other.spaceid)

    def calcutateforces(self, distancesqured, other):
        """Merhod calculate force affected by others and
        store it in list.

        :param distancesqured: distancesqured between objects.
        :param other: other SpaceObject.
        :return: value of force"""
        self.forces[other.spaceid] = Force(other, self, distancesqured)
        other.forces[self.spaceid] = self.forces[other.spaceid]
        # other.forces[self.spaceid].value *= -1.
        return self.forces[other.spaceid].value


    def collision(self, other):
        """Method for detect collision between object

        :param other: other SpacObjec.
        :returns: True if collision  else  False.
        """
        distancex = self.x + - other.x
        distancey = self.y - other.y
        distance = math.sqrt(distancex**2 + distancey**2)
        return distance <= (self.radius + other.radius)

    def __str__(self):
        reprstr = super(SpaceObject, self).__str__()
        reprstr += ' spaceid = %s' % self.spaceid
        return reprstr
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and  self.radius == self.radius

    def decrease(self):
        """Method decrease count of object"""
        Logger.debug("Odejmowanie")
        SpaceObject.objectcount = SpaceObject.objectcount - 1
        if SpaceObject.objectcount < 0:
            SpaceObject.objectcount = 0

class SolarSystem(ListBase):
    """Class containing list of spaceobjects"""
    # __metaclass__ = Singleton

    def __init__(self):
        """Init method for SolarSystem class
        it define 3 numericmethods"""
        self.system = list()
        self.matmethods = {
                'RungeKutta': RungeKutta(), 'VerletVelocity': VerletVelocity(), 'Euler': Euler()}

    @property
    def data(self):
        """Basic property getter"""
        return self.system

    @data.setter
    def data(self, value):
        """Basic property setter"""
        self.system = value

    def update(self):
        """Method runned periodicly. It refres system list.
        Check collisions between object and whether it is to far
        """
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
            matmethod = self.matmethods[appsettings['numericmethod']]
        except KeyError:
            matmethod = self.matmethods['RungeKutta']
            Logger.warning("Defualt method %s " % appsettings['numericmethod'])

        self.system = matmethod.calculate(self.system, appsettings['dt_in_numericmethod'])
        return self

    def points_in_system(self, posx, posy):
        """Method check if point is in system

        :param posx: x point value.
        :param posy: y point value.
        :returns: True if point is in system else False
        """
        tmp = SpaceObjectBase()
        tmp.x = posx # pylint: disable=C0103
        tmp.y = posy # pylint: disable=C0103
        tmp.radius = 1
        for item in self.system:
            if item.collision(tmp):
                return True
        return False

    def clear(self):
        """Method clear system list"""
        self.system = list()

    def append(self, spaceobject):
        """Metgod for adding spaceobject to list"""
        self.system.append(spaceobject)

    def get_system(self):
        """Metho for getting system list"""
        return self.system

    def __len__(self):
        return len(self.system)


    def __iter__(self):
        return self.system.__iter__()

