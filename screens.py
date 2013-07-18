from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window

class MainScreen(Screen):
  pass

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
    self.running = Image(source="images/Skater.png", pos=(50,100), size=(100, 200))
    self.attacking = Image(source="images/SkaterJump.png", pos=(50,100), size=(100, 200))
    self.got_hit = Image(source="images/SkaterSitting.png", pos=(50,100), size=(200, 100))

    self.root = Widget()
    self.is_running()

    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)


  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard = None

  def is_running(self):
    self.current_img = self.running
    self.add_current_img()

  def is_attacking(self):
    self.current_img = self.attacking
    self.add_current_img()

  def is_got_hit(self):
    self.current_img = self.got_hit
    self.add_current_img()

  def add_current_img(self):
    self.root.clear_widgets()
    self.root.add_widget(self.current_img)
    self.add_widget(self.root)

  def on_touch_down(self, touch):
    print "touched"
    return super(MainCharacter, self).on_touch_down(touch)

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == "w":
      print "hey"
