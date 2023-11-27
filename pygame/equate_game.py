import pygame
from equate_board import EquateBoard
import styles

class EquateGame:
    def __init__(self):
        pygame.init()

    def play(self):
        screen = pygame.display.set_mode(760, 840)
        clock = pygame.time.Clock()
        pygame.display.set_caption("Equate Board Game")
        running = True

        board = EquateBoard()   
        board.initBoard()
        plays = board.seedPlays()

        p1Rack = plays[0]["player1Rack"]
        p2Rack = plays[0]["player2Rack"]
        p1Points = 0
        p2Points = 0

        tiles_on_board = []

        start_time = pygame.time.get_ticks()  # Record the start time
        current_play_index = 1  # Index to keep track of the current play
        step = 'wait'  # Current step in the game logic

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_time) / 1000  # Convert milliseconds to seconds

            if step == 'wait' and elapsed_time >= 5:

                # 5 seconds have passed, move to the next play
                if current_play_index < len(plays):
                    current_play = plays[current_play_index]
                    player = current_play["player"]
                    rack_before = current_play["beforeRack"]
                    if player == "player1":
                        p1Rack = rack_before
                    else:
                        p2Rack = rack_before

                    step = 'add_tiles'
                    start_time = current_time  # Reset the start time for the next step

            elif step == 'add_tiles' and elapsed_time >= 3:
                # 3 seconds have passed, add tiles to the board
                tiles_on_board += current_play["play"]

                step = 'update_points'
                start_time = current_time  # Reset the start time for the next step

            elif step == 'update_points' and elapsed_time >= 2:
                # 2 seconds have passed, update points and racks
                if player == "player1":
                    p1Points = current_play["points"]
                    p1Rack = current_play["afterRack"]
                else:
                    p2Points = current_play["points"]
                    p2Rack = current_play["afterRack"]

                step = 'wait'
                current_play_index += 1
                start_time = current_time  # Reset the start time for the next step

            # Redraw the entire screen here
            screen.fill(styles.WINDOW_BKGD)
            board.drawTopInfo(screen, p1Points, p1Rack)
            board.drawBottomInfo(screen, p2Points, p2Rack)
            board.drawBoard(screen, tiles_on_board)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


game = EquateGame()
game.play()