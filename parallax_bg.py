from kivy.uix.widget import Widget
from kivy.uix.image import Image
import constants

#adding paralax to the background to add depth to background
class ParallaxBG(Widget):
  def __init__(self, **kwargs):
    super(ParallaxBG, self).__init__(**kwargs)
    self.set_images()
    
  #set images for background and add it as a widget
  def set_images(self):
    self.bg = Image(source=constants.NIGHT_BG)
    self.bg.size = self.bg.texture_size
    self.add_widget(self.bg)

    self.cloud_1 = self.left_img(constants.CLOUD_SPEED, constants.CLOUD_LEFT_BG)
    self.cloud_2 = self.right_img(constants.CLOUD_RIGHT_BG, self.cloud_1)

    self.barrio_1 = self.left_img(constants.BARRIO_SPEED, constants.BARRIO_LEFT_BG)
    self.barrio_2 = self.right_img(constants.BARRIO_RIGHT_BG, self.barrio_1)

    self.ground_1 = self.left_img(constants.GROUND_SPEED, constants.GROUND_LEFT_BG)
    self.ground_2 = self.right_img(constants.GROUND_RIGHT_BG, self.ground_1)
    
  #left paralax image
  def left_img(self, speed, img_source):
    initial_pos = (0,0)
    obj = ParallaxIMG(speed, initial_pos, pos=initial_pos, source=img_source)
    obj.size = obj.texture_size
    self.add_widget(obj)
    return obj

  #right paralax image
  def right_img(self, img_source, left_img):
    initial_pos = (left_img.x + left_img.width, left_img.y)
    obj = ParallaxIMG(left_img.speed, initial_pos, pos=initial_pos, source=img_source)
    obj.size = obj.texture_size
    self.add_widget(obj)
    return obj

  #move all images
  def move_all(self):
    self.move(self.cloud_1, self.cloud_2)
    self.move(self.barrio_1, self.barrio_2)
    self.move(self.ground_1, self.ground_2)
    
  #move the object based on where they are in the screen
  def move(self, obj1, obj2):
    if obj1.x >= -obj1.width:
      obj1.x -= obj1.speed
    else:
      obj1.x = obj2.x + obj2.width - obj2.speed

    if obj2.x >= -obj2.width:
      obj2.x -= obj2.speed
    else:
      obj2.x = obj1.x + obj1.width - obj1.speed
      
  #reset images
  def reset(self):
    self.cloud_1.reset()
    self.cloud_2.reset()
    self.barrio_1.reset()
    self.barrio_2.reset()
    self.ground_1.reset()
    self.ground_2.reset()
    
#create a paralax image
class ParallaxIMG(Image):
  def __init__(self, speed, initial_pos, **kwargs):
    super(ParallaxIMG, self).__init__(**kwargs)
    self.initial_pos = initial_pos
    self.speed = speed
    
  #reset image to initial position
  def reset(self):
    self.pos = self.initial_pos
