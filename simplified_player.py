from player import Player
from itertools import combinations, permutations
from constants import Orientation
from tile import Tile

class SimplifiedPlayer(Player):
  def __init__(self):
    super().__init__()

  def play(self, board):
    highest_score = 0
    highest_equation = []
    tile = None

    for y_pos in range(19):
      for x_pos in range(19): 

        tile = board.getTile(x_pos, y_pos)

        if tile is None or not tile.isPlayable():
          continue

        tile_orientation = tile.getOrientation()
        play_space = self.generate_play_space(tile)
    
        for i in range(1, len(play_space) - 1):
          b_type = play_space[i-1].getType() if play_space[i-1] is not None else None
          a_type = play_space[i+1].getType() if play_space[i+1] is not None else None

          if play_space[i] is not None or (b_type is "operator" or b_type is "negative") or a_type is "operator":
            continue

          temp_list = play_space.copy()
          temp_list[i] = Tile("=", 0, "equals")
          possibleArrangements = []
          print("New arrangement: ", [str(obj) for obj in temp_list])

          # Equal before tile
          # i is the position of the = sign
          # len(temp_list) - tile.getAfter() is the position of the tile
          if i < len(temp_list) - tile.getAfter():
            for j in range(0, i):
              for k in range(len(temp_list) - tile.getAfter(), len(temp_list)+1):
                # print([str(obj) for obj in temp_list[j:k]])
                possibleArrangements.append(temp_list[j:k])
          else:
            for j in range(0, len(temp_list) - tile.getAfter()):
              for k in range(i+2, len(temp_list)+1):
                # print([str(obj) for obj in temp_list[j:k]])
                possibleArrangements.append(temp_list[j:k])
          
          for pa in possibleArrangements: 
            for 


          

    # for i in range(len(highest_equation)):
    #   if highest_equation[i] is not None:
    #     self.rack.remove(highest_equation[i])

    # # set tile orientation and coordinates
    # returnValue = []
    # tile_index = None
    # for i, current_tile in enumerate(highest_equation):
    #     if current_tile is not None and current_tile.getOrientation() == tile_orientation:
    #         tile_index = i
    #         break

    # for i, current_tile in enumerate(highest_equation):
    #     if current_tile is not None:
    #         if tile_orientation == 'horizontal':
    #             x_coord = xPos + (i - tile_index)
    #             y_coord = yPos
    #             current_tile.setOrientation(Orientation.VERTICAL)
    #         else:
    #             x_coord = xPos
    #             y_coord = yPos + (i - tile_index)
    #             current_tile.setOrientation(Orientation.HORIZONTAL)
    #         returnValue.append((current_tile, (y_coord, x_coord)))

    # return returnValue
              
  def generate_play_space(self, tile):
    playSpace = []
    before = min(tile.getBefore(), 10)
    for i in range(before):
      playSpace.append(None)
    playSpace.append(tile)
    after = min(tile.getAfter(), 10)
    for i in range(after):
      playSpace.append(None)
    return playSpace
  
  def getPlayableTiles(self, before = None, after = None):
    playableTiles = []
    match (before.getType() if before is not None else None, after.getType() if after is not None else None):
      case ("operator", "operator"):
        return self.integers + self.fractions
      case ("operator", "negative"):
        return self.integers + self.fractions
      case ("operator", "integer"):
        return self.integers + self.negatives
      case ("operator", "fraction"):
        return self.integers + self.negatives
      case ("operator", "equals"):
        return self.integers + self.fractions
      case ("operator", None):
        return self.integers + self.fractions + self.negatives
      case ("negative", "operator"):
        return self.integers + self.fractions
      case ("negative", "negative"):
        return self.integers + self.fractions
      case ("negative", "integer"):
        return self.integers
      case ("negative", "fraction"):
        return self.integers
      case ("negative", "equals"):
        return self.integers + self.fractions
      case ("negative", None):
        return self.integers + self.fractions
      case ("integer", "operator"):
        return self.integers + self.fractions
      case ("integer", "negative"):
        return self.integers + self.fractions
      case ("integer", "integer"):
        return self.integers + self.negatives + self.operators
      case ("integer", "fraction"):
        return self.integers + self.negatives + self.operators
      case ("integer", "equals"):
        return self.integers + self.fractions
      case ("integer", None):
        return self.integers + self.fractions + self.negatives + self.operators
      case ("fraction", "operator"):
        return []
      case ("fraction", "negative"):
        return self.operators
      case ("fraction", "integer"):
        return self.operators + self.negatives
      case ("fraction", "fraction"):
        return self.operators + self.negatives
      case ("fraction", "equals"):
        return []
      case ("fraction", None):
        return self.operators + self.negatives
      case ("equals", "operator"):
        return self.integers + self.fractions
      case ("equals", "negative"):
        return self.integers + self.fractions
      case ("equals", "integer"):
        return self.integers + self.negatives
      case ("equals", "fraction"):
        return self.integers + self.negatives
      case ("equals", None):
        return self.integers + self.fractions + self.negatives