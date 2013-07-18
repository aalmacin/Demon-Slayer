from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from parallax_bg import ParallaxBG

class MainScreen(Screen):
  def __init__(self, **kwargs):
    super(MainScreen, self).__init__(**kwargs)
    self.background = ParallaxBG()
    self.main_character = MainCharacter()

    self.add_widget(self.background)
    self.add_widget(self.main_character)

class StartScreen(Screen):
  def __init__(self, **kwargs):
    super(StartScreen, self).__init__(**kwargs)
    self.starter = Button(text="Click anywhere to start game")
    self.add_widget(self.starter)
    self.starter.bind(on_press= self.btn_pressed)

  def btn_pressed(self, instance):
    self.parent.current = "main_screen"

class GameOverScreen(Screen):
  def __init__(self, **kwargs):
    super(GameOverScreen, self).__init__(**kwargs)
    self.restarter = Button(text="Click anywhere to play again")
    self.add_widget(self.restarter)
    self.restarter.bind(on_press= self.btn_pressed)

  def btn_pressed(self, instance):
    self.parent.current = "main_screen"

class MainCharacter(Widget):
  def __init__(self, **kwargs):
    super(MainCharacter, self).__init__(**kwargs)

    self.main_char_img = Image(source="images/Skater.png")
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
    if keycode[1] == "w":
      self.main_char_img.source = "images/Skater2.zip"
      self.moving = True
    elif keycode[1] == "s":
      self.main_char_img.source = "images/Skater.zip"
      self.moving = True

  def _on_keyboard_up(self, keyboard, keycode):
    if keycode[1] == "w":
      self.main_char_img.source = "images/Skater.png"
      self.moving = False
    elif keycode[1] == "s":
      self.main_char_img.source = "images/Skater.png"
      self.moving = False
