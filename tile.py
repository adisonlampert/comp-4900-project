class Tile:
  def __init__(self, value, points, type = None):
    '''
    For math symbols: +, -, ×, ÷
    '''
    self.value = value
    self.points = points
    self.orientation = None # The orientation of the equation it is part of
    self.before = None
    self.after = None
    self.type = type

  def getValue(self):
    return self.value
  
  def getPoints(self):
    return self.points
  
  def getOrientation(self):
    return self.orientation
  
  def getBefore(self):
    return self.before
  
  def getAfter(self):
    return self.after

  def getType(self):
    return self.type
  
  def isPlayable(self):
    return self.after+self.before > 1
  
  def setOrientation(self, orientation):
    self.orientation = orientation

  def setBefore(self, before):
    self.before = before

  def setAfter(self, after):
    self.after = after
  
  def __str__(self):
    return f'{self.value}'