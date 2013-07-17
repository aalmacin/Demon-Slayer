from kivy.app import App
from kivy.uix.widget import Widget
from kivy.atlas import Atlas
from kivy.uix.image import Image
from kivy.factory import Factory

from parallax_bg import ParallaxBG
from parallax_bg import ParallaxIMG

import kivy

kivy.require("1.0.9")
Factory.register("ParallaxBG", ParallaxBG)
Factory.register("ParallaxIMG", ParallaxIMG)

class DemonSlayer(Widget):
  pass

class DemonSlayerApp(App):
  def build(self):
    from kivy.base import EventLoop
    EventLoop.ensure_window()
    self.window = EventLoop.window
    return DemonSlayer()


if __name__ == "__main__":
  DemonSlayerApp().run()
