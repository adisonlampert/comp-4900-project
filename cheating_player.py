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
    overall_highest_opp_points, overall_opp_pos, skip_pos, overall_opp_len = 0, (-1, -1), (-1, -1), set()
    opp_plays =  {}

    for indx, option in enumerate(options):
      points, eq, orientation, positions, _ = option

      print(f"Checking option {indx+1}/{len(options)}")

      if points > highest_points:
        highest_points = points
        highest_play = eq
        highest_orientation = orientation
        highest_positions = positions

      if points < 10 or points < diff: # If we can't get 10 points, don't bother
        continue
      
      if skip_pos == positions[0] and len(option) in overall_opp_len: # We know that this position does not change the outcome
        continue

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
      opp_options = opponent.generate_all_options(cp_board, opp_plays)
      _, highest_opp_points, _, _, opp_plays = opponent.find_highest_play(cp_board, opp_options, opp_plays)

      if highest_opp_points > overall_highest_opp_points:
        overall_highest_opp_points = highest_opp_points
        overall_opp_len = set()
        overall_opp_len.add(len(option))
      elif highest_opp_points == overall_highest_opp_points:
        skip_pos = positions[0]
        overall_opp_len.add(len(option))
      
      if points - highest_opp_points >= diff:
        diff = points - highest_opp_points
        best_option = option
        print("New diff ", diff)
    
    return best_option, highest_play, highest_points, highest_orientation, highest_positions
