from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.config import Config
from collections import Counter
from world_parser import *


# world: set representing the world of living cells;
# each alive cell is a (x, y) pair of integer coordinates on the grid.
# If a cell borns, it is added to the world; if a cell dies, it is removed from the world.

world =  set()

# model representing the single cell
class Cell(Widget):

  # Numeric Property representing age of the Cell (dead: age = 0) 
  age = NumericProperty(0) 

  def __init__(self, x, y ,**kwargs):
    super().__init__(**kwargs)
    self.x_grid = x
    self.y_grid = y
  
  # click event : changes cell from dead to alive or viceversa
  def on_touch_down(self, touch):

    if self.collide_point(*touch.pos): 
      if self.age == 0:
        self.age = 1
      else:
        self.age = 0
      
      
      if self.age == 1:
        #add cell coordinates to the world
        world.add((self.x_grid, self.y_grid))

      else:
        #remove cell coordinates from the world
        world.remove((self.x_grid, self.y_grid))
 
  # mouse motion event:  draw pattern of alive cells on the grid
  def on_touch_move(self, touch): 
      if self.collide_point(*touch.pos):
        if(self.age == 0):
          self.age = 1
          world.add((self.x_grid, self.y_grid))

  
  # callback event on the age property: the cell is cleared and redesigned as a rectangle canvas,
  # updating the color according to its age
  def on_age(self, instance, value):
    self.canvas.clear()
    
    # age >=1 :  cell is alive
    if value >= 1:

      color = self.get_color(self.age);
      with self.canvas:
        Color(color[0],color[1], color[2]) 
        Rectangle(size = self.size, pos = self.pos)

    # age = 0 :  cell is dead
    else:
       with self.canvas:
        Color(0.5, 0.5, 0.5) #grey
        Rectangle(size = self.size, pos = self.pos)

  # linear color interpolation from blue to red, reflecting the age of the cell
  def get_color(self, age):
    minimum = 0
    maximum = 10
    ratio = 2 * (age-minimum) / (maximum - minimum)
    blue = max(0,  1-ratio)
    red = max(0, ratio-1)
    green = 0
    return (red ,green , blue) 

  # increase age of cell for the next generation
  def grow(self):
    self.age += 1

  # kill the cell
  def die(self):
    self.age = 0

# class of the Grid of cells, each cell is visualized as a rectangle canvas 
class Grid(GridLayout):
  
  # number of iterations 
  steps = NumericProperty(0) 
  
  # clear the grid
  def clear(self):
    for cell in self.children:
      cell.die()

  # build the cell grid when the app starts
  def add_cells(self):
    for i in range(self.rows):
      for j in range(self.cols):
        self.add_widget(Cell(i,j))

  # create the next generation of the world according to the rules;
  # the new born cells are added to the world, while the dead cells in this generation are removed
  def next_generation(self, dt= 1):
    candidates = self.get_counts()
    dead_cells = set()
    for cell in candidates:
      if cell in world:
        if candidates[cell] != 2 and  candidates[cell] != 3 :
          dead_cells.add(cell)
          world.remove(cell)
      elif candidates[cell] == 3:
        world.add(cell)

    # remove remaining cells in world that are not in candidates (isolated cells with no alive neighbor)
    isolated = world.difference(candidates)
    if( len(isolated)>0):
      for cell in isolated:
          world.remove(cell)
          dead_cells.add(cell)

    self.evolve(dead_cells)
    self.steps += 1
  
 # get_counts returns a dictionary {(x,y): count} , where:
 #  - (x,y) are the  possible cells that could be added  to the world in the next generation;
 #  - count is the number of living neighbors of (x, y)
  def get_counts(self):

    # counts[(x,y)] represent the number of living neighbors  of the (x,y) cell
    counts = {}
    for cell in world:
      for nb in self.neighborhood(cell):
        if nb not in counts:
          counts[nb] = 1
        else:
          counts[nb] += 1

    return counts

  # returns the neighborhood of the cell
  def neighborhood(self, cell): 
    (x,y) = cell
    return [(x-1, y-1), (x, y-1), (x+1, y-1),
            (x-1, y),             (x+1, y),
            (x-1, y+1), (x, y+1), (x+1, y+1)]


  # update the age of the cells according to the new generation in the world, and kill the dead cells 
  def evolve(self, dead_cells= set()):
    n = self.rows * self.cols
    for cell in world: 
      if(cell >= (0,0) and cell < (self.rows, self.cols)):
        #reflexing indices because kivy saves widget in the GridLayout from bottom right to top left 
        self.children[n-1-(cell[0] * self.cols + cell[1])].grow() 

    for cell in dead_cells: 
      if(cell >= (0,0) and cell < (self.rows, self.cols)): 
        self.children[n-1-(cell[0] * self.cols + cell[1])].die()

    if len(world) == 0 : Clock.unschedule(self.next_generation)



