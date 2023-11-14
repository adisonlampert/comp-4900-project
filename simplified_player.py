from player import Player
from itertools import combinations, permutations

class SimplifiedPlayer(Player):
  def __init__(self):
    super(self)

  def play(self, board):
    highest_score = 0
    highest_equation = []

    for row in board:
      for col in row:

        if col["tile"] == None or not col["tile"].isPlayable():
          continue

        tile = board.getTile(row, col)
        play_space = self.generate_play_space(tile)
    
        for i in range(1, len(play_space) - 1):

          temp_list = list.copy()
          temp_list[i] = "="

          for length in range(3, len(play_space) + 1):
              for start in range(len(play_space) - length + 1):
                  end = start + length
                  sliced_list = temp_list[start:end]

                  if "=" in sliced_list and tile.getValue() in sliced_list and sliced_list[0] != "=" and sliced_list[-1] != "=":
                      # find all indices to permute over
                      none_indices = [index for index, value in enumerate(sliced_list) if value is None]
                      for r in range(1, len(self.rack) + 1):
                          for comb in combinations(self.rack, r):
                              for perm in permutations(comb, r):
                                  temp_sliced_list = sliced_list.copy()
                                  for idx, val in zip(none_indices, perm):
                                      temp_sliced_list[idx] = val
                                  # exclude any equations that have None in between two non-None values
                                  if all(temp_sliced_list.index(None) in [0, len(temp_sliced_list) - 1] for _ in range(temp_sliced_list.count(None))):
                                    temp_score = 0
                                    for j in range(len(temp_sliced_list)):
                                        if temp_sliced_list[j] is not None:
                                            temp_score += temp_sliced_list[j].getPoints()
                                    if temp_score > highest_score:
                                        if super().validatePlay(temp_sliced_list):
                                          highest_score = temp_score
                                          highest_equation = temp_sliced_list

    # remove tiles from rack (first investigate data type of rack)
    return highest_equation
              
  def generate_play_space(self, tile):
    playSpace = []
    for i in range(tile.getBefore()):
      playSpace.append(None)
    playSpace.append(tile.getValue())
    for i in range(tile.getAfter()):
      playSpace.append(None)
    return playSpace