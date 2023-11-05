from tile import Tile

class Player:
  def __init__(self):
    self.tiles = []
    self.points = 0

  def getTiles(self):
    return self.tiles
  
  def getPoints(self):
    return self.points
  
  def drawTile(self, tile):
    self.tiles.append(tile)

  def addPoints(self, points):
    self.points += points

  def play(self, board):
    '''
    Board is 2D array
    Each entry of the array will look like
    {
      multiplier: string
        - "" if no multiplier,
        - "2S" = 2x symbol score,
        - "3S" = 3x symbol score,
        - "2E" = 2x equation score, 
        - "3E = 3x equation score
      value: None || Tile
    }

    This method will create a tile for the equal symbol and include it
    in the returned array

    Return an array of tuples (ordered left to right or up to down):
    [(Tile, (x_pos, y_pos))]
    
    '''

    return []

