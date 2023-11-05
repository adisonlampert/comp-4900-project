class Tile:
  def __init__(self, value, points):
    '''
    For math symbols: +, -, ×, ÷
    '''
    self.value = value
    self.points = points

  def getValue(self):
    return self.value
  
  def getPoints(self):
    return self.points