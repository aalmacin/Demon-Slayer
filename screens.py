from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.image import Image
from parallax_bg import ParallaxBG
from characters import *
import constants
from kivy.app import App

 #the screen where the game actually takes place
class MainScreen(Screen):
  def __init__(self, **kwargs):
    super(MainScreen, self).__init__(**kwargs)
    self.background = ParallaxBG()
    self.character_manager = CharacterManager()
    #add background and character manager to main game screen
    self.add_widget(self.background)
    self.add_widget(self.character_manager)
    
  
  def on_enter(self):
    self.character_manager.on_enter()

  def on_leave(self):
    self.character_manager.on_leave()
    self.background.reset()
    
#main menu screen
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
    self.game_title = Label(text = "Demon Slayer")
    self.game_title.font_size = constants.LARGE_FNT_SIZE
    self.add_widget(self.game_title)
    self.game_title.pos = (-125,-25)
    #start button
    self.starter = Button(text=constants.START_MSG)
    self.add_widget(self.starter)
    self.starter.bind(on_press= self.start_btn_pressed)
    self.starter.size_hint = constants.SMALL_BTN_SIZE
    self.starter.font_size = constants.STANDARD_FNT_SIZE
    self.starter.pos = (1000,260)
    #how to play button, goes to different screen
    self.how_to_play = Button(text=constants.HOW_TO_MSG)
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
    self.quit.font_size = constants.STANDARD_FNT_SIZE
    self.quit.pos = (1000,100)
  #when start button pressed
  def start_btn_pressed(self, instance):
    self.parent.current = constants.DIFFICULTY_SCREEN
  #when how_to_play button pressed
  def how_to_play_btn_pressed(self, instance):
    self.parent.current = constants.INSTRUCTION_SCREEN
  #when quit button pressed
  def quit_btn_pressed(self, instance):
    App.get_running_app().stop() #stop app
    
#instruction screen
class InstructionScreen(Screen):
  def __init__(self, **kwargs):
    super(InstructionScreen, self).__init__(**kwargs)
    #background
    self.bg = Image(source=constants.NIGHT_BG)
    self.bg.size = self.bg.texture_size
    self.add_widget(self.bg)
    self.cloud_1 = Image(source = constants.CLOUD_LEFT_BG)
    self.cloud_1.size = self.bg.texture_size
    self.add_widget(self.cloud_1)
    #instructions
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
  #when go back btton pressed
  def go_back_btn_pressed(self, instance):
    self.parent.current = constants.START_SCREEN
    
#the screen when the user gets game over
class GameOverScreen(Screen):
  def __init__(self, **kwargs):
    super(GameOverScreen, self).__init__(**kwargs)
    #background
    self.bg = Image(source=constants.NIGHT_BG)
    self.bg.size = self.bg.texture_size
    self.add_widget(self.bg)
    self.cloud_1 = Image(source = constants.CLOUD_LEFT_BG)
    self.cloud_1.size = self.bg.texture_size
    self.add_widget(self.cloud_1)
    #play again button
    self.play_again_btn = Button(text=constants.GAME_OVER_MSG)
    self.add_widget(self.play_again_btn)
    self.play_again_btn.bind(on_press= self.play_again_btn_pressed)
    self.play_again_btn.size_hint = constants.SMALL_BTN_SIZE
    self.play_again_btn.font_size = constants.STANDARD_FNT_SIZE
    self.play_again_btn.pos = (1000,260)
    #go back button
    self.go_back = Button(text=constants.GO_BACK_MSG)
    self.add_widget(self.go_back)
    self.go_back.bind(on_press= self.go_back_btn_pressed)
    self.go_back.size_hint = constants.SMALL_BTN_SIZE
    self.go_back.font_size = constants.STANDARD_FNT_SIZE
    self.go_back.pos = (1000,180)
    #quit quits game
    self.quit = Button(text=constants.QUIT_GAME_MSG)
    self.add_widget(self.quit)
    self.quit.bind(on_press= self.quit_btn_pressed)
    self.quit.size_hint = constants.SMALL_BTN_SIZE
    self.quit.font_size = constants.STANDARD_FNT_SIZE
    self.quit.pos = (1000,100)

    self.final_score = Label(font_size="100px", text="[color=E01B5D]" + constants.FINAL_SCORE_TEXT + "----[/color]", markup=True)
    self.add_widget(self.final_score)
    
  #display final score in specified colour
  def on_enter(self):
    self.final_score.text = "[color=E01B5D]" + constants.FINAL_SCORE_TEXT + str(self.parent.final_score) + "[/color]"
    self.x = (constants.WIDTH/2) - (self.final_score.width/2)
    self.y = (constants.HEIGHT/2) - (self.final_score.height/2)

