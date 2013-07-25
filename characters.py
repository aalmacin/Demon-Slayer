from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
import constants
class CharacterManager(Widget):
  def __init__(self, **kwargs):
    super(CharacterManager, self).__init__(**kwargs)
    mc_sources = {
      Character.STAND: constants.MC_STAND,
      Character.STAND_ATTACK_LEFT: constants.MC_STAND_ATTACK_LEFT,
      Character.STAND_ATTACK_RIGHT: constants.MC_STAND_ATTACK_RIGHT,
      Character.RUNNING_LEFT: constants.MC_RUNNING_LEFT,
      Character.RUNNING_RIGHT: constants.MC_RUNNING_RIGHT,
    }
    self.main_character = MainCharacter(mc_sources)
    self.add_widget(self.main_character)

class Character(Image):
  STAND = "stand"
  STAND_ATTACK_LEFT = "stand attack left"
  STAND_ATTACK_RIGHT = "stand attack right"
  RUNNING_LEFT = "running left"
  RUNNING_RIGHT = "running right"
  def __init__(self, sources, **kwargs):
    super(Character, self).__init__(**kwargs)
    self.sources = sources

    self.source = self.sources[Character.STAND]
    self.size = self.texture_size
    self.y = constants.STANDING_Y

    # Game values
    self.moving = False
    self.attacking = False
    self.jumping = False
    self.to_right = False

    Clock.schedule_interval(self.check_moving, 1/60)
    Clock.schedule_interval(self.check_jumping, 1/60)

  def check_moving(self, dt):
    if self.moving:
      if self.to_right and self.x < (constants.WIDTH - self.width):
        self.x += constants.RUNNING_SPEED
      if not self.to_right and self.x > constants.MIN_X:
        self.x -= constants.RUNNING_SPEED

  def check_jumping(self, dt):
    if self.y == constants.STANDING_Y:
      self.jumping = False
    else:
      self.jumping = True

  def attack(self):
    if self.to_right:
      self.source = self.sources[Character.STAND_ATTACK_RIGHT]
    else:
      self.source = self.sources[Character.STAND_ATTACK_LEFT]
    self.size = self.texture_size

    self.attacking = True
    Clock.schedule_once(self.change_back, 0.2)

  def change_back(self, dt):
    self.attacking = False
    self.source = self.sources[Character.STAND]
    self.size = self.texture_size

class MainCharacter(Character):
  def __init__(self, sources, **kwargs):
    super(MainCharacter, self).__init__(sources, **kwargs)
    self.x = (constants.MC_X)
    self.on_battle = False

    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self._keyboard.bind(on_key_up=self._on_keyboard_up)

  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard.unbind(on_key_up=self._on_keyboard_up)
    self._keyboard = None

  def on_touch_down(self, touch):
    if not self.attacking:
      self.attack()
    return super(Character, self).on_touch_down(touch)

  def check_moving(self, dt):
    if self.moving:
      if self.on_battle:
        super(MainCharacter, self).check_moving(dt)
      else:
        self.parent.parent.background.move_all()

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == "d":
      if not self.attacking:
        self.source = self.sources[Character.RUNNING_RIGHT]
      self.to_right = True
      self.moving = True
    elif keycode[1] == "a":
      if self.on_battle:
        if not self.attacking:
          self.source = self.sources[Character.RUNNING_LEFT]
        self.to_right = False
        self.moving = True
    elif keycode[1] == "w" and not self.jumping:
      if not self.attacking:
        anim = Animation(
          y=constants.JUMP_HEIGHT,
          duration=constants.JUMP_DURATION
        ) + Animation(
          y=constants.STANDING_Y,
          duration=constants.JUMP_DURATION
        )
        anim.start(self)

  def _on_keyboard_up(self, keyboard, keycode):
    if keycode[1] == "d" or keycode[1] == "a" and not self.attacking:
      self.source = self.sources[Character.STAND]
      self.moving = False
