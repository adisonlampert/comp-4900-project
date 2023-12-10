from copy import deepcopy
from constants import BOARD_SIZE

class Board:
  def __init__(self):
    self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

  def add_tile(self, tile, x_pos, y_pos):
    self.board[y_pos][x_pos] = deepcopy(tile)

  def get_tile(self, x_pos, y_pos):
    return self.board[y_pos][x_pos]
  
  def update_tile_before(self, x_pos, y_pos, before):
    self.board[y_pos][x_pos].set_before(before)
  
  def update_tile_after(self, x_pos, y_pos, after):
    self.board[y_pos][x_pos].set_after(after)
    
  def __str__(self):
    pr = ""
    format = []
    for i in range(19):
      format.append([])
      for j in range(19):
        tile = self.get_tile(j,i)
        if tile != None:
          format[i].append(tile.get_value())
        else:
          format[i].append("")
          
    mx = max((len(str(ele)) for sub in format for ele in sub))
    i = 0
    
    for row in format:
      pr += f'{"|".join(["{:<{mx}}".format(ele,mx=mx) for ele in row])} {i}\n'
      i += 1
      
    return pr