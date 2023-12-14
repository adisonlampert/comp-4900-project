import pygame
from equate_board import EquateBoard
import styles

class EquateGame:
    def __init__(self):
        pygame.init()

    def play(self):
        screen = pygame.display.set_mode((760, 840))
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

        playIndex = 1
        tile_index = 0
        start_delay_time = None
        pause_after_play = False

        while running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if playIndex < len(plays) and not pause_after_play:
                currPlay = plays[playIndex]
                player = currPlay["player"]
                rack = p1Rack if player == "player1" else p2Rack

                points = currPlay["points"]
                if player == "player1":
                    p1Points = points
                else:
                    p2Points = points

                # Timing for displaying tiles
                if start_delay_time is None or current_time - start_delay_time >= 1000:
                    if tile_index < len(currPlay["play"]):
                        tile = currPlay["play"][tile_index]
                        tiles_on_board.append(tile)
                        # Remove tile from rack
                        for rack_tile in rack:
                            if rack_tile.value == tile.value:
                                rack.remove(rack_tile)
                                break
                        board.drawGame(screen, p1Rack, p2Rack, p1Points, p2Points, tiles_on_board)
                        tile_index += 1
                        start_delay_time = current_time
                    else:
                        # Update tile counts after all tiles are placed
                        tileCounts = {}
                        for tile in currPlay["afterRack"]:
                            tileCounts[tile.value] = tileCounts.get(tile.value, 0) + 1

                        currCounts = {}
                        for tile in rack:
                            currCounts[tile.value] = currCounts.get(tile.value, 0) + 1

                        for tile in currPlay["afterRack"]:
                            if currCounts.get(tile.value, 0) < tileCounts[tile.value]:
                                rack.append(tile)
                                currCounts[tile.value] = currCounts.get(tile.value, 0) + 1
                                board.drawGame(screen, p1Rack, p2Rack, p1Points, p2Points, tiles_on_board)
                        pause_after_play = True
                        start_delay_time = current_time

            elif pause_after_play and current_time - start_delay_time >= 3000:
                # Reset for next play
                playIndex += 1
                tile_index = 0
                pause_after_play = False
                start_delay_time = None

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

game = EquateGame()
game.play()
