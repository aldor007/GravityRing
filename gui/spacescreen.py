"""Modul containg screens for showing simulation"""
import math

import kivy
kivy.require('1.0.9')
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.graphics import Color

from simulation.system.spacesystem import SpaceSystem
from simulation.system.spacesystem import SpaceObject
from simulation.conf.settings import appsettings

class ComboEdit(TextInput):
    """Kivy version of ComboBox"""
    options = ListProperty(('', ))

    def __init__(self, **kw):
        ddn = self.drop_down = DropDown()
        ddn.bind(on_select=self.on_select)
        super(ComboEdit, self).__init__(**kw)
        self.font_size = 15
        self.height = 88

    def on_options(self, instance, value):
        """Run when click on button"""
        ddn = self.drop_down
        ddn.clear_widgets()
        for widg in value:
            widg.bind(on_release=lambda btn: ddn.select(btn.text))
            ddn.add_widget(widg)

    def on_select(self, *args):
        """save change to TextInput"""
        self.text = args[1]


    def on_touch_up(self, touch):
        if touch.grab_current == self:
            self.drop_down.open(self)
        return super(ComboEdit, self).on_touch_up(touch)

class SettingDialog(BoxLayout):
    """ Popup dialog containg propery for
    simulation
    """
    speed_slider = ObjectProperty(None)
    gravity_slider = ObjectProperty(None)
    density_slider = ObjectProperty(None)
    gravity_label = ObjectProperty(None)
    speed_label = ObjectProperty(None)
    zoom_label = ObjectProperty(None)
    numeric_label = ObjectProperty(None)
    zoom_label = ObjectProperty(None)
    root = ObjectProperty(None)
    numeric_combo = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SettingDialog, self).__init__(**kwargs)
        self.gravity_label.text = str(appsettings['gravity'])
        self.speed_label.text = str(appsettings['calculation_speed'])
        self.density_label.text = str(appsettings['density'])
        self.numeric_label.text = str(appsettings['numericmethod'])
        self.numeric_combo.text = str(appsettings['numericmethod'])
        # self.zoom_label.text = str(appsettings['zoom'])
        self.gravity_slider.bind(value=self.update_grvity)
        self.density_slider.bind(value=self.update_density)
        self.speed_slider.bind(value=self.update_speed)
        # self.zoom_slider.bind(value=self.update_zoom)
        self.numeric_combo.bind(text=self.update_numeric)
        #TODO: zoom

    def update_grvity(self, instance, value):
        """change gravity value """
        appsettings['gravity'] = value
        self.gravity_label.text = str(value)

    def update_numeric(self, instance, value):
        """change numeric method """
        appsettings['numericmethod'] = str(value)
        self.numeric_label.text = str(value)

    # def update_zoom(self, instance, value):
    #     appsettings['zoom'] = value
    #     self.zoom_label.text = str(value)
    def update_density(self, instance, value):
        """change density value"""
        appsettings['density'] = value
        self.density_label.text = str(value)

    def update_speed(self, instance, value):
        """ change speed of calculations and drawing"""
        appsettings['calculation_speed'] = value
        self.speed_label.text = str(value)

    def dismiss_parent(self):
        """close popup"""
        self.root.setting_popup.dismiss()

