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
        self.tiles.append(Tile(tile, TILES[tile]["points"]))
    random.shuffle(self.tiles) # Shuffles the tiles

    self.board = Board()

  def startGame(self):
    for _ in range(9):
      self.player1.drawTile(self.dealTile())
      self.player2.drawTile(self.dealTile())
  
  def playRound(self):
    play = self.turn.play(self.board)

    if len(play) == 0: 
      return False # Player cannot play so end game
    
    for p in play:
      tile, xPos, yPos = p[0], p[1][0], p[1][1]

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
    xStart, yStart, xEnd, yEnd = play[0][1][0], play[0][1][1], play[-1][1][0], play[-1][1][1]
    self.updateParallelPlayableSpace(xStart, xEnd, yStart, yEnd)
    bdists = self.updatePerpendicularPlayableSpace(xStart, yStart, xEnd, yEnd, "before")
    adists = self.updatePerpendicularPlayableSpace(xStart, yStart, xEnd, yEnd, "after")
    
    orientation = self.board.getTile(xStart, yStart).getOrientation()
    
    for x in range(xStart, xEnd+1):
      for y in range(yStart, yEnd+1):
        if orientation == Orientation.HORIZONTAL:
          if x > 0:
            if x < 18:
              self.board.updateTileBefore(x, y, max(*[bdists[x-1], bdists[x], bdists[x+1]]))
              self.board.updateTileAfter(x, y, max(*[adists[x-1], adists[x], adists[x+1]]))
            else:
              self.board.updateTileBefore(x, y, max(*[bdists[x-1], bdists[x]]))
              self.board.updateTileAfter(x, y, max(*[adists[x-1], adists[x]]))
          else:
            self.board.updateTileBefore(x, y, max(*[bdists[x], bdists[x+1]]))
            self.board.updateTileAfter(x, y, max(*[adists[x], adists[x+1]]))
        else:
          if y > 0:
            if y < 18:
              self.board.updateTileBefore(x, y, max(*[bdists[y-1], bdists[y], bdists[y+1]]))
              self.board.updateTileAfter(x, y, max(*[adists[y-1], adists[y], adists[y+1]]))
            else:
              self.board.updateTileBefore(x, y, max(*[bdists[y-1], bdists[y]]))
              self.board.updateTileAfter(x, y, max(*[adists[y-1], adists[y]]))
          else:
            self.board.updateTileBefore(x, y, max(*[bdists[y], bdists[y+1]]))
            self.board.updateTileAfter(x, y, max(*[adists[y], adists[y+1]]))
  
  def updateParallelPlayableSpace(self, xStart, xEnd, yStart, yEnd):
    orientation = self.board.getTile(xStart, yStart).getOrientation()

    match orientation:
      case Orientation.HORIZONTAL:
        self.updateParallel(Orientation.VERTICAL, yStart, xStart, "before")
        self.updateParallel(Orientation.VERTICAL, yStart, xEnd, "after")
      case Orientation.VERTICAL:
        self.updateParallel(Orientation.HORIZONTAL, xStart, yStart, "before")
        self.updateParallel(Orientation.HORIZONTAL, xStart, yEnd, "after")
      case _:
        return
  
  def updateParallel(self, orientation, parallel, perp, direction):
    bTile, cTile, aTile = False, False, False # We are updating all surrounding parallel tiles

    r = range(perp+1, 19) # Iterate after play to bottom/right of board
    if direction == "before":
      r = range(perp-1, 0, -1) # Iterate before play to top/left of board

    # Update playable range for parallel tiles
    for i in r:
      # Iterate until we find & update all surrounding parallel tiles or edge of board
      xPos, yPos = parallel, i
      if orientation == Orientation.VERTICAL:
        xPos, yPos = i, parallel

      tile = self.board.getTile(xPos, yPos)
      if tile != None:
        self.updatePlayableTileSpace(tile, orientation, direction, perp, i, xPos, yPos)
        cTile = True
      
      # We also want to check & update the tiles before and after the play
      #   For horizontal plays, above and below
      #   For vertical plays, left and right
      # because we don't want tiles next to each other
      if parallel > 0:
        xPos = parallel-1
        if orientation == Orientation.VERTICAL:
          yPos = parallel-1
        
        lt = self.board.getTile(xPos, yPos)
        if lt != None:
          self.updatePlayableTileSpace(tile, orientation, direction, perp, i, xPos, yPos)
          bTile = True
      if parallel < 18:
        xPos = parallel+1
        if orientation == Orientation.VERTICAL:
          yPos = parallel+1

        rt = self.board.getTile(xPos, yPos)
        if rt != None:
          self.updatePlayableTileSpace(tile, orientation, direction, perp, i, xPos, yPos) 
          aTile = True

      if bTile and cTile and aTile:
        break
  
  def updatePerpendicularPlayableSpace(self, xStart, yStart, xEnd, yEnd, direction):
    orientation = self.board.getTile(xStart, yStart).getOrientation()
    dists = {}

    r, start = range(max(0, yStart-1), min(19, yEnd+2)), xStart
    if orientation == Orientation.HORIZONTAL:
      r, start = range(max(0, xStart-1), min(19, xEnd+2)), yStart
    
    for i in r:
      rd = range(start+1, 19) # Iterate after play to bottom/right of board
      
      if direction == "before":
        rd = range(start-1, 0, -1) # Iterate before play to top/left of board
      
      dist = 0  
      for j in rd:
        xPos, yPos = j, i
        if orientation == Orientation.VERTICAL:
          xPos, yPos = i, j

        tile = self.board.getTile(xPos, yPos)
        
        if tile != None:
          self.updatePlayableTileSpace(tile, orientation, direction, start, j, xPos, yPos, perp = True)
          break
        
        dist += 1
        
      dists[i] = dist
    return dists
          

  def updatePlayableTileSpace(self, tile, orientation, direction, playPos, i, xPos, yPos, perp = False):
    if tile.getOrientation() == orientation:
      # We only need to update if the tile is perpendicular to the play
      # which means the next play on it would be parallel
      if direction == "before":
        self.board.updateTileAfter(xPos, yPos, playPos-i-2)
      else:
        self.board.updateTileBefore(xPos, yPos, i-playPos-2)

p1, p2 = Player(), Player()
g = Game(p1, p2)

def generatePlay():
  x, y = random.randrange(19), random.randrange(19)
  orientation = random.choice([Orientation.HORIZONTAL, Orientation.VERTICAL])
  play = []
  r = random.randrange(1,6)
  for i in range(r):
    tile = g.dealTile()
    tile.setOrientation(orientation)
    if orientation == Orientation.HORIZONTAL and x+i<19 and g.board.getTile(x+i, y) == None:
      play.append((tile, (x+i, y)))
    elif orientation == Orientation.VERTICAL and y+i<19 and g.board.getTile(x, y+1) == None:
      play.append((tile, (x, y+i)))
  return play

# for p in play:
#   print(p[0].value, p[1])

for i in range(5):
  play = generatePlay()
  g.addPlayToBoard(play)

format = []
for i in range(19):
  format.append([])
  for j in range(19):
    if g.board.getTile(i,j):
      format[i].append(g.board.getTile(i,j).value)
    else:
      format[i].append("")
      
mx = max((len(str(ele)) for sub in format for ele in sub))
i = 0
for row in format:
    print("|".join(["{:<{mx}}".format(ele,mx=mx) for ele in row]), i)
    i+=1

for i in range(19):
  for j in range(19):
    t = g.board.getTile(i, j)
    if t != None:
      print(i, j, t.value, t.before, t.after, t.orientation)
