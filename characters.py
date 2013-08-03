from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import *
from kivy.app import App
import constants
import random
"""
  Class: CharacterManager
  Description: Manages all characters and their behaviour.
"""
class CharacterManager(Widget):
  """
    Constructor
  """
  difficulty = NumericProperty(1)
  def __init__(self, **kwargs):
    super(CharacterManager, self).__init__(**kwargs)
    self.scorer = Scorer()
    self.scorer.pos = constants.SCORER_POS
    self.add_widget(self.scorer)

    self.create_horseman_boss()
    self.create_main_character()
    self.create_weak_enemies()
    self.create_special_items()

    self.weak_enemies_attack = 0

  """
    Method: create_main_character
    Description: Method called to create the avatar to be controlled by the user.
  """
  def create_horseman_boss(self):
    hm_sources = {
      constants.STAND_RIGHT: constants.HM_STAND_RIGHT,
      constants.STAND_LEFT: constants.HM_STAND_LEFT,
      constants.STAND_ATTACK_LEFT: constants.HM_STAND_ATTACK_LEFT,
      constants.STAND_ATTACK_RIGHT: constants.HM_STAND_ATTACK_RIGHT,
      constants.RUNNING_LEFT: constants.HM_RUNNING_LEFT,
      constants.RUNNING_RIGHT: constants.HM_RUNNING_RIGHT,
      constants.DAMAGED: constants.HM_DAMAGED,
      constants.DEAD: constants.HM_DEAD
    }
    self.horseman = BossCharacter(hm_sources, constants.HM_LIFE_MAX)
    self.add_widget(self.horseman)

  """
    Method: create_main_character
    Description: Method called to create the avatar to be controlled by the user.
  """
  def create_main_character(self):
    mc_sources = {
      constants.STAND_RIGHT: constants.MC_STAND_RIGHT,
      constants.STAND_LEFT: constants.MC_STAND_LEFT,
      constants.STAND_ATTACK_LEFT: constants.MC_STAND_ATTACK_LEFT,
      constants.STAND_ATTACK_RIGHT: constants.MC_STAND_ATTACK_RIGHT,
      constants.RUNNING_LEFT: constants.MC_RUNNING_LEFT,
      constants.RUNNING_RIGHT: constants.MC_RUNNING_RIGHT,
      constants.DAMAGED: constants.MC_DAMAGED,
      constants.DEAD: constants.MC_DEAD
    }
    self.main_character = MainCharacter(mc_sources, constants.MC_LIFE_MAX)
    self.add_widget(self.main_character)

  """
    Method: create_weak_enemies
    Description: Method called to create the weak enemies.
  """
  def create_weak_enemies(self):
    self.weak_enemies = []
    for i in range(0, constants.ROCK_COUNT):
      rock = WeakEnemy(
        constants.WC_ROCK,
        constants.WC_ROCK_IMAGE_DMG,
        constants.WC_ROCK_DMG,
        constants.WC_ROCK_SPEED
      )
      self.weak_enemies.append(rock)
      self.add_widget(rock)

    for i in range(0, constants.PLAYFULL_GIRL_COUNT):
      playfull_girl = WeakEnemy(
        constants.WC_PLAYFULL_GIRL,
        constants.WC_PLAYFULL_GIRL_IMAGE_DMG,
        constants.WC_PLAYFULL_GIRL_DMG,
        constants.WC_PLAYFULL_GIRL_SPEED,
        normal_sounds=[constants.WC_PLAYFULL_GIRL_YELL_SOUND_1, constants.WC_PLAYFULL_GIRL_YELL_SOUND_2],
        die_sounds=constants.WC_PLAYFULL_GIRL_DIE_SOUND,
        jumper=True
      )
      self.weak_enemies.append(playfull_girl)
      self.add_widget(playfull_girl)

    for i in range(0, constants.FROGMAN_COUNT):
      frogman = WeakEnemy(
        constants.WC_FROGMAN,
        constants.WC_FROGMAN_IMAGE_DMG,
        constants.WC_FROGMAN_DMG,
        constants.WC_FROGMAN_SPEED,
        normal_sounds=[constants.WC_FROGMAN_YELL_SOUND_1, constants.WC_FROGMAN_YELL_SOUND_2],
        die_sounds=constants.WC_FROGMAN_DIE_SOUND,
        jumper=True
      )
      self.weak_enemies.append(frogman)
      self.add_widget(frogman)

  """
    Method: create_special_items
    Description: Method called to create the special items.
  """
  def create_special_items(self):
    self.special_items = []
    for i in range(0, constants.HEART_COUNT):
      heart = Heart(self.main_character)
      self.special_items.append(heart)
      self.add_widget(heart)
    for i in range(0, constants.CANDY_COUNT):
      candy = Candy(self.main_character)
      self.special_items.append(candy)
      self.add_widget(candy)
    for i in range(0, constants.COIN_COUNT):
      coin = Coin(self.main_character)
      self.special_items.append(coin)
      self.add_widget(coin)

  """
    Method: on_enter
    Description: Method to be called when the widget enters the game.
  """
  def on_enter(self):
    self.difficulty = self.parent.parent.difficulty
    self.weak_enemies_attack = 0

    Clock.schedule_interval(self.check_collisions, 0)
    Clock.schedule_interval(self.control_weak_enemies, 0.5)
    Clock.schedule_interval(self.control_items, 0.3)
    Clock.schedule_interval(self.control_game, 0)

    self.horseman.on_enter()
    self.main_character.on_enter()
    for weak_enemy in self.weak_enemies:
      weak_enemy.on_enter()
    self.scorer.reset()
    for item in self.special_items:
      item.on_enter()

  """
    Method: on_leave
    Description: Method to be called when the widget exits the game.
  """
  def on_leave(self):
    Clock.unschedule(self.check_collisions)
    Clock.unschedule(self.control_weak_enemies)
    Clock.unschedule(self.control_items)
    Clock.unschedule(self.control_game)

    self.main_character.on_leave()
    self.horseman.on_leave()
    for weak_enemy in self.weak_enemies:
      weak_enemy.on_leave()
    for item in self.special_items:
      item.on_leave()

  """
    Method: check_collisions
    Description: Method that checks for collisions.
  """
  def check_collisions(self, dt):
    if self.main_character.alive:
      for weak_enemy in self.weak_enemies:
        if self.main_character.collide_widget(weak_enemy):
          if self.main_character.attacking:
            weak_enemy.damaged()
          else:
            self.main_character.life_meter.decrease_life(weak_enemy.dmg)
            self.main_character.damaged()
            weak_enemy.reset()
      for item in self.special_items:
        if self.main_character.collide_widget(item):
          item.use_effect()
          item.reset()

      # When the main character collides with the boss
      if self.main_character.collide_widget(self.horseman):
        # Make sure the images dont overlap each other
        if self.horseman.x > self.main_character.x + (self.main_character.width / 2):
          if self.main_character.x + self.main_character.width < (constants.WIDTH - self.width):
            self.horseman.x = self.main_character.x + self.main_character.width
          else:
            self.main_character.x = self.horseman.x - self.main_character.width
        else:
          if self.main_character.x - self.horseman.width > constants.MIN_X:
            self.horseman.x = self.main_character.x - self.horseman.width
          else:
            self.main_character.x = self.horseman.x + self.horseman.width

        if not self.horseman.attacking:
          self.horseman.to_right = not self.main_character.to_right
          self.horseman.attack()

        # Make the attacks happen
        if self.main_character.attacking and not self.horseman.hit:
          self.horseman.damaged()
          self.horseman.life_meter.decrease_life(constants.MAIN_CHAR_HIT_DMG / self.difficulty)

        if self.horseman.attacking and not self.main_character.hit:
          self.main_character.damaged()
          self.main_character.life_meter.decrease_life(constants.HIT_DMG * self.difficulty)

  """
    Method: control_weak_enemies
    Description: Method that controls all weak enemies.
  """
  def control_weak_enemies(self, dt):
    res = random.randint(0,1)
    if res:
      weak_enemy = random.choice(self.weak_enemies)
      weak_enemy.run = True
      self.weak_enemies_attack += 1

  """
    Method: control_items
    Description: Method that controls all items.
  """
  def control_items(self, dt):
    res = random.randint(0,1)
    if res:
      item = random.choice(self.special_items)
      item.run = True

  """
    Method: control_game
    Description: Method that controls the game.
  """
  def control_game(self, dt):
    if self.weak_enemies_attack >= constants.ENEMY_MAX:
      self.main_character.on_battle = True
      self.main_character.moving = False

      Clock.unschedule(self.control_weak_enemies)
      Clock.unschedule(self.control_items)
      for weak_enemy in self.weak_enemies:
        weak_enemy.reset()
        weak_enemy.run = False
      for item in self.special_items:
        item.reset()
        item.run = False

      self.horseman.animate_entrance()
      Clock.unschedule(self.control_game)

  """
    Method: to_game_over
    Description: Moves the screen to game over screen
  """
  def to_game_over(self, dt):
    if not self.horseman.alive:
      self.scorer.score += constants.HM_BOSS_BONUS * self.difficulty
    App.get_running_app().root.final_score = self.scorer.score
    App.get_running_app().root.current = constants.GAME_OVER_SCREEN

