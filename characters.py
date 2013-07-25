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
      Character.STAND_RIGHT: constants.MC_STAND_RIGHT,
      Character.STAND_LEFT: constants.MC_STAND_LEFT,
      Character.STAND_ATTACK_LEFT: constants.MC_STAND_ATTACK_LEFT,
      Character.STAND_ATTACK_RIGHT: constants.MC_STAND_ATTACK_RIGHT,
      Character.RUNNING_LEFT: constants.MC_RUNNING_LEFT,
      Character.RUNNING_RIGHT: constants.MC_RUNNING_RIGHT,
    }
    self.main_character = MainCharacter(mc_sources)

    ge_sources = {
      Character.STAND_RIGHT: constants.MC_STAND_RIGHT,
      Character.STAND_LEFT: constants.MC_STAND_LEFT,
      Character.STAND_ATTACK_LEFT: constants.MC_STAND_ATTACK_LEFT,
      Character.STAND_ATTACK_RIGHT: constants.MC_STAND_ATTACK_RIGHT,
      Character.RUNNING_LEFT: constants.MC_RUNNING_LEFT,
      Character.RUNNING_RIGHT: constants.MC_RUNNING_RIGHT,
    }
    self.first_boss = GroundEnemy(ge_sources)

    self.add_widget(self.main_character)
    self.add_widget(self.first_boss)

    Clock.schedule_interval(self.check_collisions, 1/60)

  def check_collisions(self, dt):
    if self.main_character.collide_widget(self.first_boss):
      print "COLLIDE"

  def return_to_normal(self, dt):
    self.first_boss.moving = False
    self.first_boss.to_right = self.main_character.to_right
    if self.first_boss.to_right:
      self.first_boss.source = self.first_boss.sources[Character.STAND_RIGHT]
    else:
      self.first_boss.source = self.first_boss.sources[Character.STAND_LEFT]

class Character(Image):
  STAND_LEFT = "stand left"
  STAND_RIGHT = "stand right"
  STAND_ATTACK_LEFT = "stand attack left"
  STAND_ATTACK_RIGHT = "stand attack right"
  RUNNING_LEFT = "running left"
  RUNNING_RIGHT = "running right"
  def __init__(self, sources, **kwargs):
    super(Character, self).__init__(**kwargs)
    self.sources = sources

    self.source = self.sources[Character.STAND_RIGHT]
    self.to_right = True
    self.size = self.texture_size
    self.y = constants.STANDING_Y

    # Game values
    self.moving = False
    self.attacking = False
    self.jumping = False

    Clock.schedule_interval(self.check_moving, 1/60)
    Clock.schedule_interval(self.check_jumping, 1/60)

  def check_moving(self, dt):
    if not self.attacking:
      if self.moving:
        if self.to_right and self.x < (constants.WIDTH - self.width):
          self.source = self.sources[Character.RUNNING_RIGHT]
          self.move(constants.RUNNING_SPEED)
          self.size = self.texture_size
        if not self.to_right and self.x > constants.MIN_X:
          self.source = self.sources[Character.RUNNING_LEFT]
          self.move(-constants.RUNNING_SPEED)
          self.size = self.texture_size

  def move(self, move_by):
    self.x += move_by


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
    if self.to_right:
      self.source = self.sources[Character.STAND_RIGHT]
    else:
      self.source = self.sources[Character.STAND_LEFT]
    self.size = self.texture_size

  def jump(self):
    if not self.jumping:
      anim = Animation(
        y=constants.JUMP_HEIGHT,
        duration=constants.JUMP_DURATION
      ) + Animation(
        y=constants.STANDING_Y,
        duration=constants.JUMP_DURATION
      )
      anim.start(self)

class MainCharacter(Character):
  def __init__(self, sources, **kwargs):
    super(MainCharacter, self).__init__(sources, **kwargs)
    self.x = (constants.MC_X)
    self.on_battle = True

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
      self.to_right = True
      self.moving = True
    elif keycode[1] == "a":
      if self.on_battle:
        self.to_right = False
        self.moving = True
    elif keycode[1] == "w":
      if not self.attacking:
        self.jump()

  def _on_keyboard_up(self, keyboard, keycode):
    if not self.attacking:
      if keycode[1] == "d":
        self.source = self.sources[Character.STAND_RIGHT]
        self.moving = False
      elif keycode[1] == "a":
        self.source = self.sources[Character.STAND_LEFT]
        self.moving = False

class GroundEnemy(Character):
  def __init__(self, sources, **kwargs):
    super(GroundEnemy, self).__init__(sources, **kwargs)
    self.x = 700


