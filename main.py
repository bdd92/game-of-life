from kivy.lang import Builder
from kivy.app import App
from kivy.config import Config

import controller

class GameApp(App):
  def build(self):

    # set fixed window size 
    Config.set('graphics', 'width', 1000)
    Config.set('graphics', 'height', 700)
    Config.set('graphics', 'resizable', 0)

    #start game and build grid of cells
    game = controller.Game()
    game.grid.add_cells()

    return game

if __name__ == "__main__":
  GameApp().run() 