#---------------------------------------------------------------------------------

"""
  Class: Character
  Description: A character that has life and can move around the screen.
    Has a life meter and various images for different action.
"""
class Character(Image):
  alive = BooleanProperty(True)
  to_right = BooleanProperty(True)
  moving = BooleanProperty(True)
  jumping = BooleanProperty(False)
  attacking = BooleanProperty(False)
  hit = BooleanProperty(False)
  on_battle = BooleanProperty(False)
  """
    Constructor
  """
  def __init__(self, sources, max_life, **kwargs):
    super(Character, self).__init__(**kwargs)
    self.sources = sources
    self.life_meter = LifeMeter(max=max_life)
    self.add_widget(self.life_meter)
    self.sources = sources
    self.change_src(constants.STAND_RIGHT)
    self.life_meter.pos = (self.x, self.y + self.height + 100)

  """
    Method: on_enter
    Description: Method to be called when the widget enters the game.
  """
  def on_enter(self):
    self.alive, self.to_right, self.moving, self.jumping, self.attacking, self.on_battle = True, True, True, False, False, False
    self.life_meter.reset()
    Clock.schedule_interval(self.check_life, 0)
    Clock.schedule_interval(self.check_movement_images, 0)
    Clock.schedule_interval(self.check_jumping, 0)
    Clock.schedule_interval(self.move_character, 0)

  """
    Method: on_leave
    Description: Method to be called when the widget exits the game.
  """
  def on_leave(self):
    Clock.unschedule(self.check_life)
    Clock.unschedule(self.check_movement_images)
    Clock.unschedule(self.check_jumping)
    Clock.unschedule(self.move_character)

  """
    Method: check_life
    Description: Method that checks if the character is alive or dead.
  """
  def check_life(self, dt):
    self.life_meter.pos = (self.x, self.y + self.height)
    if self.life_meter.value <= 0:
      self.alive = False

  """
    method: check_jumping
    description: method that checks if the character is jumping.
  """
  def check_jumping(self, dt):
    if self.y != constants.STANDING_Y:
      self.jumping = True
    else:
      self.jumping = False

  """
    Method: attack
    Description: Method used to make the character attack.
  """
  def attack(self):
    if not self.attacking and not self.hit and self.alive:
      if self.to_right:
        self.change_src(constants.STAND_ATTACK_RIGHT)
      else:
        self.change_src(constants.STAND_ATTACK_LEFT)
      self.attacking = True
      Clock.schedule_once(self.change_back, 0.3)

  """
    Method: damaged
    Description: Method used to make the character looked like attacked.
  """
  def damaged(self):
    if not self.attacking and not self.hit and self.alive:
      self.change_src(constants.DAMAGED)
      self.hit = True
      Clock.schedule_once(self.change_back, 0.3)

  """
    Method: change_back
    Description: Changes the character back to its proper image.
  """
  def change_back(self, dt):
    if self.to_right:
      self.change_src(constants.STAND_RIGHT)
    else:
      self.change_src(constants.STAND_LEFT)
    self.attacking = False
    self.hit = False

  """
    Method: jump
    Description: Method used to make the character jump.
  """
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

  """
    Method: move_character
    Description: Moves the character based on its moving values
  """
  def move_character(self, dt):
    if not self.attacking and not self.hit and self.alive and self.moving and self.on_battle:
      if self.to_right and self.x < (constants.WIDTH - self.width):
        self.x += constants.RUNNING_SPEED
      if not self.to_right and self.x > constants.MIN_X:
        self.x -= constants.RUNNING_SPEED

  """
    Method: check_movement_images
    Description: Method that changes the source base on the movement variables.
  """
  def check_movement_images(self, dt):
    if not self.attacking and not self.hit and self.alive:
      if self.to_right:
        if self.moving:
          self.change_src(constants.RUNNING_RIGHT)
        else:
          self.change_src(constants.STAND_RIGHT)
      else:
        if self.moving:
          self.change_src(constants.RUNNING_LEFT)
        else:
          self.change_src(constants.STAND_LEFT)
    if not self.alive:
      self.change_src(constants.DEAD)

  """
    Method: change_src
    Description: Changes the source of the image.
  """
  def change_src(self, key):
    if self.source != self.sources[key]:
      self.source = self.sources[key]
      self.size = self.texture_size

