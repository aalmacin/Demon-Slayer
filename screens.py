from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from parallax_bg import ParallaxBG
from main_character import MainCharacter

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