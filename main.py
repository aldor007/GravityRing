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

from libs.numericmethods.rungakutta import RungaKutta
from libs.system.solarsystem import SolarSystem
from libs.system.solarsystem import SpaceObject

GRAVITYSTRENGTH = 1e10
DENSITY = 0.01



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
        pass
        # self.solarsystem.append(SpaceObject(pos=(0, 0)))
        # self.solarsystem[0].center = self.center
        # self.solarsystem[0].velocity = Vector(4, 0).rotate(randint(0, 360))


class GravityRingApp(App):

    def build(self):
        self.gravity = GravityRing()
        self.gravity.start_space()
        # gravity.update(1)
        Clock.schedule_interval(self.gravity.draw, 1. / 50)
        # Clock.schedule_interval(self.gravity.update, 1. / 60)
        return self.gravity

if __name__ == '__main__':
    GravityRingApp().run()

