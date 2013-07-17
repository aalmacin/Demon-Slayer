from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

class MainScreen(Screen):
  pass

class StartScreen(Screen):
  def __init__(self, **kwargs):
    super(StartScreen, self).__init__()
    self.starter = Button(text="Click anywhere to start game")
    self.add_widget(self.starter)
    self.starter.bind(on_press= self.btn_pressed)

  def btn_pressed(self, instance):
    self.parent.current = "main_screen"

class GameOverScreen(Screen):
  def __init__(self, **kwargs):
    super(GameOverScreen, self).__init__()
    self.restarter = Button(text="Click anywhere to play again")
    self.add_widget(self.restarter)
    self.restarter.bind(on_press= self.btn_pressed)

  def btn_pressed(self, instance):
    self.parent.current = "main_screen"
