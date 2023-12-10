import random
from constants import Orientation
from game import Game
from greedy_player import GreedyPlayer
from cheating_player import CheatingPlayer
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
    g.startGame()
    g.playRound()

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

    for _ in range(9):
      player.drawTile(game.deal_tile())
    
    x, y = random.randrange(19), random.randrange(19)
    orientation = Orientation.VERTICAL
    
    tile = game.deal_tile()
    tile.setOrientation(orientation)
    game.add_play_to_board([(tile, (x, y))])
    
    for i in range(19):
      for j in range(19):
        if game.board != None:
          tile = game.board.get_tile(j,i)
          if tile is not None:
            print(f'Tile: {tile.get_value()} ({j}, {i}), Orientation: {tile.get_orientation()}')

    play = player.play(game.board)
    
    points = 0
    for p in play:
      print(f'{p[0].getValue()} {p[1][0], p[1][1]}')
      points += p[0].getPoints()
    print(f'Points: {points}')
    
    player = Player()
    player.validate_play([p[0] for p in play])
    
    
  def testFirstPlay(self, player):
    game  = Game(player, player)

    for _ in range(9):
      player.draw_tile(game.deal_tile())
      
    play = player.first_play()
    
    points = 0
    for p in play:
      print(f'{p[0].get_value()} {p[1][0], p[1][1]}')
      points += p[0].get_points()
    print(f'Points: {points}')
    
    if points == 0:
      print([t.getValue() for t in player.operators])
      print([t.getValue() for t in player.negatives])
      print([t.getValue() for t in player.integers])
      print([t.getValue() for t in player.fractions])

test = Test()

# Tests that the Game class sets the before and after of tiles appropriately
while(True):
  file = open('cheating_data.txt', 'a+') 
  p1, p2 = GreedyPlayer("Greedy Player"), CheatingPlayer("Cheating Player")
  g = Game(p1, p2)
  g.start_game()
  print(g)

  while (g.play_round()):
    print(g)
  file.write(str(g))
  file.close()
