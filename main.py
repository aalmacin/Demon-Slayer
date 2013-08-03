import kivy
kivy.require("1.0.9")

from kivy.config import Config
Config.set('graphics','resizable',0)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.atlas import Atlas
from kivy.uix.image import Image
from kivy.factory import Factory

from parallax_bg import *
from screens import *
from kivy.uix.screenmanager import *
from kivy.base import EventLoop
import constants

class DemonSlayer(ScreenManager):
  def __init__(self, transition):
    super(ScreenManager, self).__init__(transition=transition)
    self.difficulty = constants.DIFFICULTY_EASY
    self.final_score = 0

    self.start_screen = StartScreen(name=constants.START_SCREEN)
    self.game_over_screen = GameOverScreen(name=constants.GAME_OVER_SCREEN)
    self.main_screen = MainScreen(name=constants.MAIN_SCREEN)
    self.instruction_screen = InstructionScreen(name=constants.INSTRUCTION_SCREEN)
    self.difficulty_screen = DifficultyScreen(name=constants.DIFFICULTY_SCREEN)

    self.add_widget(self.start_screen)
    self.add_widget(self.game_over_screen)
    self.add_widget(self.main_screen)
    self.add_widget(self.instruction_screen)
    self.add_widget(self.difficulty_screen)

class DemonSlayerApp(App):
  def build(self):
    EventLoop.ensure_window()
    self.window = EventLoop.window
    self.window.size = (constants.WIDTH, constants.HEIGHT)
    return DemonSlayer(transition= FadeTransition())

if __name__ == "__main__":
  DemonSlayerApp().run()
