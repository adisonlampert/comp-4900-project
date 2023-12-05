import json
from copy import deepcopy
from tile import Tile
from constants import TILES, Orientation
from board import Board
import random

class Game:
  def __init__(self, player1, player2):
    self.tiles = []
    self.rounds = 0
    self.player1, self.player2 = player1, player2
    self.turn = random.choice([self.player1, self.player2]) # Randomly choose first player
    self.opponent = None

    for tile in TILES:
      for _ in range(TILES[tile]["frequency"]):
        self.tiles.append(Tile(tile, TILES[tile]["points"], TILES[tile]["type"]))
    random.shuffle(self.tiles) # Shuffles the tiles

    self.board = Board()

  def startGame(self):
    for _ in range(9):
      self.player1.drawTile(self.dealTile())
      self.player2.drawTile(self.dealTile())
    
    play = self.turn.firstPlay()
    self.addPlayToBoard(play)
    
    for _ in range(len(play)-1):
      self.turn.drawTile(self.dealTile())
      
    if self.turn == self.player1:
      self.turn, self.opponent = self.player2, self.player1
    else:
      self.turn, self.opponent = self.player1, self.player2
  
  def playRound(self):
    play = self.turn.play(self.board, self.opponent)

    if len(play) == 0 or len(play[0]) == 0: 
      return False # Player cannot play so end game
    
    self.addPlayToBoard(play)
    
    for _ in range(len(play)-2):
      if len(self.tiles) == 0:
        break
      self.turn.drawTile(self.dealTile())

    if self.turn == self.player1:
      self.turn, self.opponent = self.player2, self.player1
    else:
      self.turn, self.opponent = self.player1, self.player2
    
    return True
      
  def dealTile(self):
    return self.tiles.pop(-1)
  
  def addPlayToBoard(self, play):
    for p in play:
      self.board.addTile(p[0], p[1][0], p[1][1])
    
    self.board = Game.updatePlayableSpace(play, deepcopy(self.board))
      
  def updatePlayableSpace(play, board):
    match (play[0][0].getOrientation()):
      case Orientation.HORIZONTAL:
        return Game.updatePlayableSpaceHorizontal(play, board)
      case Orientation.VERTICAL:
        return Game.updatePlayableSpaceVertical(play, board)
  
  def updatePlayableSpaceHorizontal(play, board):
    # We need to search and update all before and after values for tiles to the 
    # left or right of the play if the tile is vertical because then the play on it
    # would be horizontal and we don't want it to collide with this play
    leftXPos, rightXPos, yPos = play[0][1][0], play[-1][1][0], play[0][1][1]
    
    # Since this play is horizontal, the y value is always the same
    # We also want to search one row above and one row below and update those tiles
    # Because we don't want parallel plays to be touching each other
    board = Game.updateHorizontalInlineBefore(leftXPos, yPos, board)
    board = Game.updateHorizontalInlineAfter(rightXPos, yPos, board)
    
    # For horizontal plays, before and after refer to vertical space
    # above and below each tile that can be played in another turn
    
    # We need to check for tiles above and below the play tiles to find their 
    # before and after values
    bDists, board = Game.updateHorizontalPerpendicularBefore(leftXPos, rightXPos, yPos, board)
    aDists, board = Game.updateHorizontalPerpendicularAfter(leftXPos, rightXPos, yPos, board)
    
    startX = play[0][1][0]
    endX = play[-1][1][0]
    if startX == 0:
      bDists.insert(0, 18)
      aDists.insert(0, 18)
    if endX == 18:
      bDists.append(18)
      aDists.append(18)
    
    for i in range(len(play)):
      tile, xPos, yPos = play[i][0], play[i][1][0], play[i][1][1]
      if tile.getValue() == "=" or tile.getBefore() != None:
        board.updateTileBefore(xPos, yPos, 0)
        board.updateTileAfter(xPos, yPos, 0)
      else:
        board.updateTileBefore(xPos, yPos, min(*bDists[i:i+3]))
        board.updateTileAfter(xPos, yPos, min(*aDists[i:i+3]))
        
      if xPos < 18:
        if yPos > 0:
          if board.getTile(xPos+1, yPos-1) != None:
            board.updateTileBefore(xPos, yPos, 0)
            board.updateTileBefore(xPos+1, yPos-1, 0)
        if yPos < 18:
          if board.getTile(xPos+1, yPos+1) != None:
            board.updateTileAfter(xPos, yPos, 0)
            board.updateTileBefore(xPos+1, yPos+1, 0)
      if xPos > 0:
        if yPos > 0:
          if board.getTile(xPos-1, yPos-1) != None:
            board.updateTileBefore(xPos, yPos, 0)
            board.updateTileAfter(xPos-1, yPos-1, 0)
        if yPos < 18:
          if board.getTile(xPos-1, yPos+1) != None:
            board.updateTileAfter(xPos, yPos, 0)
            board.updateTileAfter(xPos-1, yPos+1, 0)
      
    return board     
    
  def updatePlayableSpaceVertical(play, board):
    # We need to search and update all before and after values for tiles above and
    # below the play if the tile is horizontal because then the play on it
    # would be vertical and we don't want it to collide with this play
    xPos, topYPos, bottomYPos = play[0][1][0], play[0][1][1], play[-1][1][1]
    
    # Since this play is horizontal, the y value is always the same
    # We also want to search one row above and one row below and update those tiles
    # Because we don't want parallel plays to be touching each other
    board = Game.updateVerticalInlineBefore(topYPos, xPos, board)
    board = Game.updateVerticalInlineAfter(bottomYPos, xPos, board)
    
    # For vertical plays, before and after refer to horizontal space to the
    # right and left of each tile that can be played in another turn
    
    # We need to check for tiles to the left and right of the play tiles to 
    # find their before and after values
    bDists, board = Game.updateVerticalPerpendicularBefore(topYPos, bottomYPos, xPos, board)
    aDists, board = Game.updateVerticalPerpendicularAfter(topYPos, bottomYPos, xPos, board)
    
    startY = play[0][1][1]
    endY = play[-1][1][1]
    if startY == 0:
      bDists.insert(0, 18)
      aDists.insert(0, 18)
    if endY == 18:
      bDists.append(18)
      aDists.append(18)
    
    for i in range(len(play)):
      tile, xPos, yPos = play[i][0], play[i][1][0], play[i][1][1]
      if tile.getValue() == "=" or tile.getBefore() != None:
        board.updateTileBefore(xPos, yPos, 0)
        board.updateTileAfter(xPos, yPos, 0)
      else:
        board.updateTileBefore(xPos, yPos, min(*bDists[i:i+3]))
        board.updateTileAfter(xPos, yPos, min(*aDists[i:i+3]))
        
      if xPos < 18:
        if yPos > 0:
          if board.getTile(xPos+1, yPos-1) != None:
            board.updateTileAfter(xPos, yPos, 0)
            board.updateTileAfter(xPos+1, yPos-1, 0)
        if yPos < 18:
          if board.getTile(xPos+1, yPos+1) != None:
            board.updateTileAfter(xPos, yPos, 0)
            board.updateTileBefore(xPos+1, yPos+1, 0)
      
      if xPos > 0:
        if yPos > 0:
          if board.getTile(xPos-1, yPos-1) != None:
            board.updateTileBefore(xPos, yPos, 0)
            board.updateTileAfter(xPos-1, yPos-1, 0)
        if yPos < 18:
          if board.getTile(xPos-1, yPos+1) != None:
            board.updateTileBefore(xPos, yPos, 0)
            board.updateTileBefore(xPos-1, yPos+1, 0)
    
    return board
  
  def updateHorizontalInlineBefore(leftXPos, yPos, board):
    # Let's start at the left position and iterate backwards until we reach another
    # tile or the left edge of the board
    aTile, rTile, bTile = False, False, False # Above tile, row tile, below tile
    
    if yPos == 0: 
      aTile = True # There are no tiles above our play
    elif yPos == 18:
      bTile = True # There are no tiles below our play
      
    for i in range(leftXPos-1, -1, -1):
      newAfter = leftXPos-i-2
      if not aTile:
        tile = board.getTile(i, yPos-1)
        if tile != None:
          aTile = True
          if tile.getOrientation() == Orientation.HORIZONTAL and tile.getValue() != "=":
            # We only need to update this tile's after value if its orientation
            # is vertical because then the play on it would be horizontal and 
            # potentially collide with this play
            board.updateTileAfter(i, yPos-1, newAfter+1)
  
      if not rTile:
        tile = board.getTile(i, yPos)
        if tile != None:
          rTile = True
          if tile.getOrientation() == Orientation.HORIZONTAL and tile.getValue() != "=":
            board.updateTileAfter(i, yPos, newAfter)

      if not bTile:
        tile = board.getTile(i, yPos+1)
        if tile != None:
          bTile = True
          if tile.getOrientation() == Orientation.HORIZONTAL and tile.getValue() != "=":
            board.updateTileAfter(i, yPos+1, newAfter+1)
      
      if aTile and rTile and bTile:
        break
      
    return board
      
  def updateHorizontalInlineAfter(rightXPos, yPos, board):
    # Let's start at the left position and iterate backwards until we reach another
    # tile or the left edge of the board
    aTile, rTile, bTile = False, False, False # Above tile, row tile, below tile
    
    if yPos == 0: 
      aTile = True # There are no tiles above our play
    elif yPos == 18:
      bTile = True # There are no tiles below our play
      
    for i in range(rightXPos+1, 19):
      newBefore = i-rightXPos-2
      if not aTile:
        tile = board.getTile(i, yPos-1)
        if tile != None:
          aTile = True
          if tile.getOrientation() == Orientation.HORIZONTAL and tile.getValue() != "=":
            # We only need to update this tile's after value if its orientation
            # is vertical because then the play on it would be horizontal and 
            # potentially collide with this play
            board.updateTileBefore(i, yPos-1, newBefore+1)
  
      if not rTile:
        tile = board.getTile(i, yPos)
        if tile != None:
          rTile = True
          if tile.getOrientation() == Orientation.HORIZONTAL and tile.getValue() != "=":
            board.updateTileBefore(i, yPos, newBefore)

      if not bTile:
        tile = board.getTile(i, yPos+1)
        if tile != None:
          bTile = True
          if tile.getOrientation() == Orientation.HORIZONTAL and tile.getValue() != "=":
            board.updateTileBefore(i, yPos+1, newBefore+1)
      
      if aTile and rTile and bTile:
        break
      
    return board
    
  def updateHorizontalPerpendicularBefore(startXPos, endXPos, yPos, board):
    dists = []
    xStart, xEnd = max(startXPos-1, 0), min(endXPos+2,19) # Ensures we are never out of bounds
    
    for i in range(xStart, xEnd):
      for j in range(yPos-1, -1, -1):
        tile = board.getTile(i, j)
        if tile != None:
          if tile.getOrientation() == Orientation.HORIZONTAL and tile.getValue() != "=":
            # This means that the play on the tile will be vertical (perpendicular)
            # So the space below it represents its after value so we need to update it
            newAfter = yPos-j-2
            board.updateTileAfter(i, j, newAfter)
          dists.append(yPos-j-2)
          break
      if len(dists) < (i-startXPos+1):
        dists.append(yPos)
    
    return dists, board
  
  def updateHorizontalPerpendicularAfter(startXPos, endXPos, yPos, board):
    dists = []
    xStart, xEnd = max(startXPos-1, 0), min(endXPos+2,19) # Ensures we are never out of bounds
    
    for i in range(xStart, xEnd):
      for j in range(yPos+1, 19):
        tile = board.getTile(i, j)
        if tile != None:
          if tile.getOrientation() == Orientation.HORIZONTAL and tile.getValue() != "=":
            # This means that the play on the tile will be vertical (perpendicular)
            # So the space below it represents its after value so we need to update it
            newAfter = j-yPos-2
            board.updateTileBefore(i, j, newAfter)
          dists.append(j-yPos-2)
          break
      if len(dists) < (i-startXPos+1):
        dists.append(19-yPos-1)
    
    return dists, board
  
  def updateVerticalInlineBefore(topYPos, xPos, board):
    # Let's start at the left position and iterate backwards until we reach another
    # tile or the left edge of the board
    lTile, cTile, rTile = False, False, False # Left tile, center tile, right tile
    
    if xPos == 0: 
      lTile = True # There are no tiles to the left of our play
    elif xPos == 18:
      rTile = True # There are no tiles to the right of our play
      
    for i in range(topYPos-1, -1, -1):
      newAfter = topYPos-i-2
      if not lTile:
        tile = board.getTile(xPos-1, i)
        if tile != None:
          lTile = True
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            # We only need to update this tile's after value if its orientation
            # is horizontal because then the play on it would be vertical and 
            # potentially collide with this play
            board.updateTileAfter(xPos-1, i, newAfter+1)
  
      if not cTile:
        tile = board.getTile(xPos, i)
        if tile != None:
          cTile = True
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            board.updateTileAfter(xPos, i, newAfter)

      if not rTile:
        tile = board.getTile(xPos+1, i)
        if tile != None:
          rTile = True
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            board.updateTileAfter(xPos+1, i, newAfter+1)
      
      if lTile and cTile and rTile:
        break
      
    return board
      
  def updateVerticalInlineAfter(bottomYPos, xPos, board):
    lTile, cTile, rTile = False, False, False # Left tile, center tile, right tile
    
    if xPos == 0: 
      lTile = True # There are no tiles left of our play
    elif xPos == 18:
      rTile = True # There are no tiles right of our play
      
    for i in range(bottomYPos+1, 19):
      newBefore = i-bottomYPos-2
      if not lTile:
        tile = board.getTile(xPos-1, i)
        if tile != None:
          lTile = True
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            board.updateTileBefore(xPos-1, i, newBefore+1)
  
      if not cTile:
        tile = board.getTile(xPos, i)
        if tile != None:
          cTile = True
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            board.updateTileBefore(xPos, i, newBefore)

      if not rTile:
        tile = board.getTile(xPos+1, i)
        if tile != None:
          rTile = True
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            board.updateTileBefore(xPos+1, i, newBefore+1)
      
      if lTile and cTile and rTile:
        break
      
    return board
    
  def updateVerticalPerpendicularBefore(startYPos, endYPos, xPos, board):
    dists = []
    yStart, yEnd = max(startYPos-1, 0), min(endYPos+2,19) # Ensures we are never out of bounds
    
    for i in range(yStart, yEnd):
      for j in range(xPos-1, -1, -1):
        tile = board.getTile(j, i)
        if tile != None:
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            # This means that the play on the tile will be horizontal (perpendicular)
            # So the space below it represents its after value so we need to update it
            newAfter = xPos-j-2
            board.updateTileAfter(j, i, newAfter)
          dists.append(xPos-j-2)
          break
      if len(dists) < (i-startYPos+1):
        dists.append(xPos)
    
    return dists, board
  
  def updateVerticalPerpendicularAfter(startYPos, endYPos, xPos, board):
    dists = []
    yStart, yEnd = max(startYPos-1, 0), min(endYPos+2,19) # Ensures we are never out of bounds
    
    for i in range(yStart, yEnd):
      for j in range(xPos+1, 19):
        tile = board.getTile(j, i)
        if tile != None:
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            newBefore = j-xPos-2
            board.updateTileBefore(j, i, newBefore)
          dists.append(j-xPos-2)
          break
      if len(dists) < (i-startYPos+1):
        dists.append(19-xPos-1)
    
    return dists, board
  
  def __str__(self):
    return f'Player 1 points: {self.player1.getPoints()}\nPlayer 2 points: {self.player2.getPoints()}\n{self.board}'


# try:
#   with open("game.json", "r") as file:
#     existingGame = json.load(file)
# except (FileNotFoundError, json.JSONDecodeError):
#   existingGame = []
  
# entry = {}
# entry["player"] = self.turn.getName()
# entry["beforeRack"] = [r.getValue() for r in initRack]
# entry["afterRack"] = [r.getValue() for r in self.turn.getRack()]
# entry["play"] = [p[0].getValue() for p in play]
# entry["xPositions"] = [p[1][0] for p in play]
# entry["yPositions"] = [p[1][1] for p in play]
# entry["points"] = self.turn.getPoints()

# existingGame.append(entry)
  
# with open("game.json", "w") as file:
#   json.dump(existingGame, file, indent=2)