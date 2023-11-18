from tile import Tile

class Player:
  def __init__(self):
    self.operators = []
    self.negatives = []
    self.integers = []
    self.fractions = []
    self.points = 0

  def getRack(self):
    return self.operators + self.negatives + self.integers + self.fractions
  
  def getPoints(self):
    return self.points

  def drawTile(self, tile):
    match tile.getType():
      case "operator":
        self.operators.append(tile)
      case "negative":
        self.negatives.append(tile)
      case "integer":
        self.integers.append(tile)
      case "fraction":
        self.fractions.append(tile)

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
  
  def validatePlay(self, play):
    # Format fractions
    eq = []
    for i in range(len(play)):
      curr = play[i].getValue()
      eq.append(curr)
      if "/" in curr and i > 0:
        if eq[i-1].isnumeric():
          for j in range(i-1,0,-1):
            prev = eq[j]
            if not prev.isnumeric():
              eq[j+1] = "(" + eq[j+1]
              eq[i] = "+" + curr + ")"
              break

    # Split equation into expressions to be evaluated and compared for equality
    equation = "".join([e for e in eq]).replace("×", "*").replace("÷","/")

    expressions = equation.split("=")

    # Get the value of the expressions to compare
    try:
      leftExpression = float(eval(expressions[0]))
      rightExpression = float(eval(expressions[1]))
    except:
      return False
    
    if leftExpression != rightExpression:
      return False
    
    return True