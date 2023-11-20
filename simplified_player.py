from copy import deepcopy
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
    
    options = []

    for yPos in range(19):
      for xPos in range(19): 
        tile = board.getTile(xPos, yPos)

        if tile is None or not tile.isPlayable():
          continue
        
        playSpace = self.generatePlaySpace(tile)
        options += self.generateOptions(playSpace, tile, xPos, yPos)  
        
    validEquations = []
    for r in options:
      for p in r["possibleEquations"]:
        if super().validatePlay(p):
          validEquations.append({"location": r["location"], "equation": p})
    
    highestPlay, highestPoints, coords = [], 0, (0,0)
    for eq in validEquations: 
      points = 0
      for t in eq["equation"]:
        points += t.getPoints()

      if points > highestPoints:
        highestPoints = points
        highestPlay = eq["equation"]
        coords = eq["location"]

    orientation, tileIndex = None, 0
    
    for i in range(len(highestPlay)):
      if highestPlay[i].getOrientation():
        orientation, tileIndex = highestPlay[i].getOrientation(), i
        
    self.removePlayedTiles(highestPlay)

    returnValue = []

    for i, currTile in enumerate(highestPlay): 
      if orientation == Orientation.HORIZONTAL:
          currTile.setOrientation(Orientation.VERTICAL)
          xPos = coords[0]
          yPos = coords[1]-abs(i-tileIndex) if i <= tileIndex else abs(i-tileIndex)+coords[1]
      else:
        currTile.setOrientation(Orientation.HORIZONTAL)
        yPos = coords[1]
        xPos = coords[0]-abs(i-tileIndex) if i <= tileIndex else abs(i-tileIndex)+coords[0]
      returnValue.append((currTile, (xPos, yPos)))

    return returnValue
              
  def generatePlaySpace(self, tile=None):
    playSpace = []
    
    if tile == None:
      return [None for _ in range(10)]
    before = min(tile.getBefore(), 10)
    for _ in range(before):
      playSpace.append(None)
    playSpace.append(tile)
    after = min(tile.getAfter(), 10)
    for _ in range(after):
      playSpace.append(None)
    return playSpace
  
  def generateOptions(self, playSpace, tile, xPos, yPos):
    options = []
    
    for i in range(1, len(playSpace) - 1):
      bType = playSpace[i-1].getType() if playSpace[i-1] is not None else None
      aType = playSpace[i+1].getType() if playSpace[i+1] is not None else None

      if playSpace[i] is not None or (bType == "operator" or bType == "negative") or aType == "operator":
        continue

      cPlaySpace = playSpace.copy()
      cPlaySpace[i] = Tile("=", 0, "equals")
      possibleArrangements = []

      # Operators cannot be the first or last symbol of the equation so our range changes
      space =  False
      if tile.getType() == "operator" or tile.getType() == "negative":
        space =  True
        
      if i < len(cPlaySpace) - min(10, tile.getAfter()):
        for j in range(0, i):
          sRange = len(cPlaySpace) - min(10, tile.getAfter()) if not space else len(cPlaySpace) - min(10, tile.getAfter())+1
          for k in range(sRange, min(j+12, len(cPlaySpace)+1)):
            possibleArrangements.append(cPlaySpace[j:k])
      else:
        # eRange = len(cPlaySpace) - min(10, tile.getAfter()) if not space else len(cPlaySpace) - min(10, tile.getAfter())-1
        for j in range(0, i):
          for k in range(i+2, min(j+12, len(cPlaySpace)+1)):
            possibleArrangements.append(cPlaySpace[j:k])
            
      possibilities = self.generatePossibleEquations(possibleArrangements)
      options.append({"location": (xPos, yPos), "possibleEquations": possibilities})
      
    return options
    
  def generatePossibleEquations(self, possibleArrangements):
    possibilities = []
    
    for pa in possibleArrangements:      
      integers, fractions, negatives, operators = deepcopy(self.integers), deepcopy(self.fractions), deepcopy(self.negatives), deepcopy(self.operators)
            
      noneIndices = [i for i, x in enumerate(pa) if x is None]
      
      # Start the recursive generation process
      self.generatePartialEquations(pa.copy(), noneIndices, integers, fractions, negatives, operators, possibilities)
        
    return possibilities
  
  def generatePartialEquations(self, currentEq, remainingNoneIndices, integers, fractions, negatives, operators, possibilities):
    if not remainingNoneIndices:
      # If there are no remaining None indices, check if the equation is valid
      possibilities.append(currentEq.copy())
      return

    # Get the next None index to fill
    nextNoneIndex = remainingNoneIndices[0]

    # Get playable tiles for the current position
    before = currentEq[nextNoneIndex-1] if nextNoneIndex-1 >= 0 else None
    after = currentEq[nextNoneIndex+1] if nextNoneIndex+1 < len(currentEq) else None
          
    if nextNoneIndex == len(currentEq)-1:
      playableTiles = self.getPlayableTiles(integers, fractions, negatives, operators, before=before, after=after, last=True)
    else:
      playableTiles = self.getPlayableTiles(integers, fractions, negatives, operators, before=before, after=after)
          
    # Return and don't add equation if there are no playable tiles
    if len(playableTiles) == 0:
      return
    
    for tile in playableTiles:
      currentEq[nextNoneIndex] = tile
      
      # Create new lists without the tile we just played
      integers_copy = [t for t in integers if t != tile]
      fractions_copy = [t for t in fractions if t != tile]
      negatives_copy = [t for t in negatives if t != tile]
      operators_copy = [t for t in operators if t != tile]
      
      # Generate permutations for the remaining None indices
      self.generatePartialEquations(currentEq, remainingNoneIndices[1:], integers_copy, fractions_copy,
                                      negatives_copy, operators_copy, possibilities)
      currentEq[nextNoneIndex] = None  # Backtrack
      
  def firstPlay(self):
    highestPlay = []
        
    playSpace = [None]*10
    options = []
    
    for i in range(1, len(playSpace) - 1):
      cPlaySpace = playSpace.copy()
      cPlaySpace[i] = Tile("=", 0, "equals")
      possibleArrangements = []
        
      for j in range(0, i):
        for k in range(i+1, len(cPlaySpace)-1):
          if len(cPlaySpace[j:k]) > 2:
            possibleArrangements.append(cPlaySpace[j:k])
            
      options += self.generatePossibleEquations(possibleArrangements)
        
    highestPlay, highestPoints  = [], 0
    for eq in options: 
      points = 0
      for t in eq:
        points += t.getPoints()

      if points > highestPoints:
        if super().validatePlay(eq):
          highestPlay = eq
          highestPoints = points
          highestPlay = eq
        
    self.removePlayedTiles(highestPlay)

    returnValue = []

    xVal = 9-math.floor(len(highestPlay)/2)
    
    for i, currTile in enumerate(highestPlay):
      currTile.setOrientation(Orientation.HORIZONTAL)
      yPos = 9
      xPos = xVal
      xVal +=1
      returnValue.append((currTile, (xPos, yPos)))

    return returnValue
  
  def removePlayedTiles(self, highestPlay):
    def removeFirstMatchingTile(obj, arrayList):
      try:
        arrayIndex, itemIndex = next(
            ((i, j) for i, array in enumerate(arrayList) for j, item in enumerate(array) if obj.getValue() == item.getValue())
        )
        del arrayList[arrayIndex][itemIndex]
      except StopIteration:
        pass  # No matching item found
    
    rack = [self.integers, self.fractions, self.operators, self.negatives]
    for i in range(len(highestPlay)):
      removeFirstMatchingTile(highestPlay[i], rack)

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
        return integers + negatives
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
