from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
import constants
import random
from kivy.app import *
class CharacterManager(Widget):
  def __init__(self, **kwargs):
    super(CharacterManager, self).__init__(**kwargs)
    self.difficulty = constants.DIFFICULTY_EASY
    self.enemy_count = 0

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

    ge_sources = {
      constants.STAND_RIGHT: constants.HM_STAND_RIGHT,
      constants.STAND_LEFT: constants.HM_STAND_LEFT,
      constants.STAND_ATTACK_LEFT: constants.HM_STAND_ATTACK_LEFT,
      constants.STAND_ATTACK_RIGHT: constants.HM_STAND_ATTACK_RIGHT,
      constants.RUNNING_LEFT: constants.HM_RUNNING_LEFT,
      constants.RUNNING_RIGHT: constants.HM_RUNNING_RIGHT,
      constants.DAMAGED: constants.HM_DAMAGED,
      constants.DEAD: constants.HM_DEAD
    }
    self.horse_man = GroundEnemy(ge_sources, self.main_character, constants.HM_LIFE_MAX * self.difficulty)
    self.horse_man.x = constants.CHARACTER_STORAGE

    self.rock_obstacle = WeakEnemy(
      constants.WC_ROCK,
      constants.WC_ROCK_DMG * self.difficulty,
      constants.WC_ROCK_SPEED,
      self.main_character,
      constants.WC_ROCK_IMAGE_DMG
    )
    self.playfull_girl = SoundedWeakEnemy(
      constants.WC_PLAYFULL_GIRL,
      constants.WC_PLAYFULL_GIRL_DMG * self.difficulty,
      constants.WC_PLAYFULL_GIRL_SPEED,
      self.main_character,
      constants.WC_PLAYFULL_GIRL_IMAGE_DMG,
      [
        SoundLoader.load(constants.WC_PLAYFULL_GIRL_YELL_SOUND_1),
        SoundLoader.load(constants.WC_PLAYFULL_GIRL_YELL_SOUND_2)
      ],
      SoundLoader.load(constants.WC_PLAYFULL_GIRL_DIE_SOUND),
      jumper=True
    )
    self.frogman = SoundedWeakEnemy(
      constants.WC_FROGMAN,
      constants.WC_FROGMAN_DMG * self.difficulty,
      constants.WC_FROGMAN_SPEED,
      self.main_character,
      constants.WC_FROGMAN_IMAGE_DMG,
      [
        SoundLoader.load(constants.WC_FROGMAN_YELL_SOUND_1),
        SoundLoader.load(constants.WC_FROGMAN_YELL_SOUND_2)
      ],
      SoundLoader.load(constants.WC_FROGMAN_DIE_SOUND),
      jumper=True
    )

    self.main_character.attack_dmg_dur = 0.2
    self.horse_man.attack_dmg_dur = 0.4

    self.main_character.opp_attack_dmg_dur = self.horse_man.attack_dmg_dur
    self.horse_man.opp_attack_dmg_dur = self.main_character.attack_dmg_dur

    self.weak_enemies = []
    self.weak_enemies.append(self.rock_obstacle)
    self.weak_enemies.append(self.playfull_girl)
    self.weak_enemies.append(self.frogman)

    self.add_widget(self.main_character)
    self.add_widget(self.horse_man)
    self.add_widget(self.rock_obstacle)
    self.add_widget(self.playfull_girl)
    self.add_widget(self.frogman)

  def reset(self):
    self.horse_man.reset()
    self.main_character.reset()
    for weak_enemy in self.weak_enemies:
      weak_enemy.on_leave()
    self.enemy_count = 0
    Clock.unschedule(self.attack_player)
    Clock.unschedule(self.check_boss_fight)

  def check_boss_fight(self, dt):
    if self.enemy_count > constants.ENEMY_MAX:
      self.main_character.on_battle = True
      self.horse_man.animate_entrance()
      self.main_character.source = self.main_character.sources[constants.STAND_RIGHT]
      self.horse_man.source = self.horse_man.sources[constants.RUNNING_LEFT]
      self.horse_man.size = self.horse_man.texture_size
      self.horse_man.active = True
      Clock.unschedule(self.check_boss_fight)

  def on_enter(self):
    self.difficulty = self.parent.parent.difficulty
    self.rock_obstacle.dmg = constants.WC_ROCK_DMG * self.difficulty
    self.playfull_girl.dmg = constants.WC_PLAYFULL_GIRL_DMG * self.difficulty
    self.frogman.dmg = constants.WC_FROGMAN_DMG * self.difficulty
    self.horse_man.on_enter()
    self.main_character.on_enter()
    for weak_enemy in self.weak_enemies:
      weak_enemy.on_enter()
    Clock.schedule_interval(self.attack_player, 0)
    Clock.schedule_interval(self.check_boss_fight, 0)

  def attack_player(self, dt):
    for enemy in self.weak_enemies:
      if enemy.attacking:
        return
    selected_enemy = random.choice(self.weak_enemies)
    selected_enemy.attacking = True
    self.enemy_count += 1

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

    self.attack_dmg_dur = 0
    self.opp_attack_dmg_dur = 0

    # Game values
    self.moving = False
    self.attacking = False
    self.jumping = False
    self.hit = False

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
    if not self.hit and not self.attacking:
      if self.to_right:
        self.source = self.sources[constants.STAND_ATTACK_RIGHT]
      else:
        self.source = self.sources[constants.STAND_ATTACK_LEFT]
      self.size = self.texture_size

      self.attacking = True
      Clock.schedule_once(self.change_back, self.opp_attack_dmg_dur)

  def check_life(self, dt):
    if self.alive:
      def move_to_game_over(dt):
        App.get_running_app().root.current = constants.GAME_OVER_SCREEN
      if self.life_meter.value <= 0:
        self.alive = False
        self.source = self.sources[constants.DEAD]
        self.size = self.texture_size
        Clock.schedule_once(move_to_game_over, 2)

  def damaged(self):
    self.source = self.sources[constants.DAMAGED]
    self.size = self.texture_size
    self.hit = True
    Clock.schedule_once(self.change_back, self.opp_attack_dmg_dur)

  def change_back(self, dt):
    self.hit = False
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

    Clock.unschedule(self.check_moving)
    Clock.unschedule(self.check_jumping)
    Clock.unschedule(self.check_life)

  def on_enter(self):
    Clock.schedule_interval(self.check_moving, 1/60)
    Clock.schedule_interval(self.check_jumping, 0)
    Clock.schedule_interval(self.check_life, 0)
    self.alive = True

