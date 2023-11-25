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
    
  def __str__(self):
    pr = ""
    format = []
    for i in range(19):
      format.append([])
      for j in range(19):
        if self.getTile(j,i):
          format[i].append(self.getTile(j,i).getValue())
        else:
          format[i].append("")
          
    mx = max((len(str(ele)) for sub in format for ele in sub))
    i = 0
    for row in format:
      pr += f'{"|".join(["{:<{mx}}".format(ele,mx=mx) for ele in row])} {i}\n'
      i+=1
    return pr