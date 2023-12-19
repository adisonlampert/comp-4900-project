from game import Game
from greedy_player import GreedyPlayer
from cheating_player import CheatingPlayer

def play():
  while True:
    p1, p2 = CheatingPlayer("Cheating Player"), GreedyPlayer("Greedy Player")
    g = Game(p1, p2)
    g.start_game()
    print(g)

    while (g.play_round()):
      print(g)

if __name__ == "__main__":
  play()
