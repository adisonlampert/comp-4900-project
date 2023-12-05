from copy import deepcopy
from game import Game

class CheatingPlayer(SimplifiedPlayer):
  def __init__(self, name):
    super().__init__(name)
    
  def firstPlay(self, board):
    super().firstPlay(board)
    
  def play(self, board, opponent):
    options = super().generateAllOptions(board)
    validOptions, highestOption = self.validateOptions(board, options)
    
    print("Finished finding valid options")
    
    bestOption = self.cheat(opponent, board, validOptions)
    
    play, orientation, points, positions = 
      highestOption["play"], 
      highestOption["orientation"], 
      highestOption["points"],
      highestOption["positions"]
      
    if bestOption != None:
      play, orientation, points, positions = 
        bestOption["play"], 
        bestOption["orientation"], 
        bestOption["points"],
        bestOption["positions"]
      
    returnValue = []
    
    for i, currTile in enumerate(play):
      if orientation == None:
        break
      
      if currTile.getOrientation() != None:
        print(f"Playing on tile {currTile.getValue()}, Before: {currTile.getBefore()}, After: {currTile.getAfter()}")
        
      if orientation == Orientation.HORIZONTAL:
        currTile.setOrientation(Orientation.VERTICAL)
      else:
        currTile.setOrientation(Orientation.HORIZONTAL)
      
      returnValue.append((currTile, positions[i]))
        
    super().removePlayedTiles(play)
    
    self.points += points
    
    if super().getRackSize() == 0:
      self.points += 40

    return returnValue
    
  def cheat(self, opponent, board, options):
    diff, bestOption = 0, None
    for option in options:
      cpBoard = Game.updatePlayableSpace(play, deepcopy(board))
      oppOptions = opponent.generateAllOptions(cpBoard)
      _, highestPoints, _, _ = opponent.findHighestPlay(cpBoard, oppOptions)
      
      if option["points"] - highestPoints > diff:
        diff = option["points"] - highestPoints
        bestOption = option
    
    return bestOption
    
  def validateOptions(self, board, options):
    validOptions = []
    highestPlay, highestPoints, highestOrientation, highestPositions = [], 0, None, []
    
    for option in options:
      tileX, tileY, orientation = option["location"][0], option["location"][1], option["orientation"]
      
      for eq in option["possibleEquations"]:
        if super().validatePlay(eq):
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
            
          validOptions.append({
            "points": points,
            "play": eq,
            "orientation": orientation,
            "positions": positions
          })
          
          if points > highestPoints:
            highestPoints = points
            highestPlay = eq
            highestOrientation = orientation
            highestPositions = positions
    
    return validOptions, {
      "points": highestPlay,
      "play": highestPoints,
      "orientation": highestOrientation,
      "positions": highestPositions
    }   
        