from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty

class ParallaxBG(Widget):
  pass

class ParallaxIMG(Image):
  def __init__(self, **kwargs):
    super(ParallaxIMG, self).__init__(**kwargs)

  def move_parallax(self):
    if self.x >= -self.width:
      self.x -= self.speed
    else:
      self.x = self.width
