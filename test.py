import random
from constants import Orientation
from game import Game
from simplified_player import SimplifiedPlayer
from player import Player
from board import Board

class Test:
  def generatePlay(self, g):
    x, y = random.randrange(16), random.randrange(16)
    orientation = random.choice([Orientation.HORIZONTAL, Orientation.VERTICAL])
    play = []
    r = random.randrange(3,7)
    for i in range(r):
      tile = g.dealTile()
      tile.setOrientation(orientation)
      if orientation == Orientation.HORIZONTAL and x+i<19 and g.board.getTile(x+i, y) == None:
        play.append((tile, (x+i, y)))
      elif orientation == Orientation.VERTICAL and y+i<19 and g.board.getTile(x, y+i) == None:
        play.append((tile, (x, y+i)))
    return play

  def testBeforeAfter(self, g):
    for i in range(5):
      play = self.generatePlay(g)
      g.addPlayToBoard(play)

    format = []
    for i in range(19):
      format.append([])
      for j in range(19):
        if g.board.getTile(j,i):
          format[i].append(g.board.getTile(j,i).value)
        else:
          format[i].append("")
          
    mx = max((len(str(ele)) for sub in format for ele in sub))
    i = 0
    for row in format:
        print("|".join(["{:<{mx}}".format(ele,mx=mx) for ele in row]), i)
        i+=1

    for i in range(19):
      for j in range(19):
        t = g.board.getTile(i, j)
        if t != None:
          print(f'Value: {t.value} ({i}, {j})\n    Before: {t.before}\n    After: {t.after}\n    Orientation: {t.orientation}')
          
  def testPlay(self, player):
    game  = Game(player, player)
    
    x, y = random.randrange(19), random.randrange(19)
    orientation = random.choice([Orientation.HORIZONTAL, Orientation.VERTICAL])
    
    tile = game.dealTile()
    tile.setOrientation(orientation)
    game.addPlayToBoard([(tile, (x, y))])

    play = player.play(game.board)
    
    points = 0
    for p in play:
      print(f'{p[0].getValue()} ({p[1][0], p[1][1]})')
      points += p[0].getPoints()
    print(f'Points: {points}')

    # for i in range(19):
    #   for j in range(19):
    #     if game.board.getTile(j, i) != None:
    #       tile = game.board.getTile(j,i)
    #       print(f'{tile.getValue()} ({j}, {i})')

test = Test()

# Tests that the Game class sets the before and after of tiles appropriately
# p1, p2 = Player(), Player()
# g = Game(p1, p2)
# test.testBeforeAfter(g)

# Tests that the player finds the best play
sp = SimplifiedPlayer()
test.testPlay(sp)