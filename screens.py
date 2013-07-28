from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from parallax_bg import ParallaxBG
from characters import *
import constants

class MainScreen(Screen):
  def __init__(self, **kwargs):
    super(MainScreen, self).__init__(**kwargs)
    self.background = ParallaxBG()
    self.character_manager = CharacterManager()

    self.add_widget(self.background)
    self.add_widget(self.character_manager)

  def on_leave(self):
    self.character_manager.reset()
    self.background.reset()

class StartScreen(Screen):
  def __init__(self, **kwargs):
    super(StartScreen, self).__init__(**kwargs)
    self.starter = Button(text=constants.START_MSG)
    self.add_widget(self.starter)
    self.starter.bind(on_press= self.btn_pressed)

  def btn_pressed(self, instance):
    self.parent.current = constants.MAIN_SCREEN

class GameOverScreen(Screen):
  def __init__(self, **kwargs):
    super(GameOverScreen, self).__init__(**kwargs)
    self.restarter = Button(text=constants.GAME_OVER_MSG)
    self.add_widget(self.restarter)
    self.restarter.bind(on_press= self.btn_pressed)

  def btn_pressed(self, instance):
    self.parent.current = constants.MAIN_SCREEN
