from kivy.uix.widget import Widget
from kivy.uix.image import Image

class ParallaxBG(Widget):
  def __init__(self, **kwargs):
    super(ParallaxBG, self).__init__(**kwargs)
    self.set_images()

  def set_images(self):
    self.bg = Image(source="images/Background.png")
    self.bg.size = self.bg.texture_size
    self.add_widget(self.bg)

    cloud_speed = 5
    barrio_speed = 10
    ground_speed = 20

    self.cloud_1 = self.left_img(cloud_speed, "images/Clouds_01.png")
    self.cloud_2 = self.right_img("images/Clouds_02.png", self.cloud_1)

    self.barrio_1 = self.left_img(barrio_speed, "images/Barrio_01.png", pos=(0, 140))
    self.barrio_2 = self.right_img("images/Barrio_02.png", self.barrio_1, y=140)

    self.ground_1 = self.left_img(ground_speed, "images/Ground_01.png")
    self.ground_2 = self.right_img("images/Ground_02.png", self.ground_1)

  def left_img(self, speed, img_source, pos=(0,0)):
    obj = ParallaxIMG(speed, source=img_source)
    obj.size = obj.texture_size
    obj.pos = pos
    self.add_widget(obj)
    return obj

  def right_img(self, img_source, left_img, y=0):
    obj = ParallaxIMG(left_img.speed, source=img_source)
    obj.size = obj.texture_size
    obj.pos = (left_img.x + left_img.width, y)
    self.add_widget(obj)
    return obj

  def move_all(self):
    self.move(self.cloud_1, self.cloud_2)
    self.move(self.barrio_1, self.barrio_2)
    self.move(self.ground_1, self.ground_2)

  def move(self, obj1, obj2):
    if obj1.x >= -obj1.width:
      obj1.x -= obj1.speed
    else:
      obj1.x = obj2.x + obj2.width - obj2.speed

    if obj2.x >= -obj2.width:
      obj2.x -= obj2.speed
    else:
      obj2.x = obj1.x + obj1.width - obj1.speed

class ParallaxIMG(Image):
  def __init__(self, speed, **kwargs):
    super(ParallaxIMG, self).__init__(**kwargs)
    self.speed = speed
    self.anchor = (0, 0)
