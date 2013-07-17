from kivy.app import App
from kivy.uix.widget import Widget
from kivy.atlas import Atlas
from kivy.uix.image import Image
from kivy.factory import Factory

from parallax_bg import *
from screens import *
from kivy.uix.screenmanager import *

import kivy

kivy.require("1.0.9")
Factory.register("ParallaxBG", ParallaxBG)
Factory.register("ParallaxIMG", ParallaxIMG)
Factory.register("MainScreen", MainScreen)

class DemonSlayer(ScreenManager):
  pass

class DemonSlayerApp(App):
  def build(self):
    from kivy.base import EventLoop
    EventLoop.ensure_window()
    self.window = EventLoop.window
    return DemonSlayer(transition= FadeTransition())


if __name__ == "__main__":
  DemonSlayerApp().run()
