import os
import yaml

import kivy
kivy.require('1.0.9')
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup


from simulation.conf import Config
from simulation.conf.configparser import ConfigParser
from simulation.conf.settings import appsettings
from gui.spacescreen import GravityRing



class LoadDialog(FloatLayout):
    """Dialog for loading configuration"""
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    """Dialog for saving prepared configuration"""
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ConfigScreen(Screen):
    """Screen for settings"""
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    config = Config()
    space_widget = ObjectProperty(None)
    sm = ObjectProperty(None)


    def __init__(self, *args, **kwargs):
        super(ConfigScreen, self).__init__(*args, **kwargs)
        Clock.schedule_interval(self.space_widget.draw, 1./appsettings['calculation_speed'])
        self.space_widget.spacesystem.clear()
        self.space_widget.bind(on_touch_up=self.add_spaceobject)

    def add_spaceobject(self, obj, value):
        # self.space_widget.on_touch_up(touch)
        Logger.debug("TODO: add object to input")
        # if len(self.space_widget.spacesystem) >0:
        #     self.text_input.text = str(yaml.dump(self.space_widget.spacesystem.data))


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
            self.__load_system(self.text_input.text)
        self.dismiss_popup()

    def save(self, path, filename):
        """ save prepared configuration """
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)
        self.dismiss_popup()
    def __load_system(self, text):
        self.config.loadfromstring(text)
        parser = ConfigParser(self.config)
        self.space_widget.spacesystem.clear()
        self.space_widget.spacesystem.system = parser.parse()
        Logger.debug("Len system %s parser %s  "% (len(self.space_widget.spacesystem), len(parser.parse())))
    def __validate(self, value):
        pass

    def ok_pressed(self):
        self.__load_system(self.text_input.text)
        GravityRing.spacesystem = self.space_widget.spacesystem
        self.sm.current = 'gravity'

    def show_praview(self):
        try:
            if self.text_input.text == '':
                Logger.warning("Skiping show praview!")
                return
            self.__validate(self.text_input.text)
            self.__load_system(self.text_input.text)
            Logger.debug("Cofnig %s" % str(self.config.data))
        except Exception as err:
            Logger.warning("Parse error %s " % (err))

    def on_enter(self):
        self.space_widget.spacesystem.clear()
        self.space_widget.draw_label = False
        Clock.schedule_interval(self.space_widget.draw, 1. / appsettings['calculation_speed'])

    def on_leave(self):
        self.space_widget.draw_label = True
        Clock.unschedule(self.space_widget.draw)

