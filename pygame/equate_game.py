import pygame
from equate_board import EquateBoard
import styles

class EquateGame:
    def __init__(self):
        pygame.init()

    def play(self):
        # pygame init
        screen = pygame.display.set_mode((760, 840))
        clock = pygame.time.Clock()
        pygame.display.set_caption("Equate Board Game")
        running = True

        # Initialize board
        board = EquateBoard()
        board.init_board()
        plays = board.seed_plays()

        # Initialize game state
        p1_rack = plays[0]["player1Rack"]
        p2_rack = plays[0]["player2Rack"]
        p1_points = 0
        p2_points = 0

        tiles_on_board = []

        play_index = 1
        tile_index = 0
        start_delay_time = None
        pause_after_play = False

        # Game loop
        while running:
            current_time = pygame.time.get_ticks()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw board
            if play_index < len(plays) and not pause_after_play:
                curr_play = plays[play_index]
                player = curr_play["player"]
                rack = p1_rack if player == "player1" else p2_rack

                # Update points
                points = curr_play["points"]
                if player == "player1":
                    p1_points = points
                else:
                    p2_points = points

                # Time delay displaying tiles sequentially
                if start_delay_time is None or current_time - start_delay_time >= 1000:
                    # Draw tiles on board
                    if tile_index < len(curr_play["play"]):
                        tile = curr_play["play"][tile_index]
                        tiles_on_board.append(tile)
                        # Remove tile from rack
                        for rack_tile in rack:
                            if rack_tile.value == tile.value:
                                rack.remove(rack_tile)
                                break
                        board.draw_game(screen, p1_rack, p2_rack, p1_points, p2_points, tiles_on_board)
                        tile_index += 1
                        start_delay_time = current_time
                    else:
                        # Update tile counts after all tiles are placed
                        tile_counts = {}
                        for tile in curr_play["afterRack"]:
                            tile_counts[tile.value] = tile_counts.get(tile.value, 0) + 1

                        curr_counts = {}
                        for tile in rack:
                            curr_counts[tile.value] = curr_counts.get(tile.value, 0) + 1

                        for tile in curr_play["afterRack"]:
                            if curr_counts.get(tile.value, 0) < tile_counts[tile.value]:
                                rack.append(tile)
                                curr_counts[tile.value] = curr_counts.get(tile.value, 0) + 1
                                board.draw_game(screen, p1_rack, p2_rack, p1_points, p2_points, tiles_on_board)
                        pause_after_play = True
                        start_delay_time = current_time

            elif pause_after_play and current_time - start_delay_time >= 3000:
                # Reset for next play
                play_index += 1
                tile_index = 0
                pause_after_play = False
                start_delay_time = None

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

game = EquateGame()
game.play()