#when restart button is pressed
  def play_again_btn_pressed(self, instance):
    self.parent.current = constants.MAIN_SCREEN
  #when go back btton pressed
  def go_back_btn_pressed(self, instance):
    self.parent.current = constants.START_SCREEN
  #when quit button pressed
  def quit_btn_pressed(self, instance):
    App.get_running_app().stop() #stop app
    
#screen to choose difficulty
class DifficultyScreen(Screen):
  def __init__(self, **kwargs):
    super(DifficultyScreen, self).__init__(**kwargs)
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
    self.game_title = Label(text = "Demon Slayer")
    self.game_title.font_size = constants.LARGE_FNT_SIZE
    self.add_widget(self.game_title)
    self.game_title.pos = (-125,-25)
    #easy button
    self.easy_choice = Button(text="Easy")
    self.add_widget(self.easy_choice)
    self.easy_choice.bind(on_press= self.easy_btn_pressed)
    self.easy_choice.size_hint = constants.SMALL_BTN_SIZE
    self.easy_choice.font_size = constants.STANDARD_FNT_SIZE
    self.easy_choice.pos = (1000,260)
    #medium button
    self.medium_choice = Button(text="Medium")
    self.add_widget(self.medium_choice)
    self.medium_choice.bind(on_press= self.medium_btn_pressed)
    self.medium_choice.size_hint = constants.SMALL_BTN_SIZE
    self.medium_choice.font_size = constants.STANDARD_FNT_SIZE
    self.medium_choice.pos = (1000,180)
   #hard button
    self.hard_choice = Button(text="Hard")
    self.add_widget(self.hard_choice)
    self.hard_choice.bind(on_press= self.hard_btn_pressed)
    self.hard_choice.size_hint = constants.SMALL_BTN_SIZE
    self.hard_choice.font_size = constants.STANDARD_FNT_SIZE
    self.hard_choice.pos = (1000,100)
    #go back button
    self.go_back = Button(text=constants.GO_BACK_MSG, font_size=constants.SMALL_FNT_SIZE)
    self.add_widget(self.go_back)
    self.go_back.bind(on_press= self.go_back_btn_pressed)
    self.go_back.size_hint = constants.SMALL_BTN_SIZE
    self.go_back.font_size = constants.STANDARD_FNT_SIZE
    self.go_back.pos = (1000,20)
  #when go back btton pressed
  def go_back_btn_pressed(self, instance):
    self.parent.current = constants.START_SCREEN
  #when start button pressed
  def easy_btn_pressed(self, instance):
    self.parent.difficulty = constants.DIFFICULTY_EASY
    self.parent.current = constants.MAIN_SCREEN
  #when how_to_play button pressed
  def medium_btn_pressed(self, instance):
    self.parent.difficulty = constants.DIFFICULTY_MEDIUM
    self.parent.current = constants.MAIN_SCREEN
  #when quit button pressed
  def hard_btn_pressed(self, instance):
    self.parent.difficulty = constants.DIFFICULTY_HARD
    self.parent.current = constants.MAIN_SCREEN
