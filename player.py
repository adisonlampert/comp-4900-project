from tile import Tile

class Player:
  def __init__(self, name):
    self.name = name
    self.operators = []
    self.negatives = []
    self.integers = []
    self.fractions = []
    self.points = 0

  def getRack(self):
    return self.operators + self.negatives + self.integers + self.fractions
  
  def getPoints(self):
    return self.points
  
  def

  def getRackSize(self):
    return len(self.operators) + len(self.negatives) + len(self.integers) + len(self.fractions)

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

  def play(self, board, opponent):
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
          for j in range(i-1,-1,-1):
            prev = eq[j]
            if j == 0:
              eq[j] = "(" + eq[j]
              eq[i] = "+" + curr + ")"
            elif not prev.isnumeric():
              eq[j+1] = "(" + eq[j+1]
              eq[i] = "+" + curr + ")"
              break
        else:
          eq[i] = "(" + eq[i] + ")"

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

    return leftExpression == rightExpression

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