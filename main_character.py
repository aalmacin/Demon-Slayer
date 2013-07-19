from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
class MainCharacter(Widget):
  RUNNING = "images/KatipuneroRunning.zip"
  STAND = "images/KatipuneroStand.png"
  def __init__(self, **kwargs):
    super(MainCharacter, self).__init__(**kwargs)

    self.main_char_img = Image(source=MainCharacter.STAND)
    self.main_char_img.pos = (50, 100)
    self.main_char_img.size = (150, 300)
    self.add_widget(self.main_char_img)

    self.moving = False
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

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == "d":
      self.main_char_img.source = MainCharacter.RUNNING
      self.moving = True

  def _on_keyboard_up(self, keyboard, keycode):
    if keycode[1] == "d":
      self.main_char_img.source = MainCharacter.STAND
      self.moving = False
