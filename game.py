from tile import Tile
from constants import TILES, Orientation
from board import Board
from player import Player
import random
import numpy as np


class Game:
  def __init__(self, player1, player2):
    self.tiles = []
    self.rounds = 0
    self.player1, self.player2 = player1, player2
    self.turn = random.choice([self.player1, self.player2]) # Randomly choose first player

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
    
    if self.turn == self.player1:
      self.turn = self.player2
    else:
      self.turn = self.player1
  
  def playRound(self):
    play = self.turn.play(self.board)

    if len(play) == 0: 
      return False # Player cannot play so end game
    
    self.addPlayToBoard(play)

    if self.turn == self.player1:
      self.turn = self.player2
    else:
      self.turn = self.player1
      
  def dealTile(self):
    return self.tiles.pop(-1)
  
  def addPlayToBoard(self, play):
    for p in play:
      self.board.addTile(p[0], p[1][0], p[1][1])
    
    self.updatePlayableSpace(play)
      
  def updatePlayableSpace(self, play):
    match (play[0][0].getOrientation()):
      case Orientation.HORIZONTAL:
        self.updatePlayableSpaceHorizontal(play)
        return 
      case Orientation.VERTICAL:
        self.updatePlayableSpaceVertical(play)
        return
  
  def updatePlayableSpaceHorizontal(self, play):
    # We need to search and update all before and after values for tiles to the 
    # left or right of the play if the tile is vertical because then the play on it
    # would be horizontal and we don't want it to collide with this play
    leftXPos, rightXPos, yPos = play[0][1][0], play[-1][1][0], play[0][1][1]
    
    # Since this play is horizontal, the y value is always the same
    # We also want to search one row above and one row below and update those tiles
    # Because we don't want parallel plays to be touching each other
    self.updateHorizontalInlineBefore(leftXPos, yPos)
    self.updateHorizontalInlineAfter(rightXPos, yPos)
    
    # For horizontal plays, before and after refer to vertical space
    # above and below each tile that can be played in another turn
    
    # We need to check for tiles above and below the play tiles to find their 
    # before and after values
    bDists = self.updateHorizontalPerpendicularBefore(leftXPos, rightXPos, yPos)
    aDists = self.updateHorizontalPerpendicularAfter(leftXPos, rightXPos, yPos)
    
    for i in range(len(play)):
      tile, xPos, yPos = play[i][0], play[i][1][0], play[i][1][1]
      if tile.getValue() == "=":
        self.board.updateTileBefore(xPos, yPos, 0)
        self.board.updateTileAfter(xPos, yPos, 0)
      else:
        if xPos == 0:
          self.board.updateTileBefore(xPos, yPos, min(*bDists[:i+2]))
        elif xPos == 18:
          self.board.updateTileBefore(xPos, yPos, min(*bDists[i:]))
        else:
          self.board.updateTileBefore(xPos, yPos, min(*bDists[i:i+3]))

        if xPos == 18:
          self.board.updateTileAfter(xPos, yPos, min(*aDists[i:]))
        else:
          self.board.updateTileAfter(xPos, yPos, min(*aDists[i:i+3]))
    
  def updatePlayableSpaceVertical(self, play):
    # We need to search and update all before and after values for tiles above and
    # below the play if the tile is horizontal because then the play on it
    # would be vertical and we don't want it to collide with this play
    xPos, topYPos, bottomYPos = play[0][1][0], play[0][1][1], play[-1][1][1]
    
    # Since this play is horizontal, the y value is always the same
    # We also want to search one row above and one row below and update those tiles
    # Because we don't want parallel plays to be touching each other
    self.updateVerticalInlineBefore(topYPos, xPos)
    self.updateVerticalInlineAfter(bottomYPos, xPos)
    
    # For vertical plays, before and after refer to horizontal space to the
    # right and left of each tile that can be played in another turn
    
    # We need to check for tiles to the left and right of the play tiles to 
    # find their before and after values
    bDists = self.updateVerticalPerpendicularBefore(topYPos, bottomYPos, xPos)
    aDists = self.updateVerticalPerpendicularAfter(topYPos, bottomYPos, xPos)
    
    for i in range(len(play)):
      tile, xPos, yPos = play[i][0], play[i][1][0], play[i][1][1]
      if tile.getValue() == "=":
        self.board.updateTileBefore(xPos, yPos, 0)
        self.board.updateTileAfter(xPos, yPos, 0)
      else:
        if xPos == 0:
          self.board.updateTileBefore(xPos, yPos, min(*bDists[:i+2]))
        elif xPos == 18:
          self.board.updateTileBefore(xPos, yPos, min(*bDists[i:]))
        else:
          self.board.updateTileBefore(xPos, yPos, min(*bDists[i:i+3]))

        if xPos == 18:
          self.board.updateTileAfter(xPos, yPos, min(*aDists[i:]))
        else:
          self.board.updateTileAfter(xPos, yPos, min(*aDists[i:i+3]))
  
  def updateHorizontalInlineBefore(self, leftXPos, yPos):
    # Let's start at the left position and iterate backwards until we reach another
    # tile or the left edge of the board
    aTile, rTile, bTile = False, False, False # Above tile, row tile, below tile
    
    if yPos == 0: 
      aTile = True # There are no tiles above our play
    elif yPos == 18:
      bTile = True # There are no tiles below our play
      
    for i in range(leftXPos-1, -1, -1):
      if not aTile:
        tile = self.board.getTile(i, yPos-1)
        if tile != None:
          aTile = True
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            # We only need to update this tile's after value if its orientation
            # is vertical because then the play on it would be horizontal and 
            # potentially collide with this play
            self.board.updateTileAfter(i, yPos-1, leftXPos-i-1)
  
      if not rTile:
        tile = self.board.getTile(i, yPos)
        if tile != None:
          rTile = True
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            self.board.updateTileAfter(i, yPos, leftXPos-i-1)

      if not bTile:
        tile = self.board.getTile(i, yPos+1)
        if tile != None:
          bTile = True
          if tile.getOrientation() == Orientation.VERTICAL:
            self.board.updateTileAfter(i, yPos+1, leftXPos-i-1)
      
      if aTile and rTile and bTile:
        break
      
  def updateHorizontalInlineAfter(self, rightXPos, yPos):
    # Let's start at the left position and iterate backwards until we reach another
    # tile or the left edge of the board
    aTile, rTile, bTile = False, False, False # Above tile, row tile, below tile
    
    if yPos == 0: 
      aTile = True # There are no tiles above our play
    elif yPos == 18:
      bTile = True # There are no tiles below our play
      
    for i in range(rightXPos+1, 19):
      if not aTile:
        tile = self.board.getTile(i, yPos-1)
        if tile != None:
          aTile = True
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            # We only need to update this tile's after value if its orientation
            # is vertical because then the play on it would be horizontal and 
            # potentially collide with this play
            self.board.updateTileBefore(i, yPos-1, i-rightXPos-1)
  
      if not rTile:
        tile = self.board.getTile(i, yPos)
        if tile != None:
          rTile = True
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            self.board.updateTileBefore(i, yPos, i-rightXPos-1)

      if not bTile:
        tile = self.board.getTile(i, yPos+1)
        if tile != None:
          bTile = True
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            self.board.updateTileBefore(i, yPos+1, i-rightXPos-1)
      
      if aTile and rTile and bTile:
        break
    
  def updateHorizontalPerpendicularBefore(self, startXPos, endXPos, yPos):
    dists = []
    xStart, xEnd = max(startXPos-1, 0), min(endXPos+2,19) # Ensures we are never out of bounds
    
    for i in range(xStart, xEnd):
      for j in range(yPos-1, -1, -1):
        tile = self.board.getTile(i, j)
        if tile != None:
          if tile.getOrientation() == Orientation.HORIZONTAL and tile.getValue() != "=":
            # This means that the play on the tile will be vertical (perpendicular)
            # So the space below it represents its after value so we need to update it
            self.board.updateTileAfter(i, j, yPos-j-2)
            dists.append(yPos-j-2)
            break
      if len(dists) < (i-xStart+1):
        dists.append(yPos)
    
    return dists
  
  def updateHorizontalPerpendicularAfter(self, startXPos, endXPos, yPos):
    dists = []
    xStart, xEnd = max(startXPos-1, 0), min(endXPos+2,19) # Ensures we are never out of bounds
    
    for i in range(xStart, xEnd):
      for j in range(yPos+1, 19):
        tile = self.board.getTile(i, j)
        if tile != None:
          if tile.getOrientation() == Orientation.HORIZONTAL and tile.getValue() != "=":
            # This means that the play on the tile will be vertical (perpendicular)
            # So the space below it represents its after value so we need to update it
            self.board.updateTileBefore(i, j, j-yPos-2)
            dists.append(j-yPos-2)
            break
      if len(dists) < (i-xStart+1):
        dists.append(19-yPos-1)
    
    return dists
  
  def updateVerticalInlineBefore(self, topYPos, xPos):
    # Let's start at the left position and iterate backwards until we reach another
    # tile or the left edge of the board
    lTile, cTile, rTile = False, False, False # Left tile, center tile, right tile
    
    if xPos == 0: 
      lTile = True # There are no tiles to the left of our play
    elif xPos == 18:
      rTile = True # There are no tiles to the right of our play
      
    for i in range(topYPos-1, -1, -1):
      if not lTile:
        tile = self.board.getTile(xPos-1, i)
        if tile != None:
          lTile = True
          if tile.getOrientation() == Orientation.HORIZONTAL and tile.getValue() != "=":
            # We only need to update this tile's after value if its orientation
            # is horizontal because then the play on it would be vertical and 
            # potentially collide with this play
            self.board.updateTileAfter(xPos-1, i, topYPos-i-1)
  
      if not cTile:
        tile = self.board.getTile(xPos, i)
        if tile != None:
          cTile = True
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            self.board.updateTileAfter(xPos, i, topYPos-i-1)

      if not rTile:
        tile = self.board.getTile(xPos+1, i)
        if tile != None:
          rTile = True
          if tile.getOrientation() == Orientation.VERTICAL:
            self.board.updateTileAfter(xPos+1, i, topYPos-i-1)
      
      if lTile and cTile and rTile:
        break
      
  def updateVerticalInlineAfter(self, bottomYPos, xPos):
    lTile, cTile, rTile = False, False, False # Left tile, center tile, right tile
    
    if xPos == 0: 
      lTile = True # There are no tiles left of our play
    elif xPos == 18:
      rTile = True # There are no tiles right of our play
      
    for i in range(bottomYPos+1, 19):
      if not lTile:
        tile = self.board.getTile(xPos-1, i)
        if tile != None:
          lTile = True
          if tile.getOrientation() == Orientation.HORIZONTAL and tile.getValue() != "=":
            self.board.updateTileBefore(xPos-1, i, i-bottomYPos-1)
  
      if not cTile:
        tile = self.board.getTile(xPos, i)
        if tile != None:
          cTile = True
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            self.board.updateTileBefore(xPos, i, i-bottomYPos-1)

      if not rTile:
        tile = self.board.getTile(xPos+1, i)
        if tile != None:
          rTile = True
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            self.board.updateTileBefore(xPos+1, i, i-bottomYPos-1)
      
      if lTile and cTile and rTile:
        break
    
  def updateVerticalPerpendicularBefore(self, startYPos, endYPos, xPos):
    dists = []
    yStart, yEnd = max(startYPos-1, 0), min(endYPos+2,19) # Ensures we are never out of bounds
    
    for i in range(yStart, yEnd):
      for j in range(xPos-1, -1, -1):
        tile = self.board.getTile(j, i)
        if tile != None:
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            # This means that the play on the tile will be horizontal (perpendicular)
            # So the space below it represents its after value so we need to update it
            self.board.updateTileAfter(j, i, xPos-j-2)
            dists.append(xPos-j-2)
            break
      if len(dists) < (i-yStart+1):
        dists.append(xPos)
    
    return dists
  
  def updateVerticalPerpendicularAfter(self, startYPos, endYPos, xPos):
    dists = []
    xStart, xEnd = max(startYPos-1, 0), min(endYPos+2,19) # Ensures we are never out of bounds
    
    for i in range(xStart, xEnd):
      for j in range(xPos+1, 19):
        tile = self.board.getTile(j, i)
        if tile != None:
          if tile.getOrientation() == Orientation.VERTICAL and tile.getValue() != "=":
            self.board.updateTileBefore(j, i, j-xPos-2)
            dists.append(j-xPos-2)
            break
      if len(dists) < (i-xStart+1):
        dists.append(19-xPos-1)
    
    return dists
