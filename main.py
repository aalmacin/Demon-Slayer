from kivy.app import App
from kivy.uix.widget import Widget
from kivy.atlas import Atlas
from kivy.uix.image import Image
from kivy.factory import Factory

from parallax_bg import ParallaxBG

import kivy

kivy.require("1.0.9")
Factory.register("ParallaxBG", ParallaxBG)
class DemonSlayer(Widget):
  pass

class DemonSlayerApp(App):
  def build(self):
    return DemonSlayer()


if __name__ == "__main__":
  DemonSlayerApp().run()
