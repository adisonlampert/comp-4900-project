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

  def get_value(self):
    return self.value
  
  def get_points(self):
    return self.points
  
  def get_orientation(self):
    return self.orientation
  
  def get_before(self):
    return self.before
  
  def get_after(self):
    return self.after

  def get_type(self):
    return self.type
  
  def is_playable(self):
    if self.before != None and self.after != None:
      return self.after+self.before > 1 and not (self.type == "operator" and (self.before == 0 or self.after == 0))
    else:
      return False
    
  def set_orientation(self, orientation):
    self.orientation = orientation

  def set_before(self, before):
    if self.before == None or before < self.before:
      self.before = before
    self.before = max(self.before, 0)

  def set_after(self, after):
    if self.after == None or after < self.after:
      self.after = after
    self.after = max(self.after, 0)
  
  def __str__(self):
    return f'{self.value}'