#---------------------------------------------------------------------------------

"""
  Class: MainCharacter
  Description: The avatar that the user controls.
"""
class MainCharacter(Character):
  """
    Constructor
  """
  keyboard_on = BooleanProperty(False)
  def __init__(self, sources, max_life, **kwargs):
    super(MainCharacter, self).__init__(sources, max_life, **kwargs)
    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self._keyboard.bind(on_key_up=self._on_keyboard_up)
    self.pos = (constants.MC_X, constants.STANDING_Y)

  """
    Method: keyboard_closed
    Description: Called when the keyboard is closed.
  """
  def _keyboard_closed(self):
    if self.alive and self.keyboard_on:
      self._keyboard.unbind(on_key_down=self._on_keyboard_down)
      self._keyboard.unbind(on_key_up=self._on_keyboard_up)
      self._keyboard = None

  """
    Method: on_touch_down
    Description: Called when the mouse is clicked.
  """
  def on_touch_down(self, touch):
    if self.alive:
      self.attack()
      return super(Character, self).on_touch_down(touch)

  """
    Method: on_keyboard_down
    Description: Called when a key is pressed.
  """
  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if self.alive and self.keyboard_on:
      if self.on_battle:
        if keycode[1] == "d":
          self.moving, self.to_right = True, True
        elif keycode[1] == "a":
          self.moving, self.to_right = True, False
      if keycode[1] == "w":
        self.jump()

  """
    Method: on_keyboard_up
    Description: Called when a key is up.
  """
  def _on_keyboard_up(self, keyboard, keycode):
    if self.alive and self.keyboard_on and self.on_battle:
      if keycode[1] == "d":
        self.moving = False
      elif keycode[1] == "a":
        self.moving = False

  # OVERRIDEN METHODS
  """
    Method: on_enter
    Description: Method to be called when the widget enters the game.
  """
  def on_enter(self):
    super(MainCharacter, self).on_enter()
    self.keyboard_on = True
    Clock.schedule_interval(self.check_moving, 0)
    self.pos = (constants.MC_X, constants.STANDING_Y)

  """
    Method: on_leave
    Description: Method to be called when the widget exits the game.
  """
  def on_leave(self):
    super(MainCharacter, self).on_leave()
    self.keyboard_on = False
    Clock.unschedule(self.check_moving)

  """
    Method: check_movement_images
    Description: Method that changes the source base on the movement variables.
  """
  def check_movement_images(self, dt):
    if not self.attacking and not self.hit:
      if self.on_battle or not self.alive:
        super(MainCharacter, self).check_movement_images(dt)
      else:
        self.change_src(constants.RUNNING_RIGHT)

  """
    Method: check_moving
    Description: Method that checks if the character is moving. This moves the bg.
  """
  def check_moving(self, dt):
    if not self.on_battle and self.alive:
      self.parent.parent.background.move_all()

  """
    Method: change_back
    Description: Changes the character back to its proper image.
  """
  def change_back(self, dt):
    if self.on_battle:
      super(MainCharacter, self).change_back(dt)
    else:
      self.change_src(constants.RUNNING_RIGHT)
    self.attacking = False
    self.hit = False

  """
    Method: check_life
    Description: Method that checks if the character is alive or dead.
  """
  def check_life(self, dt):
    super(MainCharacter, self).check_life(dt)
    if not self.alive:
      Clock.unschedule(self.check_life)
      Clock.schedule_once(self.parent.to_game_over, 2)