class MainCharacter(Character):
  def __init__(self, sources, max_life, **kwargs):
    super(MainCharacter, self).__init__(sources, max_life, **kwargs)
    self.x = (constants.MC_X)
    self.on_battle = False

    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self._keyboard.bind(on_key_up=self._on_keyboard_up)

    self.taunt_sounds = [SoundLoader.load(constants.MC_TAUNT_SOUND_1),SoundLoader.load(constants.MC_TAUNT_SOUND_2),SoundLoader.load(constants.MC_TAUNT_SOUND_3)]
    self.die_sounds = [SoundLoader.load(constants.MC_DIE_SOUND_1),SoundLoader.load(constants.MC_DIE_SOUND_2)]

  def _keyboard_closed(self):
    if self.alive:
      self._keyboard.unbind(on_key_down=self._on_keyboard_down)
      self._keyboard.unbind(on_key_up=self._on_keyboard_up)
      self._keyboard = None

  def on_touch_down(self, touch):
    if self.alive:
      if not self.attacking:
        self.attack()
      return super(Character, self).on_touch_down(touch)

  def change_back(self, dt):
    if self.alive:
      if self.on_battle:
        super(MainCharacter, self).change_back(dt)
      else:
        self.attacking = False
        self.hit = False
        self.source = self.sources[constants.RUNNING_RIGHT]
        self.size = self.texture_size

  def check_moving(self, dt):
    if self.alive:
      if self.moving and self.on_battle:
        super(MainCharacter, self).check_moving(dt)
      if not self.on_battle:
        self.parent.parent.background.move_all()

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if self.alive:
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
    if self.alive:
      if not self.attacking and self.on_battle:
        if keycode[1] == "d":
          self.source = self.sources[constants.STAND_RIGHT]
          self.moving = False
        elif keycode[1] == "a":
          if self.on_battle:
            self.source = self.sources[constants.STAND_LEFT]
            self.moving = False

  def on_enter(self):
    super(MainCharacter, self).on_enter()
    self.source = self.sources[constants.RUNNING_RIGHT]
    self.size = self.texture_size

  def reset(self):
    super(MainCharacter, self).reset()
    self.x = constants.MC_X
    self.on_battle = False
    self.source = self.sources[constants.STAND_RIGHT]
    self.size = self.texture_size

