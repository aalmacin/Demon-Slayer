from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import NumericProperty

class ParallaxBG(Widget):
  pass

class ParallaxIMG(Image):
  def __init__(self, **kwargs):
    super(ParallaxIMG, self).__init__(**kwargs)
    Clock.schedule_interval(self.printer, 0.1)

  def printer(self, dt):
    if self.x >= -self.width:
      self.x -= self.speed
    else:
      self.x = self.width
