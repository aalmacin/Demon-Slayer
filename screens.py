from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.button import Label
from parallax_bg import ParallaxBG
from characters import *
import constants
from kivy.app import App

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
    #self.background = ParallaxBG()
    
    #temp background, would like to use same paralax as in main loop, have it run in main, 
    #over top of all other loops(game, menu, game over etc)
    self.bg = Image(source=constants.NIGHT_BG)
    self.bg.size = self.bg.texture_size
    self.add_widget(self.bg)
    self.cloud_1 = Image(source = constants.CLOUD_LEFT_BG)
    self.cloud_1.size = self.bg.texture_size
    self.add_widget(self.cloud_1)
    #title
    self.game_title = Label(text = "Demon Slayer", font_size = constants.LARGE_FNT_SIZE)
    self.add_widget(self.game_title)
    self.game_title.pos = (-125,-25)
    #start button   
    self.starter = Button(text=constants.START_MSG, font_size=14)
    self.add_widget(self.starter)
    self.starter.bind(on_press= self.start_btn_pressed)
    self.starter.size_hint = constants.SMALL_BTN_SIZE
    self.starter.font_size = constants.STANDARD_FNT_SIZE
    self.starter.pos = (1000,260)
    #how to play button, goes to different screen
    self.how_to_play = Button(text=constants.HOW_TO_MSG, font_size=14)
    self.add_widget(self.how_to_play)
    self.how_to_play.bind(on_press= self.how_to_play_btn_pressed)
    self.how_to_play.size_hint = constants.SMALL_BTN_SIZE
    self.how_to_play.font_size = constants.STANDARD_FNT_SIZE
    self.how_to_play.pos = (1000,180)
   #quit quits game
    self.quit = Button(text=constants.QUIT_GAME_MSG)
    self.add_widget(self.quit)
    self.quit.bind(on_press= self.quit_btn_pressed)
    self.quit.size_hint = constants.SMALL_BTN_SIZE
    self.quit.font_size = constants.SMALL_FNT_SIZE
    self.quit.pos = (1000,100)
    
  def start_btn_pressed(self, instance):
    self.parent.current = constants.MAIN_SCREEN
    
  def how_to_play_btn_pressed(self, instance):
    self.parent.current = constants.INSTRUCTION_SCREEN
    
  def quit_btn_pressed(self, instance):
    App.get_running_app().stop()
    
class InstructionScreen(Screen):
  def __init__(self, **kwargs):
    super(InstructionScreen, self).__init__(**kwargs)
    self.bg = Image(source=constants.NIGHT_BG)
    self.bg.size = self.bg.texture_size
    self.add_widget(self.bg)
    self.cloud_1 = Image(source = constants.CLOUD_LEFT_BG)
    self.cloud_1.size = self.bg.texture_size
    self.add_widget(self.cloud_1)
    self.instructions = Label(text = "D - move right.\n"+
                                     "A - move left.\n"+
                                     "W - Jump.\n"+
                                     "Left Click to swing sword.\n"+
                                     "Kill the enemies with your sword when they get in range.\n"+
                                     "If they hit you you will take damage.\n"+
                                      "jump over the rocks or you will take damage.""\n"+"\n"+ "Good Luck!", font_size = constants.STANDARD_FNT_SIZE) 
    self.add_widget(self.instructions)
    self.instructions.pos = (-315,-155)
    #go back button
    self.go_back = Button(text=constants.GO_BACK_MSG)
    self.add_widget(self.go_back)
    self.go_back.bind(on_press= self.go_back_btn_pressed)
    self.go_back.size_hint = constants.SMALL_BTN_SIZE
    self.go_back.font_size = constants.STANDARD_FNT_SIZE
    self.go_back.pos = (1000,180)
   
  def go_back_btn_pressed(self, instance):
    self.parent.current = constants.START_SCREEN

class GameOverScreen(Screen):
  def __init__(self, **kwargs):
    super(GameOverScreen, self).__init__(**kwargs)
    self.restarter = Button(text=constants.GAME_OVER_MSG)
    self.add_widget(self.restarter)
    self.restarter.bind(on_press= self.play_again_btn_pressed)

  def play_again_btn_pressed(self, instance):
    self.parent.current = constants.MAIN_SCREEN
