from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
import constants
import random
from kivy.app import *
class CharacterManager(Widget):
  def __init__(self, **kwargs):
    super(CharacterManager, self).__init__(**kwargs)
    mc_sources = {
      constants.STAND_RIGHT: constants.MC_STAND_RIGHT,
      constants.STAND_LEFT: constants.MC_STAND_LEFT,
      constants.STAND_ATTACK_LEFT: constants.MC_STAND_ATTACK_LEFT,
      constants.STAND_ATTACK_RIGHT: constants.MC_STAND_ATTACK_RIGHT,
      constants.RUNNING_LEFT: constants.MC_RUNNING_LEFT,
      constants.RUNNING_RIGHT: constants.MC_RUNNING_RIGHT,
    }
    self.main_character = MainCharacter(mc_sources, constants.MC_LIFE_MAX)

    ge_sources = {
      constants.STAND_RIGHT: constants.HM_STAND_RIGHT,
      constants.STAND_LEFT: constants.HM_STAND_LEFT,
      constants.STAND_ATTACK_LEFT: constants.HM_STAND_ATTACK_LEFT,
      constants.STAND_ATTACK_RIGHT: constants.HM_STAND_ATTACK_RIGHT,
      constants.RUNNING_LEFT: constants.HM_RUNNING_LEFT,
      constants.RUNNING_RIGHT: constants.HM_RUNNING_RIGHT,
    }
    self.horse_man = GroundEnemy(ge_sources, self.main_character, constants.HM_LIFE_MAX)
    #self.horse_man.x = constants.BOSS_POSITION
    self.horse_man.life_meter.value = 0

    wc_sources = [constants.WC_ROCK, constants.WC_PLAYFULL_GIRL, constants.WC_FROGMAN]
    self.weak_enemies = WeakEnemy(wc_sources, self.main_character)

    self.add_widget(self.main_character)
    self.add_widget(self.horse_man)
    self.add_widget(self.weak_enemies)

  def reset(self):
    self.horse_man.reset()
    self.main_character.reset()

class Character(Image):
  def __init__(self, sources, max_life, **kwargs):
    super(Character, self).__init__(**kwargs)
    self.sources = sources

    self.source = self.sources[constants.STAND_RIGHT]
    self.to_right = True
    self.size = self.texture_size
    self.y = constants.STANDING_Y

    self.life_meter = LifeMeter(max=max_life)
    self.add_widget(self.life_meter)

    # Game values
    self.moving = False
    self.attacking = False
    self.jumping = False

    Clock.schedule_interval(self.check_moving, 1/60)
    Clock.schedule_interval(self.check_jumping, 0)
    Clock.schedule_interval(self.show_life, 0)

  def check_moving(self, dt):
    if not self.attacking:
      if self.moving:
        if self.to_right and self.x < (constants.WIDTH - self.width):
          self.source = self.sources[constants.RUNNING_RIGHT]
          self.move(constants.RUNNING_SPEED)
          self.size = self.texture_size
        if not self.to_right and self.x > constants.MIN_X:
          self.source = self.sources[constants.RUNNING_LEFT]
          self.move(-constants.RUNNING_SPEED)
          self.size = self.texture_size

  def move(self, move_by):
    self.x += move_by

  def show_life(self, move_by):
    self.life_meter.x = self.x
    self.life_meter.y = self.y + self.height

  def check_jumping(self, dt):
    if self.y == constants.STANDING_Y:
      self.jumping = False
    else:
      self.jumping = True

  def attack(self):
    if self.to_right:
      self.source = self.sources[constants.STAND_ATTACK_RIGHT]
    else:
      self.source = self.sources[constants.STAND_ATTACK_LEFT]
    self.size = self.texture_size

    self.attacking = True
    Clock.schedule_once(self.change_back, 0.2)

  def change_back(self, dt):
    self.attacking = False
    if self.to_right:
      if self.moving:
        self.source = self.sources[constants.RUNNING_RIGHT]
      else:
        self.source = self.sources[constants.STAND_RIGHT]
    else:
      if self.moving:
        self.source = self.sources[constants.RUNNING_LEFT]
      else:
        self.source = self.sources[constants.STAND_LEFT]
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

  def reset(self):
    self.source = self.sources[constants.STAND_RIGHT]
    self.size = self.texture_size

    self.to_right = True

    self.moving = False
    self.attacking = False
    self.jumping = False

    self.life_meter.reset()

