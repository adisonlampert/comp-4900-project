from player import Player
from itertools import combinations, permutations
from constants import Orientation
from tile import Tile

class SimplifiedPlayer(Player):
  def __init__(self):
    super().__init__()
    self.rack = []

  def play(self, board):
    highest_score = 0
    highest_equation = []
    tile = None

    for yPos in range(19):
      for xPos in range(19): 

        tile = board.getTile(xPos, yPos)

        if tile is None or not tile.isPlayable():
          continue

        tile_orientation = tile.getOrientation()
        play_space = self.generate_play_space(tile)
    
        for i in range(1, len(play_space) - 1):

          temp_list = play_space.copy()
          temp_list[i] = Tile("=", 0)

          for length in range(3, len(play_space) + 1):
              for start in range(len(play_space) - length + 1):
                  end = start + length
                  sliced_list = temp_list[start:end]
                  
                  eq, tt, ds, dist = False, False, False, 0
                  for t in sliced_list:
                    if t != None:
                      if t.getValue() == "=":
                        eq = True
                        if not ds:
                          ds = True
                        else:
                          dist += 1
                      elif t.getValue() == tile.getValue():
                        tt = True
                        if not ds:
                          ds = True
                        else:
                          dist += 1
                      
                      if tt and eq:
                        break
                    
                  if not eq or not tt or (sliced_list[0] != None and sliced_list[0].getValue() == "=") or (sliced_list[-1] != None and sliced_list[-1].getValue() == "="):
                    break

                  # find all indices to permute over
                  none_indices = [index for index, value in enumerate(sliced_list) if value is None]
                  for r in range(1, len(self.rack) + 1):
                      for comb in combinations(self.rack, r):
                          for perm in permutations(comb, r):
                              temp_sliced_list = sliced_list.copy()
                              for idx, val in zip(none_indices, perm):
                                  temp_sliced_list[idx] = val
                              # exclude any equations that have None in between two non-None values
                              if all(temp_sliced_list.index(None) in [0, len(temp_sliced_list) - 1] for _ in range(temp_sliced_list.count(None))):
                                temp_score = 0
                                for j in range(len(temp_sliced_list)):
                                    if temp_sliced_list[j] is not None:
                                        temp_score += temp_sliced_list[j].getPoints()
                                if temp_score > highest_score:
                                    if super().validatePlay(temp_sliced_list):
                                      highest_score = temp_score
                                      highest_equation = temp_sliced_list

    for i in range(len(highest_equation)):
      if highest_equation[i] is not None:
        self.rack.remove(highest_equation[i])

    # set tile orientation and coordinates
    returnValue = []
    tile_index = None
    for i, current_tile in enumerate(highest_equation):
        if current_tile is not None and current_tile.getOrientation() == tile_orientation:
            tile_index = i
            break

    for i, current_tile in enumerate(highest_equation):
        if current_tile is not None:
            if tile_orientation == 'horizontal':
                x_coord = xPos + (i - tile_index)
                y_coord = yPos
                current_tile.setOrientation(Orientation.VERTICAL)
            else:
                x_coord = xPos
                y_coord = yPos + (i - tile_index)
                current_tile.setOrientation(Orientation.HORIZONTAL)
            returnValue.append((current_tile, (y_coord, x_coord)))

    return returnValue
              
  def generate_play_space(self, tile):
    playSpace = []
    for i in range(tile.getBefore()):
      playSpace.append(None)
    playSpace.append(tile)
    for i in range(tile.getAfter()):
      playSpace.append(None)
    return playSpace