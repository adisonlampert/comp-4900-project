import json
from copy import deepcopy
from tile import Tile
from constants import TILES, Orientation, BOARD_SIZE, RACK_SIZE
from board import Board
import random

class Game:
  def __init__(self, player1, player2):
    # Initialize game state
    self.tiles = []  # List to store bag of tiles
    self.rounds = 0
    self.player1, self.player2 = player1, player2
    self.turn = random.choice([self.player1, self.player2])  # Randomly choose the first player
    self.opponent = None

    # Initialize tiles based on predefined frequencies and points
    for tile in TILES:
      frequency = TILES[tile]["frequency"]
      points = TILES[tile]["points"]
      tile_type = TILES[tile]["type"]
      self.tiles.extend([Tile(tile, points, tile_type) for _ in range(frequency)])

    random.shuffle(self.tiles)  # Shuffles the tiles

    self.board = Board()  # Initialize the game board

  def start_game(self):
    # Draw initial tiles for both players
    for _ in range(RACK_SIZE):
      self.player1.draw_tile(self.deal_tile())
      self.player2.draw_tile(self.deal_tile())
    
    # Determine the first play and add it to the board
    play = self.turn.first_play()
    self.add_play_to_board(play)
    
    # Draw additional tiles for the current player based on the first play
    while self.turn.get_rack_size() != RACK_SIZE:
      self.turn.draw_tile(self.deal_tile())
    
    # Switch the current player and opponent  
    if self.turn == self.player1:
      self.turn, self.opponent = self.player2, self.player1
    else:
      self.turn, self.opponent = self.player1, self.player2
  
  def play_round(self):
    # Player makes a play
    play = self.turn.play(self.board, self.opponent)

    # Check if the player cannot play, signaling the end of the game
    if len(play) == 0 or len(play[0]) == 0: 
      return False # Player cannot play, end the game
    
    # Add the play to the board
    self.add_play_to_board(play)
    
    # Draw additional tiles for the current player based on the play
    while self.turn.get_rack_size() != RACK_SIZE:
      if len(self.tiles) == 0:
        break
      
      self.turn.draw_tile(self.deal_tile())

    # Switch the current player and opponent
    if self.turn == self.player1:
      self.turn, self.opponent = self.player2, self.player1
    else:
      self.turn, self.opponent = self.player1, self.player2
    
    return True
      
  def deal_tile(self):
    return self.tiles.pop(-1)
  
  def add_play_to_board(self, play):
    assert self.board is not None
    
    for p in play:
      self.board.add_tile(p[0], p[1][0], p[1][1])
    
    self.board = Game.update_playable_space(play, deepcopy(self.board))
  
  @staticmethod     
  def update_playable_space(play, board):
    match (play[0][0].get_orientation()):
      case Orientation.HORIZONTAL:
        return Game.update_playable_space_horizontal(play, board)
      case Orientation.VERTICAL:
        return Game.update_playable_space_vertical(play, board)
  
  @staticmethod 
  def update_playable_space_horizontal(play, board):
    # Extract positions of the leftmost and rightmost tiles in the play
    left_x_pos, right_x_pos, y_pos = play[0][1][0], play[-1][1][0], play[0][1][1]
    
    # Update before and after values for horizontal space to the left and right of the play
    board = Game.update_inline_before(left_x_pos, y_pos, Orientation.HORIZONTAL, board)
    board = Game.update_inline_after(left_x_pos, y_pos, Orientation.HORIZONTAL, board)
    
    # For horizontal plays, before and after refer to vertical space above and below each tile
    # Update perpendicular (above and below) before and after values
    b_dists, board = Game.update_perpendicular_before(left_x_pos, right_x_pos, y_pos, Orientation.HORIZONTAL, board)
    a_dists, board = Game.update_perpendicular_after(left_x_pos, right_x_pos, y_pos, Orientation.HORIZONTAL, board)
    
    # Set playable space based on before and after values
    board = Game.set_playable_space(play[0][1][0], play[-1][1][0], b_dists, a_dists, play, board, Orientation.HORIZONTAL)
      
    return board 
      
  @staticmethod  
  def update_playable_space_vertical(play, board):
    # Extract positions of the topmost and bottommost tiles in the play
    x_pos, top_y_pos, bottom_y_pos = play[0][1][0], play[0][1][1], play[-1][1][1]
    
    # Update before and after values for vertical space above and below the play
    board = Game.update_inline_before(x_pos, top_y_pos, Orientation.VERTICAL, board)
    board = Game.update_inline_after(x_pos, top_y_pos, Orientation.VERTICAL, board)
    
    # For vertical plays, before and after refer to horizontal space to the right and left of each tile
    # Update perpendicular (left and right) before and after values
    b_dists, board = Game.update_perpendicular_before(top_y_pos, bottom_y_pos, x_pos, Orientation.VERTICAL, board)
    a_dists, board = Game.update_perpendicular_after(top_y_pos, bottom_y_pos, x_pos, Orientation.VERTICAL, board)

    # Set playable space based on before and after values
    board = Game.set_playable_space(play[0][1][1], play[-1][1][1], b_dists, a_dists, play, board, Orientation.VERTICAL)
    
    return board
  
  @staticmethod 
  def set_playable_space(start_pos, end_pos, b_dists, a_dists, play, board, orientation):
    # Adjust before and after distances based on the start and end positions
    if start_pos == 0:
      b_dists = [18] + b_dists
      a_dists = [18] + a_dists
    if end_pos == 18:
      b_dists = b_dists + [18]
      a_dists = a_dists + [18]

    # Iterate through each tile in the play
    for i in range(len(play)):
      tile, x_pos, y_pos = play[i][0], play[i][1][0], play[i][1][1]
      
      # Check if the tile is a blank tile or has a defined before value
      if tile.get_value() == "=" or tile.get_before() is not None:
        board.update_tile_before(x_pos, y_pos, 0)
        board.update_tile_after(x_pos, y_pos, 0)
      else:
        # Update before and after values based on the minimum distances
        board.update_tile_before(x_pos, y_pos, min(*b_dists[i:i+3]))
        board.update_tile_after(x_pos, y_pos, min(*a_dists[i:i+3]))


      # Check and update adjacent tiles
      if x_pos < 18:
        if y_pos > 0:
          if board.get_tile(x_pos+1, y_pos-1) is not None:
            if orientation == Orientation.HORIZONTAL:
              board.update_tile_before(x_pos, y_pos, 0)
              board.update_tile_before(x_pos+1, y_pos-1, 0)
            else:
              board.update_tile_after(x_pos, y_pos, 0)
              board.update_tile_after(x_pos+1, y_pos-1, 0)
        if y_pos < 18:
          if board.get_tile(x_pos+1, y_pos+1) is not None:
            board.update_tile_after(x_pos, y_pos, 0)
            board.update_tile_before(x_pos+1, y_pos+1, 0)

      if x_pos > 0:
        if y_pos > 0:
          if board.get_tile(x_pos-1, y_pos-1) is not None:
            board.update_tile_before(x_pos, y_pos, 0)
            board.update_tile_after(x_pos-1, y_pos-1, 0)
        if y_pos < 18:
          if board.get_tile(x_pos-1, y_pos+1) is not None:
            if orientation == Orientation.HORIZONTAL:
              board.update_tile_after(x_pos, y_pos, 0)
              board.update_tile_after(x_pos-1, y_pos+1, 0)
            else:
              board.update_tile_before(x_pos, y_pos, 0)
              board.update_tile_before(x_pos-1, y_pos+1, 0)
              
    return board
  
  @staticmethod 
  def update_inline_before(position1, position2, orientation, board):
    # Start at the left/top position and iterate backwards until we reach another
    # tile or the left/top edge of the board
    tiles = [False, False, False]  # Left/top, center, right/bottom

    if position1 == 0:
      tiles[0] = True  # There are no tiles to the left/top of our play
    elif position1 == 18:
      tiles[2] = True  # There are no tiles to the right/bottom of our play

    for i in range(position2-1, -1, -1):
      new_after = position2-i-2

      for j in range(3):
        if not tiles[j]:
          # Determine the position based on orientation
          if orientation == Orientation.HORIZONTAL:
            x_pos, y_pos = i, position1+j-1
          else:
            x_pos, y_pos = position1+j-1, i
          
          # Get the tile at the current position
          tile = board.get_tile(x_pos, y_pos)
          
          if tile is not None:
            tiles[j] = True
            # Check conditions for updating the after value
            if tile.get_value() != "=" and orientation != tile.get_orientation():
              board.update_tile_after(x_pos, y_pos, new_after + (1 if j == 0 or j == 2 else 0))

      if all(tiles):
        break

    return board
  
  @staticmethod 
  def update_inline_after(position1, position2, orientation, board):
    # Start at the left/top position and iterate backwards until we reach another
    # tile or the left/top edge of the board
    tiles = [False, False, False]  # Left/top, center, right/bottom

    # Check if there are no tiles to the left/top or right/bottom of our play
    if position1 == 0:
      tiles[0] = True  # There are no tiles to the left/top of our play
    elif position1 == 18:
      tiles[2] = True  # There are no tiles to the right/bottom of our play

    for i in range(position2+1, BOARD_SIZE):
      new_before = i- position2 - 2

      for j in range(3):
        if not tiles[j]:
          # Determine the position based on orientation
          if orientation == Orientation.HORIZONTAL:
            x_pos, y_pos = i, position1+j-1
          else:
            x_pos, y_pos = position1+j-1, i
          
          # Get the tile at the current position
          tile = board.get_tile(x_pos, y_pos)
          
          if tile is not None:
            tiles[j] = True
            # Check conditions for updating the after value
            if tile.get_value() != "=" and orientation != tile.get_orientation():
              board.update_tile_after(x_pos, y_pos, new_before + (1 if j == 0 or j == 2 else 0))

      if all(tiles):
        break

    return board
  
  @staticmethod 
  def update_perpendicular_after(start_pos, end_pos, static_pos, orientation, board):
    # Initialize a list to store distances
    dists = []
    
    # Define dynamic range to ensure we are never out of bounds
    dynamic_start, dynamic_end = max(start_pos-1, 0), min(end_pos+2, BOARD_SIZE)

    # If orientation is horizontal, i is a value on the x-axis; if orientation is vertical, i is a value on the y-axis
    for i in range(dynamic_start, dynamic_end):
      # If orientation is horizontal, j is a value on the y-axis; if orientation is vertical, j is a value on the x-axis
      for j in range(static_pos+1, BOARD_SIZE):
        # Get the tile at the current position based on orientation
        tile = board.get_tile(i, j) if orientation == Orientation.HORIZONTAL else board.get_tile(j, i)
        
        # Check if there is a tile at that position on the board
        if tile:
          new_before = j-static_pos-2
          
          # Update before value if orientation matches
          if tile.get_orientation() == orientation and tile.get_value() != "=":
            board.update_tile_before(i, j, new_before) if orientation == Orientation.HORIZONTAL else board.update_tile_before(j, i, new_before)
          
          # Append the calculated distance
          dists.append(new_before)
          break
      
      # If no tile is found, append the distance from the tile in the play to the edge of the board
      if len(dists) < (i-dynamic_start+1):
        dists.append(BOARD_SIZE-static_pos-1)

    return dists, board
  
  @staticmethod 
  def update_perpendicular_before(start_pos, end_pos, static_pos, orientation, board):
    dists = []
    dynamic_start, dynamic_end = max(start_pos - 1, 0), min(end_pos + 2, BOARD_SIZE)  # Ensures we are never out of bounds

    # If orientation is horizontal, i is a value on the x-axis; if orientation is vertical, i is a value on the y-axis
    for i in range(dynamic_start, dynamic_end):
      # If orientation is horizontal, j is a value on the y-axis; if orientation is vertical, j is a value on the x-axis
      for j in range(static_pos-1, -1, -1):
        # Get the tile at the current position based on orientation
        tile = board.get_tile(i, j) if orientation == Orientation.HORIZONTAL else board.get_tile(j, i)
        
        # Check if there is a tile at that position on the board
        if tile:
          new_before = static_pos-j-2
          
          # Update before value if orientation matches
          if tile.get_orientation() == orientation and tile.get_value() != "=":
            board.update_tile_after(i, j, new_before) if orientation == Orientation.HORIZONTAL else board.update_tile_after(j, i, new_before)
          
          # Append the calculated distance
          dists.append(new_before)
          break
      
      # If no tile is found, append the distance from the tile in the play to the edge of the board 
      if len(dists) < (i-dynamic_start+1):
        dists.append(static_pos)

    return dists, board
  
  def __str__(self):
    return f'{self.player1.get_name()} points: {self.player1.get_points()}\n{self.player2.get_name()} points: {self.player2.get_points()}\n{self.board}'


# try:
#   with open("game.json", "r") as file:
#     existingGame = json.load(file)
# except (FileNotFoundError, json.JSONDecodeError):
#   existingGame = []
  
# entry = {}
# entry["player"] = self.turn.getName()
# entry["beforeRack"] = [r.getValue() for r in initRack]
# entry["afterRack"] = [r.getValue() for r in self.turn.getRack()]
# entry["play"] = [p[0].getValue() for p in play]
# entry["xPositions"] = [p[1][0] for p in play]
# entry["yPositions"] = [p[1][1] for p in play]
# entry["points"] = self.turn.getPoints()

# existingGame.append(entry)
  
# with open("game.json", "w") as file:
#   json.dump(existingGame, file, indent=2)
