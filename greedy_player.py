from copy import deepcopy
import math
from player import Player
from constants import Orientation, MULTIPLIERS, BOARD_SIZE
from tile import Tile

class GreedyPlayer(Player):
  def __init__(self, name):
    super().__init__(name)
    
  def generate_all_options(self, board):
    options = []
    tile = None

    for y_pos in range(BOARD_SIZE):
      for x_pos in range(BOARD_SIZE): 
        tile = board.get_tile(x_pos, y_pos)

        if tile is None or not tile.is_playable():
          continue
        
        # print(f'Checking new tile {tile.get_value()} {x_pos, y_pos}, Before: {tile.get_before()}, After: {tile.get_after()}')
        
        playSpace = self.generate_play_space(tile)
        options += self.generate_options(playSpace, tile, x_pos, y_pos)
        
    return options
  
  def find_highest_play(self, board, options):
    highest_play, highest_points, highest_orientation, highest_positions = [], 0, None, []
    
    # Iterate through each option in the list of play options
    for option in options:
      x_tile, y_tile, orientation = option["location"][0], option["location"][1], option["orientation"]
      
      # Iterate through possible equations for the current option
      for eq in option["possible_equations"]:
        points, positions = 0, []
        double_eq, triple_eq = False, False
        tile_index = next((index for (index, tile) in enumerate(eq) if tile.get_orientation() != None), None)
        
        if tile_index == None:
          break
        
        # Iterate through tiles in the equation
        for indx, tile in enumerate(eq):
          points += tile.get_points()
          
          # Calculate the position of the tile based on orientation
          if orientation == Orientation.HORIZONTAL:
            x_pos = x_tile
            y_pos = y_tile-abs(indx-tile_index) if indx <= tile_index else abs(indx-tile_index)+y_tile
          else:
            x_pos = x_tile-abs(indx-tile_index) if indx <= tile_index else abs(indx-tile_index)+x_tile
            y_pos = y_tile
          
          positions.append((x_pos, y_pos))
          
          coordinates = f"{x_pos},{y_pos}"
          if coordinates in MULTIPLIERS and board.get_tile(x_pos, y_pos) is None:
            mult = MULTIPLIERS[coordinates]
            points += tile.get_points() * (2 if mult == "2S" else 3 if mult == "3S" else 1)
            double_eq = double_eq or (mult == "2E")
            triple_eq = triple_eq or (mult == "3E")

        # Apply multiplier bonuses
        if double_eq:
          points *= 2
        if triple_eq:
          points *= 3
        
        # Update highest play if the current points exceed the current highest
        if points > highest_points:
          if super().validate_play(eq):
            highest_points = points
            highest_play = eq
            highest_orientation = orientation
            highest_positions = positions
    
    return highest_play, highest_points, highest_orientation, highest_positions
  
  def play(self, board, _):
    options = self.generate_all_options(board)
    highest_play, highest_points, highest_orientation, highest_positions = self.find_highest_play(board, options)
    
    play = []
    for i, curr_tile in enumerate(highest_play):
      if highest_orientation == None:
        break
      
      if curr_tile.get_orientation() != None:
        print(f"Playing on tile {curr_tile.get_value()}, Before: {curr_tile.get_before()}, After: {curr_tile.get_after()}")
        
      if highest_orientation == Orientation.HORIZONTAL:
        curr_tile.set_orientation(Orientation.VERTICAL)
      else:
        curr_tile.set_orientation(Orientation.HORIZONTAL)
      
      play.append((curr_tile, highest_positions[i]))
        
    self.remove_played_tiles(highest_play)
    
    self.points += highest_points
    if super().get_rack_size() == 0:
      self.points += 40

    return play
              
  def generate_play_space(self, tile=None):
    play_space = []
    
    if tile == None:
      return [None for _ in range(10)]
    before = min(tile.get_before(), 10)
    for _ in range(before):
      play_space.append(None)
    play_space.append(tile)
    after = min(tile.get_after(), 10)
    for _ in range(after):
      play_space.append(None)
    return play_space
  
  def generate_options(self, play_space, tile, x_pos, y_pos):
    options = []
    
    for i in range(1, len(play_space) - 1):
      b_type = play_space[i-1].get_type() if play_space[i-1] is not None else None
      a_type = play_space[i+1].get_type() if play_space[i+1] is not None else None

      if play_space[i] is not None or (b_type == "operator" or b_type == "negative") or a_type == "operator":
        continue

      cp_pspace = play_space.copy()
      cp_pspace[i] = Tile("=", 0, "equals")
      possible_arrangements = []

      # Operators cannot be the first or last symbol of the equation so our range changes
      space =  False
      if tile.get_type() == "operator" or tile.get_type() == "negative":
        space =  True
        
      if i < len(cp_pspace) - min(10, tile.get_after()):
        for j in range(0, i):
          a_range = len(cp_pspace) - min(10, tile.get_after()) if not space else len(cp_pspace) - min(10, tile.get_after())+1
          for k in range(a_range, min(j+12, len(cp_pspace)+1)):
            possible_arrangements.append(cp_pspace[j:k])
      else:
        bRange = min(10, tile.get_before()) if not space else min(10, tile.get_before())-1
        for j in range(0, bRange):
          for k in range(i+2, min(j+12, len(cp_pspace)+1)):
            possible_arrangements.append(cp_pspace[j:k])
            
      possibilities = self.generate_possible_equations(possible_arrangements)
      options.append({"location": (x_pos, y_pos), "orientation": tile.get_orientation(), "possible_equations": possibilities})
      
    return options
    
  def generate_possible_equations(self, possible_arrangements):
    possibilities = []
    
    for arrangement in possible_arrangements:      
      integers, fractions, negatives, operators = deepcopy(self.integers), deepcopy(self.fractions), deepcopy(self.negatives), deepcopy(self.operators)     
      none_indices = [i for i, x in enumerate(arrangement) if x is None]
      
      # Start the recursive generation process
      self.generate_partial_equations(arrangement.copy(), none_indices, integers, fractions, negatives, operators, possibilities)
        
    return possibilities
  
  def generate_partial_equations(self, curr_eq, remaining_none_indices, integers, fractions, negatives, operators, possibilities):
    if not remaining_none_indices:
      # If there are no remaining None indices, check if the equation is valid
      possibilities.append(curr_eq.copy())
      return

    # Get the next None index to fill
    next_none_index = remaining_none_indices[0]

    # Get playable tiles for the current position
    before = curr_eq[next_none_index-1] if next_none_index-1 >= 0 else None
    after = curr_eq[next_none_index+1] if next_none_index+1 < len(curr_eq) else None
          
    if next_none_index == len(curr_eq)-1:
      playable_tiles = super().get_playable_tiles(integers, fractions, negatives, operators, before=before, after=after, last=True)
    else:
      playable_tiles = super().get_playable_tiles(integers, fractions, negatives, operators, before=before, after=after)
          
    # Return and don't add equation if there are no playable tiles
    if len(playable_tiles) == 0:
      return
    
    for tile in playable_tiles:
      curr_eq[next_none_index] = tile
      
      # Create new lists without the tile we just played
      def cp_rack(rack):
        return [t for t in rack if t != tile]
      
      integers_copy, fractions_copy, negatives_copy, operators_copy =  cp_rack(integers), cp_rack(fractions), cp_rack(negatives), cp_rack(operators)
      
      # Generate permutations for the remaining None indices
      self.generate_partial_equations(curr_eq, remaining_none_indices[1:], integers_copy, fractions_copy, negatives_copy, operators_copy, possibilities)
      
      curr_eq[next_none_index] = None  # Backtrack
      
  def first_play(self):
    options = []
    play_space = [None]*10
    
    for i in range(1, len(play_space) - 1):
      cp_pspace = play_space.copy()
      cp_pspace[i] = Tile("=", 0, "equals") # type: ignore 
      possible_arrangements = []
        
      for j in range(0, i):
        for k in range(i+1, len(cp_pspace)-1):
          if len(cp_pspace[j:k]) > 2:
            possible_arrangements.append(cp_pspace[j:k])
            
      options += self.generate_possible_equations(possible_arrangements)
        
    highest_play, highest_points, highest_positions = [], 0, []
    for option in options: 
      double_eq, triple_eq = False, False
      x_val = 9-math.floor(len(highest_play)/2)
      points = 0
      positions = []
      for tile in option:
        points += tile.get_points()
        positions.append((x_val, 9))
        
        coordinates = f"{x_val},9" 
        if coordinates in MULTIPLIERS:
          mult = MULTIPLIERS[coordinates]
          points += tile.get_points() * (2 if mult == "2S" else 3 if mult == "3S" else 1)
          double_eq = double_eq or (mult == "2E")
          triple_eq= triple_eq or (mult == "3E") 
          
        x_val +=1

      if double_eq:
        points *= 2
      if triple_eq:
        points *= 3

      if points > highest_points:
        if super().validate_play(option):
          highest_play = option
          highest_points = points
          highest_positions = positions
        
    self.remove_played_tiles(highest_play)
    
    if super().get_rack_size() == 0:
      self.points += 40

    play = []
    
    for indx, curr_tile in enumerate(highest_play):
      curr_tile.set_orientation(Orientation.HORIZONTAL)
      play.append((curr_tile, highest_positions[indx]))
    
    self.points += highest_points
      
    return play
  
  def remove_played_tiles(self, highest_play):
    def remove_first_matching_tile(obj, list):
      try:
        array_index, item_index = next(
            ((i, j) for i, array in enumerate(list) for j, item in enumerate(array) if obj.get_value() == item.get_value())
        )
        del list[array_index][item_index]
      except StopIteration:
        pass  # No matching item found
    
    rack = [self.integers, self.fractions, self.operators, self.negatives]
    for i in range(len(highest_play)):
      remove_first_matching_tile(highest_play[i], rack)
      