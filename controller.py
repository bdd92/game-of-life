from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from collections import Counter
from world_parser import *
import model


# game controller, also the root object
class Game(BoxLayout):

  grid = ObjectProperty(None)
  fps = 1 
  is_running = False

  # start iterations , updates world according to fps
  def start(self):
    self.is_running = True
    if len(model.world) > 0:
      Clock.schedule_interval(self.grid.next_generation, self.fps)
   
  # pause current iteration
  def pause(self):
    self.is_running = False
    Clock.unschedule(self.grid.next_generation)
  
  # reset current iteration and clears grid and world
  def reset(self):
    self.pause()
    model.world.clear() 
    self.grid.clear()
    self.grid.steps = 0
  
  # changes fps to the input value
  def change_fps(self, *args):
    self.fps = float('%.3f'%(1/args[1]))       
    if self.is_running:
      self.pause()
      self.start()
  
  # loads the world selected by the user
  def spinner_clicked(self, text):
    self.reset()
    if (text != "clear"):
      for cell in get_world(text):
        model.world.add(cell)
     
      self.grid.evolve()

  # returns the world names for display
  def get_names(self):
      return get_world_names() 