#
__version__ = '0.1.1.1'
import math
import copy
import os
import kivy
kivy.require('1.0.9')
from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line,Rectangle
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivy.properties import ReferenceListProperty
from kivy.properties import ObjectProperty
from kivy.vector import Vector
from random import randint
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup


from libs.numericmethods.rungakutta import RungaKutta
from libs.system.solarsystem import SolarSystem
from libs.system.solarsystem import SpaceObject

GRAVITYSTRENGTH = 1e10
DENSITY = 0.01
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Menu(Screen):
    pass
    # def on_enter(self):
    #     self.t = 0.0


    # def update(self, dt):
    #     self.logo.pos = (self.size[0]/2 - 405/2, self.size[1]/2 - 153/2 + 157 + math.sin(self.t * 3) * 10)
    #     self.t += dt
class Settings(Screen):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        self.dismiss_popup()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()

class GravityRing(Screen):
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
        self.gravity = GravityRing(name='gravity')
        self.gravity.start_space()
        Clock.schedule_interval(self.gravity.draw, 1. / 50)
        sm = ScreenManager()
        sm.add_widget(Menu(name='menu'))
        sm.add_widget(Settings(name='settings'))
        sm.add_widget(self.gravity)
        # gravity.update(1)
        # Clock.schedule_interval(self.gravity.update, 1. / 60)
        return sm

if __name__ in ('__main__', '__android__'):
    GravityRingApp().run()