class Space(Widget):
    """ Main widget for simulation"""
    drawvelocity = False
    draw_label = True
    start_points = None

    def __init__(self, **kwargs):
        super(Space, self).__init__(**kwargs)
        self.spacesystem = SpaceSystem()
    def start_space(self):
        """start simulation of object"""
        pass
        # sun = SpaceObject(pos=(420, 220), radius=100)
        # sun.mass = 14
        # sun.spaceid = 0
        # Space.spacesystem = SpacSystem()
       # self..spacesystem.append(sun)
       #  spaceob = SpaceObject(pos=(10,30), radius = 5)
       #  spaceob1 = SpaceObject(pos=(20,60), radius = 5)
       #  spaceob1.velocity_x = 3.0
       #  spaceob1.velocity_y = 6.0
       #  # spaceob.mass = 0.013
       #  Space.spacesystem.append(spaceob)
       #  Space.spacesystem.append(spaceob1)
        # Space.spacesystem.append(SpaceObject(pos=(822,201),radius = 3))
        # Space.spacesystem.append(SpaceObject(pos=(822,401),radius = 3))

    def on_touch_down(self, touch):
        """method triggered on touch event"""
        if self.collide_point(*touch.pos):
            touch.grab(self)
            Logger.info("Touch %s  %s %s" % (self.pos, self.width, self.height))
            self.move = [0, 0]
            if self.drawvelocity:
                if self.spacesystem.points_in_system(*touch.pos):
                    self.start_points = touch.pos
            return True
        return False
    def on_touch_move(self, touch):
        """method triggered on touch move event"""
        if self.collide_point(*touch.pos):
            if touch.grab_current is self:
                self.move[0] += touch.dx
                self.move[1] += touch.dy
                if self.drawvelocity and self.start_points is not None:
                    try:
                        self.canvas.after.clear()
                        with self.canvas.after:
                            Color(0, 1, 0)
                            Line(points=(self.start_points[0], self.start_points[1], touch.x, touch.y))
                    except KeyError:
                        pass
                return True
            else:
                pass
        return False
    def on_touch_up(self, touch):
        """method triggered on touch up event"""
        if self.collide_point(*touch.pos):
            if touch.grab_current is self:
            # I receive my grabbed touch, I must ungrab it!
                newobject = SpaceObject(pos=(touch.x - self.pos[0], touch.y - self.pos[1]), radius = 2)
                for spaceobject in self.spacesystem.get_system():
                    if newobject.collision(spaceobject):
                        spaceobject.show_label = not spaceobject.show_label
                        spaceobject.decrease()
                        Logger.debug("Draw label %s" % spaceobject.show_label)
                        touch.ungrab(self)
                        return True
                if not self.drawvelocity:
                    radius = math.sqrt(self.move[0]**2 + self.move[1]**2)
                    newobject.radius = radius
                    newobject.x -= radius/2
                    newobject.y -= radius/2
                    if radius > 0:
                        self.spacesystem.append(newobject)
                else:
                    newobject.radius = math.sqrt(self.move[0]**2 + self.move[1]**2)
                    for spaceobject in self.spacesystem.get_system():
                        if newobject.collision(spaceobject):
                            spaceobject.velocity_x = (touch.x - spaceobject.x) / appsettings['calculation_speed']
                            spaceobject.velocity_y = (touch.y - spaceobject.y) / appsettings['calculation_speed']
                            spaceobject.decrease()
                        Logger.debug("Draw velocity %s %s %s " %(str(spaceobject), touch.x, touch.y))
                    self.canvas.after.clear()
                    self.start_points = None
                touch.ungrab(self)
            else:
            # it's a normal touch
                pass
            return True

    def update(self, dt):
        """Main method for updating """
        self.spacesystem.update()
    def draw(self, dt):
        """method for drawing new system """
        zoom = appsettings['zoom']
        self.canvas.clear()
        with self.canvas:
            for item in self.spacesystem.get_system():
                item.draw(self.pos, self.width, self.height, zoom)
        if self.draw_label:
            for item in self.spacesystem.get_system():
                if item.show_label:
                    self.add_widget(item.return_label())
    def stop_button_pressed(self):
        """Stop updating system """
        Clock.unschedule(self.update)


    def start_button_pressed(self):
        """Start updating system """
        Logger.info("START")
        Clock.schedule_interval(self.update, 1./(appsettings['calculation_speed']-4))

        # self.spacesystem.append(SpaceObject(pos=(0, 0)))
        # self.spacesystem[0].center = self.center
        # self.spacesystem[0].velocity = Vector(4, 0).rotate(randint(0, 360))
    def stop_updating_system(self):
        Clock.unschedule(self.draw)
        Clock.unschedule(self.update)

    def reset_button_pressed(self):
        """Reset space widget """
        self.stop_button_pressed()
        self.canvas.clear()
        self.spacesystem.clear()
        # self.start_space()
    def drawvelocity_button_pressed(self):
        Space.drawvelocity = not Space.drawvelocity
        Logger.debug("Draw ve %s" % Space.drawvelocity)
        if Space.drawvelocity:
            Clock.unschedule(self.update)
            Clock.unschedule(self.draw)
        else:
            Clock.schedule_interval(self.draw, 1./appsettings['calculation_speed'])
            # Clock.schedule_interval(self.update, 1./(appsettings['calculation_speed']+4))
            self.canvas.clear()
            self.canvas.after.clear()
Factory.register('Space', Space)


class GravityRing(Screen):
    """Main screen application class"""

    spacesystem = SpaceSystem()
    spacewidget = ObjectProperty(None)

    start_btn = ObjectProperty()
    stop_btn = ObjectProperty()
    velocity_btn = ObjectProperty()
    def __init__(self, **kwargs):
        super(GravityRing, self).__init__(**kwargs)

        self.spacewidget = Space(id="spacewidget")
        self.spacewidget.width = self.width - self.width/8.
        self.spacewidget.height = 55
        self.setting_popup = None
        self.add_widget(self.spacewidget, 500)

    def on_enter(self):
        if len(GravityRing.spacesystem) > 0:
            self.spacewidget.spacesystem = GravityRing.spacesystem
        Clock.schedule_interval(self.spacewidget.draw, 1. / appsettings['calculation_speed'])

    def on_leave(self):
        self.spacewidget.stop_updating_system()

    def stop_button_pressed(self):
        """Pass stop button pressed"""
        self.spacewidget.stop_button_pressed()
        self.start_btn.state = 'normal'
        self.velocity_btn.state = 'normal'
    def start_button_pressed(self):
        """Pass start button pressed"""
        if self.spacewidget.drawvelocity:
            self.drawvelocity_button_pressed()
            self.velocity_btn.state = 'normal'
        self.spacewidget.start_button_pressed()
        self.stop_btn.state = 'normal'
        self.start_btn.state = 'down'
    def reset_button_pressed(self):
        """Pass reset  button pressed"""
        self.spacewidget.reset_button_pressed()
        self.stop_btn.state = 'down'
        self.start_btn.state = 'normal'

    def drawvelocity_button_pressed(self):
        """Pass reset  button pressed"""
        self.start_btn.state = 'normal'
        self.spacewidget.drawvelocity_button_pressed()
        self.stop_btn.state = 'down'
    def settings_button_pressed(self):
        if self.setting_popup is None:
            self.setting_popup = Popup(attach_to=self,
                                       title='GravityRing Settings',
                                       size_hint=(0.9, 0.8))
            self.setting_dialog = SettingDialog(root=self)
            self.setting_popup.content = self.setting_dialog
        self.spacewidget.stop_button_pressed()
        self.setting_popup.open()
