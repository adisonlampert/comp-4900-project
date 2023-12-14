from copy import deepcopy
import multiprocessing
from constants import MULTIPLIERS, Orientation
from game import Game
from greedy_player import GreedyPlayer

class CheatingPlayer(GreedyPlayer):
  def __init__(self, name):
    super().__init__(name)
    
  def play(self, board, opponent):
    options = super().generate_all_options(board)
    valid_options = super().format_plays(board, options)
    
    del options

    print([t.get_value() for t in super().get_rack()])
    
    best_option, best_play, points, orientation, positions = self.cheat(opponent, board, valid_options)
      
    if best_option != None:
      print("We are strategizing")
      points, best_play, orientation, positions = best_option
      
    play = []
    
    for i, curr_tile in enumerate(best_play):
      if orientation == None:
        break
        
      if orientation == Orientation.HORIZONTAL:
        curr_tile.set_orientation(Orientation.VERTICAL)
      else:
        curr_tile.set_orientation(Orientation.HORIZONTAL)
      
      play.append((curr_tile, positions[i]))
        
    super().remove_played_tiles(best_play)
    
    self.points += points

    return play
    
  def cheat(self, opponent, board, options):
    diff, best_option = 0, None
    highest_play, highest_points, highest_orientation, highest_positions = [], 0, None, []

    for indx, option in enumerate(options):
      print(f"Checking option {indx+1}/{len(options)}")

      points, eq, orientation, positions = option
      play = []

      if points > highest_points:
        highest_points = points
        highest_play = eq
        highest_orientation = orientation
        highest_positions = positions
        
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
      _, highest_opp_points, _, _ = opponent.find_highest_play(cp_board, opp_options)
      
      if points - highest_opp_points >= diff:
        diff = points - highest_points
        best_option = option
    
    return best_option, highest_play, highest_points, highest_orientation, highest_positions
