import kivy
kivy.require("1.0.9")

from kivy.config import Config
Config.set('graphics','resizable',0)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.atlas import Atlas
from kivy.uix.image import Image
from kivy.factory import Factory

from parallax_bg import *
from screens import *
from kivy.uix.screenmanager import *
from kivy.base import EventLoop
import constants

Factory.register("ParallaxBG", ParallaxBG)
Factory.register("ParallaxIMG", ParallaxIMG)
Factory.register("MainScreen", MainScreen)
Factory.register("MainCharacter", MainCharacter)

class DemonSlayer(ScreenManager):
  pass

class DemonSlayerApp(App):
  def build(self):
    EventLoop.ensure_window()
    self.window = EventLoop.window
    self.window.size = (constants.WIDTH, constants.HEIGHT)
    return DemonSlayer(transition= FadeTransition())

if __name__ == "__main__":
  DemonSlayerApp().run()