#---------------------------------------------------------------------------------
"""
  Class: BossCharacter
  Description: Boss character that is to be killed by the main character to finish the game.
"""
class BossCharacter(Character):
  """
    CONSTRUCTOR
  """
  def __init__(self, sources, max_life, **kwargs):
    super(BossCharacter, self).__init__(sources, max_life, **kwargs)
    self.pos = (constants.CHARACTER_STORAGE, constants.STANDING_Y)

  """
    Method: animate_entrance
    Description: Creates an animated entrance for the boss.
  """
  def animate_entrance(self):
    anim = Animation(x=constants.BOSS_POSITION, duration=1)
    anim.start(self)
    def change_back(dt):
      self.to_right = False
      self.moving = False
      self.on_battle = True
    Clock.schedule_once(change_back, 1)

  def decide_actions(self, dt):
    if self.alive and self.on_battle and not self.hit and not self.attacking:
      res = random.randint(0, 3)
      if res == 0:
        self.to_right = True
        self.moving = True
      elif res == 1:
        self.to_right = False
        self.moving = True
      elif res == 2:
        self.jump()
      elif res == 3:
        self.moving = False

  """
    Method: on_enter
    Description: Method to be called when the widget enters the game.
  """
  def on_enter(self):
    super(BossCharacter, self).on_enter()
    Clock.schedule_interval(self.decide_actions, 0.5)
    self.pos = (constants.CHARACTER_STORAGE, constants.STANDING_Y)
    self.to_right = False
    self.on_battle = False

  """
    Method: on_leave
    Description: Method to be called when the widget exits the game.
  """
  def on_leave(self):
    super(BossCharacter, self).on_leave()
    Clock.unschedule(self.decide_actions)

  """
    Method: check_life
    Description: Method that checks if the character is alive or dead.
  """
  def check_life(self, dt):
    super(BossCharacter, self).check_life(dt)
    if not self.alive:
      Clock.unschedule(self.check_life)
      Clock.schedule_once(self.parent.to_game_over, 2)

