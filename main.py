"""Main module of app"""
#
__version__ = '0.1.2'
import math
import os
import kivy
kivy.require('1.0.9')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen


from gui.configscreen import ConfigScreen
from gui.spacescreen import GravityRing

class Menu(Screen):
    pass


class GravityRingApp(App):
    """Aplication class"""
    sm = ScreenManager()
    def build(self):
        """build application"""
        from kivy.base import EventLoop
        EventLoop.ensure_window()
        self.window = EventLoop.window
        self.gravity = GravityRing(name='gravity')
        self.sm.add_widget(Menu(name='menu'))
        self.sm.add_widget(self.gravity)
        self.sm.add_widget(ConfigScreen(name='configscreen', sm=self.sm))
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

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'gravity', '40')
        config.setdefault('General', 'density', '100')
        config.setdefault('General', 'FirstStartup', 'Yes')

if __name__ in ('__main__', '__android__'):
    GravityRingApp().run()
