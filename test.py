from game import Game
from greedy_player import GreedyPlayer
from cheating_player import CheatingPlayer
import cProfile, pstats, io

def profiled_play():
  p1, p2 = GreedyPlayer("Greedy Player 1"), GreedyPlayer("Greedy Player 2")
  g = Game(p1, p2)
  g.start_game()
  print(g)

  while (g.play_round()):
    print(g)

if __name__ == "__main__":
  # pr = cProfile.Profile()
  # pr.enable()
  profiled_play()
  # pr.disable()
  # s = io.StringIO()
  # sortby = 'cumulative'
  # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
  # ps.print_stats()
  # print(s.getvalue())