class MainCharacter(Character):
  def __init__(self, sources, max_life, **kwargs):
    super(MainCharacter, self).__init__(sources, max_life, **kwargs)
    self.x = (constants.MC_X)
    self.on_battle = False

    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self._keyboard.bind(on_key_up=self._on_keyboard_up)

    Clock.schedule_interval(self.check_life, 0)

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

  def check_life(self, dt):
    if self.life_meter.value <= 0:
      App.get_running_app().root.current = constants.GAME_OVER_SCREEN

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == "d":
      self.to_right = True
      self.moving = True
      self.source = self.sources[constants.RUNNING_RIGHT]
      self.size = self.texture_size
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
        self.source = self.sources[constants.STAND_RIGHT]
        self.moving = False
      elif keycode[1] == "a":
        if self.on_battle:
          self.source = self.sources[constants.STAND_LEFT]
          self.moving = False

  def reset(self):
    super(MainCharacter, self).reset()
    self.x = constants.MC_X
    self.on_battle = False

class GroundEnemy(Character):
  def __init__(self, sources, main_character, max_life, **kwargs):
    super(GroundEnemy, self).__init__(sources, max_life, **kwargs)
    self.x = constants.CHARACTER_STORAGE
    self.main_character = main_character
    Clock.schedule_interval(self.check_life, 0.1)

    self.milliseconds = 0
    Clock.schedule_interval(self.check_collisions, 0)
    Clock.schedule_interval(self.decide_actions, .1)

    self.active = False

  def check_life(self, dt):
    if self.life_meter.value <= 0:
      self.move(constants.CHARACTER_STORAGE)

  def check_collisions(self, dt):
    if self.collide_widget(self.main_character):
      if self.main_character.attacking:
        self.life_meter.decrease_life(constants.HIT_DMG)
      if self.attacking:
        self.main_character.life_meter.decrease_life(constants.HIT_DMG)
      else:
        self.attack()

  def decide_actions(self, dt):
    if self.life_meter.value <= 0:
      Clock.unschedule(self.decide_actions)
    self.milliseconds += 1
    if self.active:
      if self.milliseconds % constants.SECONDS_CHECK == 0:
        if self.x >= (constants.WIDTH - self.width):
          walk_left =  random.randint(0, 1)
          if walk_left:
            self.moving = True
            self.to_right = False
          else:
            self.jump()
            self.moving = True
            self.to_right = False
        elif self.x <= constants.MIN_X:
          walk_right =  random.randint(0, 1)
          if walk_right:
            self.moving = True
            self.to_right = True
          else:
            self.jump()
            self.moving = True
            self.to_right = True
        else:
          self.moving = True
          self.to_right = random.randint(0,1)

  def return_to_normal(self, dt):
    self.horse_man.moving = False
    self.horse_man.to_right = self.main_character.to_right
    if self.horse_man.to_right:
      self.horse_man.source = self.horse_man.sources[constants.STAND_RIGHT]
    else:
      self.horse_man.source = self.horse_man.sources[constants.STAND_LEFT]

  def reset(self):
    super(GroundEnemy, self).reset()
    self.x = constants.CHARACTER_STORAGE
    self.active = False

class WeakEnemy(Image):
  def __init__(self, sources, main_character, **kwargs):
    super(WeakEnemy, self).__init__(x=constants.CHARACTER_STORAGE, y=constants.STANDING_Y)
    self.sources = sources
    self.source = sources[0]
    self.main_character = main_character
    self.size = self.texture_size
    self.x = constants.CHARACTER_STORAGE

    Clock.schedule_interval(self.check_collisions, 0.1)
    Clock.schedule_interval(self.attack_player, 0)

  def attack_player(self, dt):
    if self.x <= -self.width:
      self.reset()
    else:
      if self.main_character.moving:
        self.x -= constants.WC_MOVEMENT_FAST
      else:
        self.x -= constants.WC_MOVEMENT_SLOW

  def check_collisions(self, dt):
    if self.collide_widget(self.main_character):
      if not self.main_character.attacking:
        self.main_character.life_meter.decrease_life(constants.WC_DMG)
      self.reset()

  def reset(self):
    res = random.randint(0, len(self.sources) - 1)
    self.source = self.sources[res]
    self.size = self.texture_size
    self.x = constants.CHARACTER_STORAGE

class LifeMeter(ProgressBar):
  def __init__(self, **kwargs):
    super(LifeMeter, self).__init__(**kwargs)
    self.value = self.max
    self.width = self.max * 2

  def decrease_life(self, dmg):
    self.value -= dmg

  def reset(self):
    self.value = self.max
