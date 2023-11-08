class Tile:
  def __init__(self, value, points):
    '''
    For math symbols: +, -, ×, ÷
    '''
    self.value = value
    self.points = points
    self.orientation = None # The orientation of the equation it is part of
    self.before = None
    self.after = None

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
  
  def setOrientation(self, orientation):
    self.orientation = orientation

  def setBefore(self, before):
    self.before = before

  def setAfter(self, after):
    self.after = after