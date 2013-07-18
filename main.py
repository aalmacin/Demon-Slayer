from kivy.app import App
from kivy.uix.widget import Widget
from kivy.atlas import Atlas
from kivy.uix.image import Image
from kivy.factory import Factory

from parallax_bg import *
from screens import *
from kivy.uix.screenmanager import *
from kivy.base import EventLoop

import kivy

kivy.require("1.0.9")
Factory.register("ParallaxBG", ParallaxBG)
Factory.register("ParallaxIMG", ParallaxIMG)
Factory.register("MainScreen", MainScreen)
Factory.register("MainCharacter", MainCharacter)

class DemonSlayer(ScreenManager):
  pass

class DemonSlayerApp(App):
  WIDTH = 1280
  HEIGHT = 700
  def build(self):
    EventLoop.ensure_window()
    self.window = EventLoop.window
    self.window.size = (DemonSlayerApp.WIDTH, DemonSlayerApp.HEIGHT)
    return DemonSlayer(transition= FadeTransition())

if __name__ == "__main__":
  DemonSlayerApp().run()
