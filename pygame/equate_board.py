import pygame
import styles
import json
import sys
import os
from equate_tile import Tile

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from constants import TILES

class EquateBoard:
    def __init__(self):
        self.board = []
   
    def init_board(self):
        for i in range(19):
            self.board.append([])
            for j in range(19):
                self.board[i].append(None)

    def generate_tiles(self, tile_values, x_positions=None, y_positions=None):
        tiles = []
        for i, value in enumerate(tile_values):
            x = x_positions[i] if x_positions else None
            y = y_positions[i] if y_positions else None
            points = TILES[self.normalize_value(value)]["points"] if value != "=" else 0
            tiles.append(Tile(value, points, x, y))
        return tiles
    
    def normalize_value(self, value):
        unicode_to_ascii = {
            "\u00d7": "×",  
            "\u00f7": "÷",
        }
        return unicode_to_ascii.get(value, value)

    def seed_plays(self):
        with open("game.json", "r") as file:
            game_data = json.load(file)
        
        plays = []
        play_data = {}
        for play in game_data:
            if play == game_data[0]:
                play_data = {
                    "player1Rack": self.generate_tiles(play["player1"]),
                    "player2Rack": self.generate_tiles(play["player2"]),
                }
            else:
                play_data = {
                    "player": play["player"],
                    "beforeRack": self.generate_tiles(play["beforeRack"]),
                    "afterRack": self.generate_tiles(play["afterRack"]),
                    "play": self.generate_tiles(play["play"], play["xPositions"], play["yPositions"]),
                    "points": play["points"],
                }
            plays.append(play_data)
        return plays

    def draw_top_info(self, screen, points, rack):
        font = pygame.font.SysFont("timesnewroman", 20) 

        # Render text surfaces
        player_surface = font.render("Player 1", True, styles.WHITE)
        points_surface = font.render(f"Points: {points}", True, styles.WHITE)
 
        # Draw text
        screen.blit(player_surface, (10, 10))
        screen.blit(points_surface, (170, 10))

        # Draw vertical separator
        pygame.draw.line(screen, styles.WHITE, (160, 0), (160, 40), 2)
        
        # Draw Advanced Player's rack
        for i in range(len(rack)):
            rack[i].draw(screen, 280 + i * 40, 0)

    def draw_bottom_info(self, screen, points, rack):
        font = pygame.font.SysFont("timesnewroman", 20)

        # Render text surfaces
        player_surface = font.render("Player 2", True, styles.WHITE)
        points_surface = font.render(f"Points: {points}", True, styles.WHITE)

        # Draw text
        screen.blit(player_surface, (10, 808))
        screen.blit(points_surface, (170, 808))

        # Draw vertical separator
        pygame.draw.line(screen, styles.WHITE, (160, 800), (160, 840), 2)
        
        # Draw Simplified Player's rack
        for i in range(len(rack)):
            rack[i].draw(screen, 280 + i * 40, 800)

    def draw_board(self, screen, tiles):
                    
        board_area = pygame.Rect(0, 40, 760, 800 - 40)
        pygame.draw.rect(screen, styles.BKGD, board_area)

        for i in range(20):
            y = 40 + i * 40
            pygame.draw.aaline(screen, styles.TILE, (0, y), (760, y))

        for i in range(19):
            x = i * 40
            pygame.draw.aaline(screen, styles.TILE, (x, 40), (x, 800))

        pygame.draw.aaline(screen, styles.TILE, (759, 40), (759, 800))

        with open("board_data.txt", "r") as file:
            board_data = [line.split() for line in file.readlines()]

        multiplier = pygame.font.SysFont("timesnewroman", 20, bold=True)

        for row in range(19):
            for col in range(19):
                x = col * 40
                y = 40 + row * 40
                tile_rect = pygame.Rect(x, y, 40, 40)
                mult = board_data[row][col]

                match mult:
                    case "2S":
                        pygame.draw.rect(screen, styles.TWO_S, tile_rect)
                    case "3S":
                        pygame.draw.rect(screen, styles.THREE_S, tile_rect)
                    case "2E":
                        pygame.draw.rect(screen, styles.TWO_E, tile_rect)
                    case "3E":
                        pygame.draw.rect(screen, styles.THREE_E, tile_rect)
        
                if mult != "NM":
                    text_surface = multiplier.render(mult, True, styles.WHITE)
                    text_rect = text_surface.get_rect(center=(x + 20, y + 20))
                    screen.blit(text_surface, text_rect)

        # Draw tiles on board that have been played
        for tile in tiles:
            tile.draw(screen, tile.get_x() * 40, tile.get_y() * 40 + 40)

    def draw_game(self, screen, p1_rack, p2_rack, p1_points, p2_points, tiles_on_board):
        screen.fill(styles.WINDOW_BKGD)
        self.draw_top_info(screen, p1_points, p1_rack)
        self.draw_bottom_info(screen, p2_points, p2_rack)
        self.draw_board(screen, tiles_on_board)
        pygame.display.flip()