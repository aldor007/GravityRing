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
from simulation.conf.configparser import ConfigParser
from simulation.system.solarsystem import SolarSystem
from simulation.system.solarsystem import SpaceObject
from kivy.core.window import Window
from kivy.factory import Factory




class LoadDialog(FloatLayout):
    """Dialog for loading configuration"""
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    """Dialog for saving prepared configuration"""
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Menu(Screen):
    """Menu screen"""
    pass
    # def on_enter(self):
    #     self.t = 0.0


    # def update(self, dt):
    #     self.logo.pos = (self.size[0]/2 - 405/2, self.size[1]/2 - 153/2 + 157 + math.sin(self.t * 3) * 10)
    #     self.t += dt
class Settings(Screen):
    """Screen for settings"""
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        """Close popups"""
        self._popup.dismiss()

    def show_load(self):
        """show loading dialog"""
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        """show dialog for saving file"""
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        """load configuration file"""
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()
            config = Config().loadfromstring(self.text_input.text)
            parser = ConfigParser(config)
            parser.parse()
            Space.solarsystem.system = parser.system()
        self.dismiss_popup()

    def save(self, path, filename):
        """ save prepared configuration """
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)
        self.dismiss_popup()

class Space(Widget):
    """ Main widget for simulation"""
    solarsystem = SolarSystem()
    config = Config()

    def start_space(self):
        """start simulation of object"""
        Clock.schedule_interval(self.draw, 1. / 3)
        sun = SpaceObject(pos=(420, 220), radius=100)
        # sun.mass = 14
        sun.spaceid = 0
        # Space.solarsystem = SolarSystem()
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
        """method triggered on touch event"""
        if self.collide_point(*touch.pos):
            touch.grab(self)
            Logger.info("Touch %s %s" % (self.width, self.height))
            self.radius = 1
            return True
        return False
    def on_touch_move(self, touch):
        """method triggered on touch move event"""
        if self.collide_point(*touch.pos):
            if touch.grab_current is self:
                dxy = 1
                if touch.dx:
                    dxy = touch.dx
                else:
                    dxy = touch.dy
                self.radius += dxy
                Logger.info("AAATouchi3 %s %s" % (self.width, self.height))
                return True
            else:
                pass
        return False
    def on_touch_up(self, touch):
        """method triggered on touch up event"""
        if self.collide_point(*touch.pos):
            if touch.grab_current is self:
                Logger.info("Touchi3 %s %s" % (self.width, self.height))
            # I receive my grabbed touch, I must ungrab it!
                newobject = SpaceObject(pos=(touch.x, touch.y), radius = self.radius)
                Space.solarsystem.append(newobject)
                touch.ungrab(self)
            else:
            # it's a normal touch
                pass
            return True

    def update(self, dt):
        """Main method for updating """
        Space.solarsystem.update()

    def draw(self, dt):
        """method for drawing new system """
        zoom = 0.5
        self.canvas.clear()
        with self.canvas:
            for item in Space.solarsystem.get_system():
                Logger.debug(" system %s " % str(item))
                item.draw(self.canvas, self.width, self.height, zoom)

    def stop_button_pressed(self):
        """Stop updating system """
        Clock.unschedule(self.update)

    def start_button_pressed(self):
        """Start updating system """
        Logger.info("START")
        Clock.schedule_interval(self.update, 1./3)

        # self.solarsystem.append(SpaceObject(pos=(0, 0)))
        # self.solarsystem[0].center = self.center
        # self.solarsystem[0].velocity = Vector(4, 0).rotate(randint(0, 360))
    def reset_button_pressed(self):
        """Reset space widget """
        self.stop_button_pressed()
        self.canvas.clear()
        Space.solarsystem.clear()
        self.start_space()

Factory.register('Space', Space)


class GravityRing(Screen):
    """Main screen application class"""

    solarsystem = SolarSystem()
    spacewidget = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GravityRing, self).__init__(**kwargs)

        self.spacewidget = Space(id="spacewidget")
        self.spacewidget.width = self.width - self.width/8.
        self.spacewidget.height = 55
        Clock.schedule_interval(self.spacewidget.draw, 1. / 30)
        self.add_widget(self.spacewidget, 500)
    # def on_pre_enter(self):
    # def __getattribute__(self, name):
    #     """Proxy method for passing calls"""
    #     return getattr(self.spacewidget, name)

    def stop_button_pressed(self):
        """Pass stop button pressed"""
        self.spacewidget.stop_button_pressed()

    def start_button_pressed(self):
        """Pass start button pressed"""
        self.spacewidget.start_button_pressed()

    def reset_button_pressed(self):
        """Pass reset  button pressed"""
        self.spacewidget.reset_button_pressed()

class GravityRingApp(App):
    """Aplication class"""

    def build(self):
        """build application"""
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
        """method for bindings keys"""
        if key == 27: # BACK
            self.sm.current = self.sm.previous()
        elif key in (282, 319): # SETTINGS
            self.sm.current = 'settings'

if __name__ in ('__main__', '__android__'):
    GravityRingApp().run()
