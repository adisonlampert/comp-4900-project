from copy import deepcopy

class Board:
  def __init__(self):
    self.board = [[{"tile": None, "multiplier": None}] * 19 for _ in range(19)]

  def addTile(self, tile, xPos, yPos):
    cell = {"tile": deepcopy(tile), "multiplier": self.board[yPos][xPos]["multiplier"]}
    self.board[yPos][xPos] = deepcopy(cell)

  def getTile(self, xPos, yPos):
    return self.board[yPos][xPos]["tile"]
  
  def updateTileBefore(self, xPos, yPos, before):
    self.board[yPos][xPos]["tile"].setBefore(before)
  
  def updateTileAfter(self, xPos, yPos, after):
    self.board[yPos][xPos]["tile"].setAfter(after)