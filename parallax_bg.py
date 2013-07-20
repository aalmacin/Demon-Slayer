from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.lang import Builder

Builder.load_file("parallax_bg.kv")
class ParallaxBG(Widget):
  def __init__(self, **kwargs):
    super(ParallaxBG, self).__init__(**kwargs)
    self.move_all()

  def move_all(self):
    for child in self.children:
      child.move_parallax()

class ParallaxIMG(Image):
  def __init__(self, **kwargs):
    super(ParallaxIMG, self).__init__(**kwargs)

  def move_parallax(self):
    if self.x >= -self.width:
      self.x -= self.speed
    else:
      self.x = self.width
      print self.width
