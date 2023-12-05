from copy import deepcopy
import math
from player import Player
from constants import Orientation, MULTIPLIERS
from tile import Tile

class SimplifiedPlayer(Player):
  def __init__(self, name):
    super().__init__(name)
    
  def generateAllOptions(self, board):
    options = []
    tile = None

    for yPos in range(19):
      for xPos in range(19): 
        tile = board.getTile(xPos, yPos)

        if tile is None or not tile.isPlayable():
          continue
        
        print(f'Checking new tile {tile.getValue()} {xPos, yPos}, Before: {tile.getBefore()}, After: {tile.getAfter()}')
        
        playSpace = self.generatePlaySpace(tile)
        options += self.generateOptions(playSpace, tile, xPos, yPos)
        
    return options
  
  def findHighestPlay(self, board, options):
    highestPlay, highestPoints, highestOrientation, highestPositions = [], 0, None, []
    
    for option in options:
      tileX, tileY, orientation = option["location"][0], option["location"][1], option["orientation"]
      
      for eq in option["possibleEquations"]:
        points, positions = 0, []
        doubleEquation, tripleEquation = False, False
        tileIndex = next((index for (index, tile) in enumerate(eq) if tile.getOrientation() != None), None)
        
        if tileIndex == None:
          break
        
        for i, t in enumerate(eq):
          points += t.getPoints()
          
          if orientation == Orientation.HORIZONTAL:
            xPos = tileX
            yPos = tileY-abs(i-tileIndex) if i <= tileIndex else abs(i-tileIndex)+tileY
          else:
            yPos = tileY
            xPos = tileX-abs(i-tileIndex) if i <= tileIndex else abs(i-tileIndex)+tileX
          
          positions.append((xPos, yPos))
          
          coordinates = f"{xPos},{yPos}"
          if coordinates in MULTIPLIERS and board.getTile(xPos, yPos) is None:
            mult = MULTIPLIERS[coordinates]
            points += t.getPoints() * (2 if mult == "2S" else 3 if mult == "3S" else 1)
            doubleEquation = doubleEquation or (mult == "2E")
            tripleEquation = tripleEquation or (mult == "3E")

        if doubleEquation:
          points *= 2
        if tripleEquation:
          points *= 3
        
        if points > highestPoints:
          if super().validatePlay(eq):
            highestPoints = points
            highestPlay = eq
            highestOrientation = orientation
            highestPositions = positions
    
    return highestPlay, highestPoints, highestOrientation, highestPositions
  
  def play(self, board, _):
    options = self.generateAllOptions(board)
    highestPlay, highestPoints, highestOrientation, highestPositions = self.findHighestPlay(board, options)
    
    returnValue = []
    for i, currTile in enumerate(highestPlay):
      if highestOrientation == None:
        break
      
      if currTile.getOrientation() != None:
        print(f"Playing on tile {currTile.getValue()}, Before: {currTile.getBefore()}, After: {currTile.getAfter()}")
        
      if highestOrientation == Orientation.HORIZONTAL:
        currTile.setOrientation(Orientation.VERTICAL)
      else:
        currTile.setOrientation(Orientation.HORIZONTAL)
      
      returnValue.append((currTile, highestPositions[i]))
        
    self.removePlayedTiles(highestPlay)
    
    self.points += highestPoints
    
    if super().getRackSize() == 0:
      self.points += 40

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
          aRange = len(cPlaySpace) - min(10, tile.getAfter()) if not space else len(cPlaySpace) - min(10, tile.getAfter())+1
          for k in range(aRange, min(j+12, len(cPlaySpace)+1)):
            possibleArrangements.append(cPlaySpace[j:k])
      else:
        bRange = min(10, tile.getBefore()) if not space else min(10, tile.getBefore())-1
        for j in range(0, bRange):
          for k in range(i+2, min(j+12, len(cPlaySpace)+1)):
            possibleArrangements.append(cPlaySpace[j:k])
            
      possibilities = self.generatePossibleEquations(possibleArrangements)
      options.append({"location": (xPos, yPos), "orientation": tile.getOrientation(), "possibleEquations": possibilities})
      
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
      playableTiles = super().getPlayableTiles(integers, fractions, negatives, operators, before=before, after=after, last=True)
    else:
      playableTiles = super().getPlayableTiles(integers, fractions, negatives, operators, before=before, after=after)
          
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
    highestPlay, options = [], []
    playSpace = [None]*10
    
    for i in range(1, len(playSpace) - 1):
      cPlaySpace = playSpace.copy()
      cPlaySpace[i] = Tile("=", 0, "equals")
      possibleArrangements = []
        
      for j in range(0, i):
        for k in range(i+1, len(cPlaySpace)-1):
          if len(cPlaySpace[j:k]) > 2:
            possibleArrangements.append(cPlaySpace[j:k])
            
      options += self.generatePossibleEquations(possibleArrangements)
        
    highestPlay, highestPoints, highestPositions  = [], 0, []
    for eq in options: 
      doubleEquation, tripleEquation = False, False
      xVal = 9-math.floor(len(highestPlay)/2)
      points = 0
      positions = []
      for t in eq:
        points += t.getPoints()
        positions.append((xVal, 9))
        
        coordinates = f"{xVal},9" 
        if coordinates in MULTIPLIERS:
          mult = MULTIPLIERS[coordinates]
          points += t.getPoints() * (2 if mult == "2S" else 3 if mult == "3S" else 1)
          doubleEquation = doubleEquation or (mult == "2E")
          tripleEquation = tripleEquation or (mult == "3E") 
          
        xVal +=1

      if doubleEquation:
        points *= 2
      if tripleEquation:
        points *= 3

      if points > highestPoints:
        if super().validatePlay(eq):
          highestPlay = eq
          highestPoints = points
          highestPlay = eq
          highestPositions = positions
        
    self.removePlayedTiles(highestPlay)
    
    if super().getRackSize() == 0:
      self.points += 40

    returnValue = []
    
    for i, currTile in enumerate(highestPlay):
      currTile.setOrientation(Orientation.HORIZONTAL)
      returnValue.append((currTile, highestPositions[i]))
    
    self.points += highestPoints
      
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
      