#---------------------------------------------------------------------------------

# OTHER CLASSES
"""
  Class: LifeMeter
  Description: A bar showing how much life characters still has.
"""
class LifeMeter(ProgressBar):
  """
    Constructor
  """
  def __init__(self, **kwargs):
    super(LifeMeter, self).__init__(**kwargs)
    self.value = self.max
    self.width = self.max * 1.5

  """
    Method: decrease_life
    Description: Decreases life by the value passed.
  """
  def decrease_life(self, dmg):
    self.value -= dmg

  """
    Method: reset
    Description: Resets the life meter to its old value.
  """
  def reset(self):
    self.value = self.max

#---------------------------------------------------------------------------------

"""
  Class: Scorer
  Description: Shows the current score the user acquired.
"""
class Scorer(Label):
  """
    Constructor
  """
  def __init__(self, **kwargs):
    super(Scorer, self).__init__(font_size="80px", markup=True, **kwargs)
    Clock.schedule_interval(self.update_text, 0)
    self.score = 0

  """
    Method: update_text
    Description: Updates the text to the current score.
  """
  def update_text(self, dt):
    self.text = '[color=79C99A]' + constants.SCORE_TEXT + str(self.score) + '[/color]'

  """
    Method: reset
    Description: Resets the score to 0.
  """
  def reset(self):
    self.score = 0

