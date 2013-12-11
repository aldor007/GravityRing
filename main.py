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
from simulation.conf import Config
from simulation.numericmethods.rungakutta import RungaKutta
from simulation.system.solarsystem import SolarSystem
from simulation.system.solarsystem import SpaceObject
from kivy.core.window import Window


DENSITY = 0.001

# The gravity coefficient - it's my universe, I can pick whatever I want :-)
GRAVITYSTRENGTH = 10000000
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

class Space(Widget):
    solarsystem = SolarSystem()
    def __init__(self, **kwargs):
        super(Space, self).__init__(**kwargs)
        self.width -= self.width/8
        self.height -= self.height/8
        self.start_space()
    def start_space(self):
        Clock.schedule_interval(self.draw, 1. / 30)
        sun = SpaceObject(pos=(420, 220), radius=100)
        # sun.mass = 14
        sun.spaceid = 0
        Space.solarsystem = SolarSystem()
        Space.solarsystem.append(sun)
        spaceob = SpaceObject(pos=(10,30), radius = 5)
        spaceob1 = SpaceObject(pos=(20,60), radius = 5)
        spaceob1.velocity_x = 3.0
        spaceob1.velocity_y = 6.0
        # spaceob.mass = 0.013
        Space.solarsystem.append(spaceob)
        Space.solarsystem.append(spaceob1)
        # Space.solarsystem.append(SpaceObject(pos=(822,201),radius = 3))
        # Space.solarsystem.append(SpaceObject(pos=(822,401),radius = 3))
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
        Space.solarsystem.update()

    def draw(self, dt):
        zoom = 0.5
        self.canvas.clear()
        for item in Space.solarsystem.get_system():
            item.draw(self.canvas, self.width, self.height, zoom)

    def stop_button_pressed(self):
        Clock.unschedule(self.update)
    def start_button_pressed(self):
        Logger.info("START")
        Clock.schedule_interval(self.update, 1./31)

        # self.solarsystem.append(SpaceObject(pos=(0, 0)))
        # self.solarsystem[0].center = self.center
        # self.solarsystem[0].velocity = Vector(4, 0).rotate(randint(0, 360))
    def reset_button_pressed(self):
        self.stop_button_pressed()
        self.canvas.clear()
        Space.solarsystem.clear()
        self.start_space()
class GravityRing(Screen):
    solarsystem = SolarSystem()
    def __init__(self, **kwargs):
        super(GravityRing, self).__init__(**kwargs)

        self.space = Space()
        self.add_widget(self.space)
    # def on_pre_enter(self):
    def stop_button_pressed(self):
        self.space.stop_button_pressed()
    def start_button_pressed(self):
        self.space.start_button_pressed()
    def reset_button_pressed(self):
        self.space.reset_button_pressed()
    
class GravityRingApp(App):

    def build(self):
        from kivy.base import EventLoop
        EventLoop.ensure_window()
        self.window = EventLoop.window
        self.gravity = GravityRing(name='gravity')
        self.sm = ScreenManager()
        self.sm.add_widget(Menu(name='menu'))
        self.sm.add_widget(Settings(name='settings'))
        self.sm.add_widget(self.gravity)
        # gravity.update(1)
        # Clock.schedule_interval(self.gravity.update, 1. / 60)
        Window.bind(on_keyboard=self.hook_keyboard)
        return self.sm

    def hook_keyboard(self, window, key, *largs):
        if key == 27: # BACK
            self.sm.current = self.sm.previous()
        elif key in (282, 319): # SETTINGS
            self.sm.current = 'settings'

if __name__ in ('__main__', '__android__'):
    GravityRingApp().run()

