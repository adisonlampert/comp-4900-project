from tile import Tile
from constants import TILES
import random


class Game:
  def __init__(self):
    self.tiles = []
    for tile in TILES:
      for _ in range(TILES[tile]["frequency"]):
        self.tiles.append(Tile(tile, TILES[tile]["points"]))
    random.shuffle(self.tiles) # Shuffles the tiles