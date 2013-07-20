from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
class MainCharacter(Widget):
  RUNNING = "images/KatipuneroRunning.zip"
  STAND = "images/KatipuneroStand.png"
  def __init__(self, **kwargs):
    super(MainCharacter, self).__init__(**kwargs)
    self.standing_place = 70

    self.main_char_img = Image(source=MainCharacter.STAND)
    self.main_char_img.pos = (50, self.standing_place)
    self.main_char_img.size = (150, 300)
    self.add_widget(self.main_char_img)

    self.moving = False
    self.jumping = False
    Clock.schedule_interval(self.check_moving, 1/60)

    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self._keyboard.bind(on_key_up=self._on_keyboard_up)

  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard.unbind(on_key_up=self._on_keyboard_up)
    self._keyboard = None

  def on_touch_down(self, touch):
    print "touched"
    return super(MainCharacter, self).on_touch_down(touch)

  def check_moving(self, dt):
    if self.moving:
      self.parent.background.move_all()
    if self.main_char_img.y == self.standing_place:
      self.jumping = False
    else:
      self.jumping = True

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    jump_height = 300
    jump_duration = 0.5
    if keycode[1] == "d":
      self.main_char_img.source = MainCharacter.RUNNING
      self.moving = True
    elif keycode[1] == "w" and not self.jumping:
      anim = Animation(y=jump_height, duration=jump_duration) + Animation(y=self.standing_place, duration=jump_duration)
      anim.start(self.main_char_img)

  def _on_keyboard_up(self, keyboard, keycode):
    if keycode[1] == "d":
      self.main_char_img.source = MainCharacter.STAND
      self.moving = False
