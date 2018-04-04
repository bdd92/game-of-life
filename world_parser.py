''' world parser: transforms string inputs in a set of cell coordinates
    * = alive cell
    . = dead cell
'''

import random

worlds = {
  "random": "random",
  "blinker": "***" ,
  "10 cell row": "**********",
  "exploder": "*.*.*\n*...*\n*...*\n*...*\n*.*.*",
  "spaceship": ".****\n*...*\n....*\n*..*.",
  "tumbler": ".**.**\n.**.**\n..*.*..\n*.*.*.*\n*.*.*.*\n**...**",
  "small exploder" : ".*.\n***\n*.*\n.*.",
  "glider": ".*.\n..*\n***",
  "switch": ".*.*\n*\n.*..*\n...***",
  "gosper glider gun": "........................*\n"
                       "......................*.*\n"
                       "............**......**............**\n"
                       "...........*...*....**............**\n"
                       "**........*.....*...**\n"
                       "**........*...*.**....*.*\n"
                       "..........*.....*.......*\n"
                       "...........*...*\n"
                       "............**",
  "clear" : ""} 

#return  world names
def get_world_names():
  return list(worlds.keys())

# transform the world string into coordinates
def get_world(text, offset = (15,25)):
  cells = set()
  world = worlds[text]
  if world == "random":
    return get_random_coord()
  else:
    if text == "gosper glider gun":
      offset = (10, 10)
    for (x,line) in enumerate(world.splitlines()):
      for (y, char) in enumerate(line):
        if char == '*': 
          cells.add((x + offset[0],y + offset[1]))    
  return cells

#return  100 random points
def get_random_coord():
  coord = set()
  for i in range(100):
    point = (random.choice(range(40)), random.choice(range(55)))
    if point not in coord:
      coord.add(point)
  return coord