class GroundEnemy(Character):
  def __init__(self, sources, main_character, max_life, **kwargs):
    super(GroundEnemy, self).__init__(sources, max_life, **kwargs)
    self.x = constants.CHARACTER_STORAGE
    self.main_character = main_character

    self.milliseconds = 0

    self.active = False

  def check_collisions(self, dt):
    if self.alive and self.main_character.alive:
      if self.collide_widget(self.main_character) and not self.hit:
        if self.main_character.attacking:
          self.damaged()
          self.life_meter.decrease_life(constants.MAIN_CHAR_HIT_DMG)
          self.main_character.taunt_sounds[random.randint(0,2)].play()
        if self.attacking:
          self.main_character.damaged()
          self.main_character.life_meter.decrease_life(constants.HIT_DMG * self.parent.difficulty)
          self.main_character.die_sounds[random.randint(0,1)].play()
        self.attack()

  def animate_entrance(self):
    def change_back(dt):
      self.source = self.sources[constants.STAND_LEFT]
      self.size = self.texture_size
    anim = Animation(x=constants.BOSS_POSITION, duration=1)
    anim.start(self)
    Clock.schedule_once(change_back, 1)

  def decide_actions(self, dt):
    if self.alive and self.main_character.alive:
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

  def damaged(self):
    super(GroundEnemy, self).damaged()
    if self.main_character.to_right:
      self.x += 200
    else:
      self.x -= 200
    self.source = self.sources[constants.DAMAGED]
    self.size = self.texture_size

  def return_to_normal(self, dt):
    if self.alive and self.main_character.alive:
      self.horse_man.moving = False
      self.horse_man.to_right = self.main_character.to_right
      if self.horse_man.to_right:
        self.horse_man.source = self.horse_man.sources[constants.STAND_RIGHT]
      else:
        self.horse_man.source = self.horse_man.sources[constants.STAND_LEFT]

  def check_life(self, dt):
    super(GroundEnemy, self).check_life(dt)
    if not self.alive:
      self.source = self.sources[constants.DEAD]
      self.size = self.texture_size
      Clock.unschedule(self.check_collisions)
      Clock.unschedule(self.decide_actions)

  def on_enter(self):
    super(GroundEnemy, self).on_enter()
    Clock.schedule_interval(self.check_collisions, 0)
    Clock.schedule_interval(self.decide_actions, .1)
    self.alive = True

  def reset(self):
    super(GroundEnemy, self).reset()
    self.x = constants.CHARACTER_STORAGE
    self.active = False
    if self.alive:
      Clock.unschedule(self.check_collisions)
      Clock.unschedule(self.decide_actions)

class WeakEnemy(Image):
  def __init__(self, source, dmg, speed, main_character, damaged_img, jumper=False, **kwargs):
    super(WeakEnemy, self).__init__(source=constants.WC_ROCK, x=constants.CHARACTER_STORAGE, y=constants.STANDING_Y)
    self.the_source = source
    self.dmg = dmg
    self.damaged_img = damaged_img
    self.speed = speed
    self.jumper = jumper
    self.jumping = False
    self.main_character = main_character
    self.attacking = False
    self.size = self.texture_size

  def attack_player(self, dt):
    if self.main_character.alive:
      if self.attacking and not self.main_character.on_battle:
        if self.x <= -self.width:
          self.reset()
        else:
          self.move_enemy()

  def damaged(self):
    if self.main_character.alive:
      self.source = self.damaged_img
      self.size = self.texture_size
      self.resetting = True
      self.x += 300
      Clock.schedule_once(self.reset_pend, 0.2)

  def check_collisions(self, dt):
    if self.main_character.alive:
      if self.collide_widget(self.main_character):
        if not self.main_character.attacking:
          self.main_character.life_meter.decrease_life(self.dmg)
          self.main_character.die_sounds[random.randint(0,1)].play()
          self.main_character.damaged()
          self.reset()
        else:
          self.main_character.taunt_sounds[random.randint(0,2)].play()
          self.damaged()
        self.move_enemy()

  def move_enemy(self):
    if self.main_character.alive:
      def change_back_from_jump(dt):
        self.jumping = False
      self.x -= self.speed
      if not self.jumping and self.jumper:
        self.jumping = True
        anim = Animation(y=constants.JUMP_HEIGHT + 100, duration=0.4) + Animation(y=constants.STANDING_Y, duration=0.4)
        anim.start(self)
        Clock.schedule_once(change_back_from_jump, random.randint(0,4))

  def on_enter(self):
    self.source = self.the_source
    self.size = self.texture_size
    Clock.schedule_interval(self.check_collisions, 0.1)
    Clock.schedule_interval(self.attack_player, 0)

  def on_leave(self):
    self.reset()
    Clock.unschedule(self.check_collisions)
    Clock.unschedule(self.attack_player)

  def reset_pend(self, dt):
    if self.main_character.alive:
      self.reset()

  def reset(self):
    self.x = constants.CHARACTER_STORAGE
    self.source = self.the_source
    self.size = self.texture_size
    self.attacking = False

class SoundedWeakEnemy(WeakEnemy):
  def __init__(self, source, dmg, speed, main_character, damaged_img, normal_sounds, die_sound, jumper=False, **kwargs):
    super(SoundedWeakEnemy, self).__init__(source, dmg, speed, main_character, damaged_img, jumper)
    self.normal_sounds = normal_sounds
    self.die_sound = die_sound

  def make_sound(self, dt):
    if self.main_character.alive:
      if self.attacking and not self.main_character.on_battle:
        random.choice(self.normal_sounds).play()

  def check_collisions(self, dt):
    if self.main_character.alive:
      if self.collide_widget(self.main_character) and self.main_character.attacking:
        self.die_sound.play()
      super(SoundedWeakEnemy, self).check_collisions(dt)

  def on_leave(self):
    super(SoundedWeakEnemy, self).on_leave()
    Clock.unschedule(self.make_sound)

  def on_enter(self):
    super(SoundedWeakEnemy, self).on_enter()
    Clock.schedule_interval(self.make_sound, 1)

class LifeMeter(ProgressBar):
  def __init__(self, **kwargs):
    super(LifeMeter, self).__init__(**kwargs)
    self.value = self.max
    self.width = self.max * 1.5

  def decrease_life(self, dmg):
    self.value -= dmg

  def reset(self):
    self.value = self.max
