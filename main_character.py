from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
import constants
class MainCharacter(Widget):
  RUNNING_LEFT = "images/KatipuneroRunningLeft.zip"
  RUNNING_RIGHT = "images/KatipuneroRunningRight.zip"
  STAND = "images/KatipuneroStand.png"
  STAND_ATTACK_RIGHT = "images/KatipuneroStandAttackRight.png"
  STAND_ATTACK_LEFT = "images/KatipuneroStandAttackLeft.png"
  def __init__(self, **kwargs):
    super(MainCharacter, self).__init__(**kwargs)
    self.standing_place = 70
    self.running_speed = 10

    self.main_char_img = Image(source=MainCharacter.STAND)
    self.main_char_img.pos = (50, self.standing_place)
    self.main_char_img.size = self.main_char_img.texture_size
    self.add_widget(self.main_char_img)

    self.old_source = self.main_char_img.source

    self.moving = False
    self.attacking = False
    self.jumping = False
    self.on_battle = False
    self.to_right = False
    Clock.schedule_interval(self.check_moving, 1/60)

    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self._keyboard.bind(on_key_up=self._on_keyboard_up)

  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard.unbind(on_key_up=self._on_keyboard_up)
    self._keyboard = None

  def on_touch_down(self, touch):
    self.old_source = self.main_char_img.source
    self.attack()
    return super(MainCharacter, self).on_touch_down(touch)

  def check_moving(self, dt):
    if self.moving:
      if self.on_battle:
        if self.to_right and self.main_char_img.x < (constants.WIDTH - self.main_char_img.width):
          self.main_char_img.x += self.running_speed
        if not self.to_right and self.main_char_img.x > 2:
          self.main_char_img.x -= self.running_speed
      else:
        self.parent.background.move_all()
    if self.main_char_img.y == self.standing_place:
      self.jumping = False
    else:
      self.jumping = True

  def attack(self):
    if self.to_right:
      self.main_char_img.source = MainCharacter.STAND_ATTACK_RIGHT
    else:
      self.main_char_img.source = MainCharacter.STAND_ATTACK_LEFT
    self.main_char_img.size = self.main_char_img.texture_size

    self.attacking = True
    Clock.schedule_once(self.change_back, 0.2)

  def change_back(self, dt):
    self.attacking = False
    self.main_char_img.source = self.old_source
    self.main_char_img.size = self.main_char_img.texture_size

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    jump_height = 300
    jump_duration = 0.5
    if keycode[1] == "d":
      if not self.attacking:
        self.main_char_img.source = MainCharacter.RUNNING_RIGHT
      self.to_right = True
      self.moving = True
    elif keycode[1] == "a":
      if not self.attacking:
        self.main_char_img.source = MainCharacter.RUNNING_LEFT
      self.to_right = False
      self.moving = True
    elif keycode[1] == "w" and not self.jumping:
      if not self.attacking:
        anim = Animation(y=jump_height, duration=jump_duration) + Animation(y=self.standing_place, duration=jump_duration)
        anim.start(self.main_char_img)

  def _on_keyboard_up(self, keyboard, keycode):
    if keycode[1] == "d" or keycode[1] == "a" and not self.attacking:
      self.main_char_img.source = MainCharacter.STAND
      self.moving = False
