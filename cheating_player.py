from copy import deepcopy
from constants import MULTIPLIERS, Orientation
from game import Game
from greedy_player import GreedyPlayer

class CheatingPlayer(GreedyPlayer):
  def __init__(self, name):
    super().__init__(name)
    
  def firstPlay(self):
    return super().first_play()
    
  def play(self, board, opponent):
    options = super().generate_all_options(board)
    valid_options, highest_option = self.validate_options(board, options)
    
    print("Finished finding valid options")
    
    best_option = self.cheat(opponent, board, valid_options)
    
    best_play, orientation, points, positions = highest_option["play"], highest_option["orientation"], highest_option["points"], highest_option["positions"]
      
    if best_option != None:
      best_play, orientation, points, positions = best_option["play"], best_option["orientation"], best_option["points"], best_option["positions"]
      
    play = []
    
    for i, curr_tile in enumerate(best_play):
      if orientation == None:
        break
      
      if curr_tile.get_orientation() != None:
        print(f"Playing on tile {curr_tile.get_value()}, Before: {curr_tile.get_before()}, After: {curr_tile.get_after()}")
        
      if orientation == Orientation.HORIZONTAL:
        curr_tile.set_orientation(Orientation.VERTICAL)
      else:
        curr_tile.set_orientation(Orientation.HORIZONTAL)
      
      play.append((curr_tile, positions[i]))
        
    super().remove_played_tiles(best_play)
    
    self.points += points
    
    if super().get_rack_size() == 0:
      self.points += 40

    return play
    
  def cheat(self, opponent, board, options):
    diff, best_option = 0, None
    for indx, option in enumerate(options):
      print(f"Checking option {indx+1}/{len(options)}")

      orientation, positions, eq, points = option["orientation"], option["positions"], option["play"], option["points"]
      play = []
        
      for indx, curr_tile in enumerate(eq): 
        if orientation == Orientation.HORIZONTAL:
          curr_tile.set_orientation(Orientation.VERTICAL)
        else:
          curr_tile.set_orientation(Orientation.HORIZONTAL)
        
        play.append((curr_tile, positions[indx]))

      cp_board = deepcopy(board)
      for p in play:
        cp_board.add_tile(p[0], p[1][0], p[1][1])

      cp_board = Game.update_playable_space(play, cp_board)
      opp_options = opponent.generate_all_options(cp_board)
      _, highest_points, _, _ = opponent.find_highest_play(cp_board, opp_options)
      
      if points - highest_points >= diff:
        diff = points - highest_points
        best_option = option
    
    return best_option
    
  def validate_options(self, board, options):
    valid_options = []
    highest_play, highest_points, highest_orientation, highest_positions = [], 0, None, []
    
    for option in options:
      x_tile, y_tile, orientation = option["location"][0], option["location"][1], option["orientation"]
      
      for eq in option["possible_equations"]:
        if super().validate_play(eq):
          points, positions = 0, []
          double_eq, triple_eq = False, False
          
          tile_index = next((index for (index, tile) in enumerate(eq) if tile.get_orientation() != None), None)
          
          if tile_index == None:
            break
          
          for i, t in enumerate(eq):
            points += t.get_points()
            
            if orientation == Orientation.HORIZONTAL:
              x_pos = x_tile
              y_pos = y_tile-abs(i-tile_index) if i <= tile_index else abs(i-tile_index)+y_tile
            else:
              y_pos = y_tile
              x_pos = x_tile-abs(i-tile_index) if i <= tile_index else abs(i-tile_index)+x_tile
            
            positions.append((x_pos, y_pos))
            
            coordinates = f"{x_pos},{y_pos}"
            if coordinates in MULTIPLIERS and board.get_tile(x_pos, y_pos) is None:
              mult = MULTIPLIERS[coordinates]
              points += t.get_points() * (2 if mult == "2S" else 3 if mult == "3S" else 1)
              double_eq = double_eq or (mult == "2E")
              triple_eq = triple_eq or (mult == "3E")

          if double_eq:
            points *= 2
          if triple_eq:
            points *= 3
            
          valid_options.append({
            "points": points,
            "play": eq,
            "orientation": orientation,
            "positions": positions
          })
          
          if points > highest_points:
            highest_points = points
            highest_play = eq
            highest_orientation = orientation
            highest_positions = positions
    
    return valid_options, {
      "play": highest_play,
      "points": highest_points,
      "orientation": highest_orientation,
      "positions": highest_positions
    }   
        