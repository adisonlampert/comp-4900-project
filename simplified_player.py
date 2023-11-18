import math
from player import Player
from itertools import combinations, permutations
from constants import Orientation
from tile import Tile

class SimplifiedPlayer(Player):
  def __init__(self):
    super().__init__()

  def play(self, board):
    highestPlay = []
    tile = None
    
    result = []
    locations = []

    for yPos in range(19):
      for xPos in range(19): 

        tile = board.getTile(xPos, yPos)

        if tile is None or not tile.isPlayable():
          continue
        
        placeSpace = self.generate_play_space(tile)
        
        for i in range(1, len(placeSpace) - 1):
          b_type = placeSpace[i-1].getType() if placeSpace[i-1] is not None else None
          a_type = placeSpace[i+1].getType() if placeSpace[i+1] is not None else None

          if placeSpace[i] is not None or (b_type == "operator" or b_type == "negative") or a_type == "operator":
            continue

          temp_list = placeSpace.copy()
          temp_list[i] = Tile("=", 0, "equals")
          possibleArrangements = []

          space =  False
          if tile.getType() == "operator":
            space =  True
            
          if i < len(temp_list) - tile.getAfter():
            for j in range(0, i):
              sRange = len(temp_list) - tile.getAfter() if not space else len(temp_list) - tile.getAfter()+1
              for k in range(sRange, len(temp_list)+1):
                possibleArrangements.append(temp_list[j:k])
          else:
            eRange = len(temp_list) - tile.getAfter() if not space else len(temp_list) - tile.getAfter()-1
            for j in range(0, eRange):
              for k in range(i+2, len(temp_list)+1):
                possibleArrangements.append(temp_list[j:k])
          
          for pa in possibleArrangements:
            integers, fractions, negatives, operators = self.integers.copy(), self.fractions.copy(), self.negatives.copy(), self.operators.copy()
            
            none_indices = [i for i, x in enumerate(pa) if x is None]
            
            def generate_partial_equations(current_equation, remaining_none_indices, integers, fractions, negatives, operators):
              if not remaining_none_indices:
                # If there are no remaining None indices, check if the equation is valid
                result.append(current_equation.copy())
                locations.append((xPos, yPos))
                return

              # Get the next None index to fill
              next_none_index = remaining_none_indices[0]

              # Get playable tiles for the current position
              before = current_equation[next_none_index-1] if next_none_index-1 >= 0 else None
              after = current_equation[next_none_index+1] if next_none_index+1 < len(current_equation) else None
              
              if next_none_index == len(current_equation)-1:
                playable_tiles = self.getPlayableTiles(integers, fractions, negatives, operators, before=before, after=after, last=True)
              else:
                playable_tiles = self.getPlayableTiles(integers, fractions, negatives, operators, before=before, after=after)
              
              if len(playable_tiles) == 0:
                return

              # Generate permutations for the remaining None indices
              for tile in playable_tiles:
                  current_equation[next_none_index] = tile
                  if tile in integers:
                    integers.remove(tile)
                  elif tile in fractions:
                    fractions.remove(tile)
                  elif tile in negatives:
                    negatives.remove(tile)
                  else:
                    operators.remove(tile)
                  generate_partial_equations(current_equation, remaining_none_indices[1:], integers.copy(), fractions.copy(), negatives.copy(), operators.copy())
                  current_equation[next_none_index] = None  # Backtrack

            # Start the recursive generation process
            generate_partial_equations(pa.copy(), none_indices, integers, fractions, negatives, operators)

    validEquations = []
    for r in result:
      if super().validatePlay(r):
        validEquations.append(r)
    
    highestPlay, highestPoints, coords = [], 0, (0,0)
    for index, r in enumerate(validEquations): 
      points = 0
      for t in r:
        points += t.getPoints()

      if points > highestPoints:
        highestPoints = points
        highestPlay = r
        coords = locations[index]

    orientation, tileIndex = None, 0
    
    for i in range(len(highestPlay)):
      if not highestPlay[i].getOrientation():
        match highestPlay[i].getType():
          case "integer":
            self.integers.remove(highestPlay[i])
          case "fraction":
            self.fractions.remove(highestPlay[i])
          case "operator":
            self.operators.remove(highestPlay[i])
          case "negative":
            self.negatives.remove(highestPlay[i])
      else:
        orientation = highestPlay[i].getOrientation()
        tileIndex = i

    returnValue = []

    for i, current_tile in enumerate(highestPlay): 
      if orientation == Orientation.HORIZONTAL:
          current_tile.setOrientation(Orientation.VERTICAL)
          xPos = coords[0]
          yPos = coords[1]-abs(i-tileIndex) if i <= tileIndex else abs(i-tileIndex)-coords[1]
      else:
        current_tile.setOrientation(Orientation.HORIZONTAL)
        yPos = coords[1]
        xPos = coords[0]-abs(i-tileIndex) if i <= tileIndex else abs(i-tileIndex)-coords[0]
      returnValue.append((current_tile, (xPos, yPos)))

    return returnValue
              
  def generate_play_space(self, tile=None):
    playSpace = []
    
    if tile == None:
      return [None for _ in range(10)]
    before = min(tile.getBefore(), 10)
    for i in range(before):
      playSpace.append(None)
    playSpace.append(tile)
    after = min(tile.getAfter(), 10)
    for i in range(after):
      playSpace.append(None)
    return playSpace
  
  def getPlayableTiles(self, integers, fractions, negatives, operators, before = None, after = None, last=False):
    match (before.getType() if before is not None else None, after.getType() if after is not None else None):
      case ("operator", "operator"):
        return integers + fractions
      case ("operator", "negative"):
        return integers + fractions
      case ("operator", "integer"):
        return integers + negatives
      case ("operator", "fraction"):
        return integers + negatives
      case ("operator", "equals"):
        return integers + fractions
      case ("operator", None):
        if not last:
          return integers + fractions + negatives
        else:
          return integers + fractions
      case ("negative", "operator"):
        return integers + fractions
      case ("negative", "negative"):
        return integers + fractions
      case ("negative", "integer"):
        return integers
      case ("negative", "fraction"):
        return integers
      case ("negative", "equals"):
        return integers + fractions
      case ("negative", None):
        return integers + fractions
      case ("integer", "operator"):
        return integers + fractions
      case ("integer", "negative"):
        return integers + fractions
      case ("integer", "integer"):
        return integers + negatives + operators
      case ("integer", "fraction"):
        return integers + negatives + operators
      case ("integer", "equals"):
        return integers + fractions
      case ("integer", None):
        if not last:
          return integers + fractions + negatives + operators
        else:
          return integers + fractions
      case ("fraction", "operator"):
        return []
      case ("fraction", "negative"):
        return operators
      case ("fraction", "integer"):
        return operators + negatives
      case ("fraction", "fraction"):
        return operators + negatives
      case ("fraction", "equals"):
        return []
      case ("fraction", None):
        if not last:
          return operators + negatives
        else:
          return []
      case ("equals", "operator"):
        return integers + fractions
      case ("equals", "negative"):
        return integers + fractions
      case ("equals", "integer"):
        return integers +negatives
      case ("equals", "fraction"):
        return integers + negatives
      case ("equals", None):
        if not last:
          return integers + fractions + negatives
        else:
          return integers + fractions
      case (None, None):
        return integers + fractions + negatives
      case (None, "operator"):
        return integers + fractions
      case (None, "negative"):
        return integers + fractions
      case (None, "integer"):
        return integers + negatives
      case (None, "fraction"):
        return integers + negatives
      case (None, "equals"):
        return integers + fractions