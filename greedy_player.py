from copy import deepcopy
import math
from player import Player
from constants import Orientation, MULTIPLIERS, BOARD_SIZE, RACK_SIZE
from tile import Tile
import multiprocessing
from itertools import chain

class GreedyPlayer(Player):
  def __init__(self, name):
    super().__init__(name)
    self.num_processes = multiprocessing.cpu_count()
    self.already_generated = set()

  def generate_all_options(self, board, prev_options = {}):
    def args_generator():
      for y_pos in range(BOARD_SIZE):
        for x_pos in range(BOARD_SIZE): 
          tile = board.get_tile(x_pos, y_pos)

          if tile is None or not tile.is_playable():
            continue
          
          if (x_pos, y_pos, min(RACK_SIZE, tile.get_before()), min(RACK_SIZE, tile.get_after())) in prev_options:
            continue
          
          play_space = self.generate_play_space(tile)

          yield (play_space, tile, x_pos, y_pos)

    with multiprocessing.Pool(processes=self.num_processes) as pool:
      options = list(chain.from_iterable(pool.map(self.generate_options, args_generator())))

    return options
  
  def format_play(self, args):
    eq, orientation, x_tile, y_tile, board = args
    points, positions = 0, []
    double_eq, triple_eq = False, False
    tile_index = next((index for (index, tile) in enumerate(eq) if tile.get_orientation() != None), None)

    if tile_index == None:
      return None
    
    # Iterate through tiles in the equation
    for indx, tile in enumerate(eq):
      points += tile.get_points()
      
      # Calculate the position of the tile based on orientation
      offset = abs(indx-tile_index)
      if orientation == Orientation.HORIZONTAL:
        x_pos = x_tile
        y_pos = y_tile-offset if indx <= tile_index else offset+y_tile
      else:
        x_pos = x_tile-offset if indx <= tile_index else offset+x_tile
        y_pos = y_tile
      
      positions.append((x_pos, y_pos))
      
      if (x_pos, y_pos) in MULTIPLIERS and board.get_tile(x_pos, y_pos) is None:
        mult = MULTIPLIERS[(x_pos, y_pos)]
        points += tile.get_points() * (1 if mult == "2S" else 2 if mult == "3S" else 0)
        double_eq = double_eq or (mult == "2E")
        triple_eq = triple_eq or (mult == "3E")

    # Apply multiplier bonuses
    if double_eq:
      points *= 2
    if triple_eq:
      points *= 3

    if len(eq) == RACK_SIZE+2:
      points += 40

    return (points, eq, orientation, positions, tile_index)
  
  def format_plays(self, board, options):
    args = []
    pool = multiprocessing.Pool(processes=self.num_processes)
    
    # Iterate through each option in the list of play options
    for option in options:
      x_tile, y_tile, orientation = option["location"][0], option["location"][1], option["orientation"]
      
      # Iterate through possible equations for the current option
      for eq in option["possible_equations"]:
        args.append((eq, orientation, x_tile, y_tile, board))

    plays = pool.map(self.format_play, args)
    pool.terminate()
    pool.join()

    return plays

  def find_highest_play(self, board, options, prev_options = {}):
    plays = self.format_plays(board, options)

    highest_play, highest_points, highest_orientation, highest_positions = [], 0, None, []
    
    for points, eq, orientation, positions in prev_options:
      if points > highest_points:
        highest_points = points
        highest_play = eq
        highest_orientation = orientation
        highest_positions = positions

    for points, eq, orientation, positions, tile_index in plays:
      # Update highest play if the current points exceed the current highest
      if points > highest_points:
        highest_points = points
        highest_play = eq
        highest_orientation = orientation
        highest_positions = positions
        
      prev_options[(positions[0][0], positions[0][1], eq[tile_index].get_before(), eq[tile_index].get_after())] = (points, eq, orientation, positions)

      prev_play_key = (positions[0][0], positions[0][1], min(RACK_SIZE, eq[tile_index].get_before()), min(RACK_SIZE, eq[tile_index].get_after()))
      if prev_play_key not in prev_options or prev_options[prev_play_key][0] < points:  
        prev_options[prev_play_key] = (points, eq, orientation, positions)

    if highest_points == 0:
      print("No valid plays")
    
    return highest_play, highest_points, highest_orientation, highest_positions, prev_options
  
  def play(self, board, _):
    options = self.generate_all_options(board)
    highest_play, highest_points, highest_orientation, highest_positions, _ = self.find_highest_play(board, options)
    del options
    
    play = []
    for i, curr_tile in enumerate(highest_play):
      if highest_orientation == None:
        break
        
      if highest_orientation == Orientation.HORIZONTAL:
        curr_tile.set_orientation(Orientation.VERTICAL)
      else:
        curr_tile.set_orientation(Orientation.HORIZONTAL)
      
      play.append((curr_tile, highest_positions[i]))
        
    self.remove_played_tiles(highest_play)
    
    self.points += highest_points

    return play
              
  def generate_play_space(self, tile=None):
    play_space = []
    
    if tile == None:
      return [None for _ in range(RACK_SIZE+1)]
    before = min(tile.get_before(), RACK_SIZE+1)
    for _ in range(before):
      play_space.append(None)
    play_space.append(tile)
    after = min(tile.get_after(), RACK_SIZE+1)
    for _ in range(after):
      play_space.append(None)
    return play_space
  
  def generate_options(self, args):
    play_space, tile, x_pos, y_pos = args
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
        
      if i < len(cp_pspace) - min(RACK_SIZE+1, tile.get_after()):
        for j in range(0, i):
          a_range = len(cp_pspace) - min(RACK_SIZE+1, tile.get_after()) if not space else len(cp_pspace) - min(RACK_SIZE+1, tile.get_after())+1
          for k in range(a_range, min(j+12, len(cp_pspace)+1)):
            possible_arrangements.append(cp_pspace[j:k])
      else:
        b_range = min(RACK_SIZE+1, tile.get_before())+1 if not space else min(RACK_SIZE+1, tile.get_before())
        for j in range(0, b_range):
          for k in range(i+2, min(j+12, len(cp_pspace)+1)):
            possible_arrangements.append(cp_pspace[j:k])
            
      possibilities = list(self.generate_possible_equations(possible_arrangements))
      self.already_generated = set()
      options.append({"location": (x_pos, y_pos), "orientation": tile.get_orientation(), "possible_equations": possibilities})
      
    return options
    
  def generate_possible_equations(self, possible_arrangements):
    for arrangement in possible_arrangements:      
      integers, fractions, negatives, operators = self.integers.copy(), self.fractions.copy(), self.negatives.copy(), self.operators.copy()   
      none_indices = [i for i, x in enumerate(arrangement) if x is None]
      
      # Start the recursive generation process
      possibilities = self.generate_partial_equations(arrangement.copy(), none_indices, integers, fractions, negatives, operators)
      for p in possibilities:
        eq, valid = super().validate_play(p)
        if valid and eq not in self.already_generated:
          self.already_generated.add(eq)
          yield p

      del integers, fractions, negatives, operators
  
  def generate_partial_equations(self, curr_eq, remaining_none_indices, integers, fractions, negatives, operators):
    if not remaining_none_indices:
      yield curr_eq.copy()
      return

    next_none_index = remaining_none_indices[0]

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

      yield from self.generate_partial_equations(curr_eq, remaining_none_indices[1:], integers_copy, fractions_copy, negatives_copy, operators_copy)

      curr_eq[next_none_index] = None  # Backtrack
      
  def first_play(self):
    options = []
    play_space = [None]*(RACK_SIZE+1)
    
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
      x_val = 9-math.floor(len(option)/2)
      points = 0
      positions = []
      for tile in option:
        points += tile.get_points()
        positions.append((x_val, 9))
        
        if (x_val,9) in MULTIPLIERS:
          mult = MULTIPLIERS[(x_val,9)]
          points += tile.get_points() * (1 if mult == "2S" else 2 if mult == "3S" else 0)
          double_eq = double_eq or (mult == "2E")
          triple_eq = triple_eq or (mult == "3E") 
          
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
      