#---------------------------------------------------------------------------------
"""
  Class: WeakEnemy
  Description: The weak enemy that attacks the user. Dies in one hit.
"""
class WeakEnemy(Image):
  """
    Constructor
  """
  def __init__(self, source, damaged_img, dmg, speed, normal_sounds=None, die_sounds=None, jumper=False, **kwargs):
    super(WeakEnemy, self).__init__(source=constants.WC_ROCK, x=constants.CHARACTER_STORAGE, y=constants.STANDING_Y)
    self.the_source = source
    self.initial_dmg = dmg
    self.dmg = dmg
    self.speed = speed
    self.jumper = jumper
    self.damaged_img = damaged_img
    self.normal_sounds = normal_sounds
    self.die_sounds = die_sounds
    self.pos = (constants.CHARACTER_STORAGE, constants.STANDING_Y)
    self.run = False
    self.jumping = False

  """
    Method: damaged
    Description: Method that shows the weak enemy damaged.
  """
  def damaged(self):
    self.source = self.damaged_img
    self.size = self.texture_size
    anim = Animation(x=self.x + 200, duration=0.3)
    anim.start(self)
    self.run = False
    def reset_pend(dt):
      self.reset()
    Clock.schedule_once(reset_pend, 0.4)

  """
    Method: start_running
    Description: Move the weak enemy closer to the main character
  """
  def start_running(self, dt):
    if self.run:
      self.x -= self.speed
      res = random.randint(0,10)
      if not self.jumping and res == 0:
        self.jump()

  """
    Method: jump
    Description: Method used to make the weak enemy jump.
  """
  def jump(self):
    if not self.jumping and self.jumper:
      anim = Animation(
        y=constants.JUMP_HEIGHT,
        duration=constants.JUMP_DURATION
      ) + Animation(
        y=constants.STANDING_Y,
        duration=constants.JUMP_DURATION
      )
      anim.start(self)

  """
    method: check_jumping
    description: method that checks if the character is jumping.
  """
  def check_jumping(self, dt):
    if self.y != constants.STANDING_Y:
      self.jumping = True
    else:
      self.jumping = False

  """
    Method: normal_sound
    Description: Play the normal sound.
  """
  def normal_sound(self):
    if self.normal_sounds != None:
      SoundLoader.load(random.choice(self.normal_sounds)).play()

  """
    Method: die_sound
    Description: Play the die sound.
  """
  def die_sound(self):
    if self.die_sounds != None:
      SoundLoader.load(random.choice(self.die_sounds)).play()

  """
    Method: on_enter
    Description: Method to be called when the widget enters the game.
  """
  def on_enter(self):
    self.pos = (constants.CHARACTER_STORAGE, constants.STANDING_Y)
    self.source = self.the_source
    self.size = self.texture_size
    self.run = False
    self.dmg = self.initial_dmg * self.parent.difficulty
    Clock.schedule_interval(self.start_running, 0)
    Clock.schedule_interval(self.check_jumping, 0)

  """
    Method: on_leave
    Description: Method to be called when the widget exits the game.
  """
  def on_leave(self):
    self.reset()
    Clock.unschedule(self.start_running)
    Clock.unschedule(self.check_jumping)

  """
    Method: reset
    Description: Sends the weak enemy back to its storage.
  """
  def reset(self):
    self.run = False
    self.pos = (constants.CHARACTER_STORAGE, constants.STANDING_Y)
    self.source = self.the_source
    self.size = self.texture_size
#---------------------------------------------------------------------------------
"""
  Class: SpecialItem
  Description: Special Item that helps the user.
"""
class SpecialItem(Image):
  """
    CONSTRUCTOR
  """
  def __init__(self, main_character, **kwargs):
    super(SpecialItem, self).__init__(**kwargs)
    self.main_character = main_character
    self.size = self.texture_size
    self.pos = (constants.CHARACTER_STORAGE, constants.STANDING_Y)

  """
    Method: use_effect
    Description: Use the effect of the special item.
  """
  def use_effect(self):
    pass

  """
    Method: start_running
    Description: Move the item closer to the main character
  """
  def start_running(self, dt):
    if self.run and self.main_character.alive:
      self.x -= constants.WC_ROCK_SPEED

  """
    Method: on_enter
    Description: Method to be called when the widget enters the game.
  """
  def on_enter(self):
    self.reset()
    Clock.schedule_interval(self.start_running, 0)

  """
    Method: on_leave
    Description: Method to be called when the widget exits the game.
  """
  def on_leave(self):
    Clock.unschedule(self.start_running)

  """
    Method: reset
    Description: Sends the item back to its storage.
  """
  def reset(self):
    up = random.randint(0, 1)
    if up:
      self.y = constants.STANDING_Y
    else:
      self.y = constants.JUMP_HEIGHT - 10
    self.x = constants.CHARACTER_STORAGE
    self.run = False

"""
  Class: Heart
  Description: Adds life to the user.
"""
class Heart(SpecialItem):
  def __init__(self, main_character, **kwargs):
    super(Heart, self).__init__(main_character, source=constants.HEART_IMG, **kwargs)

  def use_effect(self):
    self.main_character.life_meter.value += 100

"""
  Class: Candy
  Description: Adds additional points.
"""
class Candy(SpecialItem):
  def __init__(self, main_character, **kwargs):
    super(Candy, self).__init__(main_character, source=constants.CANDY_IMG, **kwargs)

  def use_effect(self):
    self.main_character.parent.scorer.score += 100

"""
  Class: Coin
  Description: Add points.
"""
class Coin(SpecialItem):
  def __init__(self, main_character, **kwargs):
    super(Coin, self).__init__(main_character, source=constants.COIN_IMG, **kwargs)

  def use_effect(self):
    self.main_character.parent.scorer.score += 10
