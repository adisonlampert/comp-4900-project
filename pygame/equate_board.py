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
        self.initBoard()
   
    def initBoard(self):
        for i in range(19):
            self.board.append([])
            for j in range(19):
                self.board[i].append(None)

    def normalize_value(self, value):
        unicode_to_ascii = {
            "\u00d7": "×",  
            "\u00f7": "÷",
        }
        return unicode_to_ascii.get(value, value)

    def create_tile_objects(self, tile_values, x_positions=None, y_positions=None):
        tile_objects = []
        for i, value in enumerate(tile_values):
            x = x_positions[i] if x_positions else None
            y = y_positions[i] if y_positions else None
            points = TILES[self.normalize_value(value)]["points"] if value != "=" else 0
            tile_objects.append(Tile(value, points, x, y))
        return tile_objects

    def seedPlays(self):
        with open("game.json", "r") as file:
            game_data = json.load(file)
        
        plays = []

        for play in game_data:
            if play == game_data[0]:
                play_data = {
                    "player1Rack": self.create_tile_objects(play["player1"]),
                    "player2Rack": self.create_tile_objects(play["player2"]),
                }
                plays.append(play_data)
                continue
                
            play_data = {
                "player": play["player"],
                "beforeRack": self.create_tile_objects(play["beforeRack"]),
                "afterRack": self.create_tile_objects(play["afterRack"]),
                "play": self.create_tile_objects(play["play"], play["xPositions"], play["yPositions"]),
                "points": play["points"],
            }
            plays.append(play_data)
    
        return plays
    
    def drawBoard(self, screen):
                    
        grid_size = 19 
        square_size = 40

        start_y = 40
        end_y = 800  

        board_area = pygame.Rect(0, start_y, 760, end_y - start_y)
        pygame.draw.rect(screen, styles.BKGD, board_area)

        for i in range(grid_size + 1):
            y = start_y + i * square_size
            pygame.draw.aaline(screen, styles.TILE, (0, y), (760, y))

        for i in range(grid_size):
            x = i * square_size
            pygame.draw.aaline(screen, styles.TILE, (x, start_y), (x, end_y))

        pygame.draw.aaline(screen, styles.TILE, (759, start_y), (759, end_y))

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


    def drawTopInfo(self, screen, points):
        font = pygame.font.SysFont("timesnewroman", 20)  # Adjust font size to fit the height

        # Define text
        player_text = "Advanced Player"
        points_text = f"points: {points}"

        # Render text surfaces
        player_surface = font.render(player_text, True, styles.WHITE)
        points_surface = font.render(points_text, True, styles.WHITE)

        # Text positions
        player_x = 10  # Flush left
        separator_1_x = player_x + player_surface.get_width() + 11  # Right after "Advanced Player" + 10px padding
        points_x = separator_1_x + 10  # After first separator + 10px for the separator width
        separator_2_x = points_x + points_surface.get_width() + 38  # Right after "points:" + 10px padding

        # Draw text
        screen.blit(player_surface, (player_x, 10))
        screen.blit(points_surface, (points_x, 10))

        # Draw vertical separators
        pygame.draw.line(screen, styles.WHITE, (separator_1_x, 0), (separator_1_x, 40), 2)  # First separator
        pygame.draw.line(screen, styles.WHITE, (separator_2_x, 0), (separator_2_x, 40), 2)  # Second separator

    def drawBottomInfo(self, screen, points):
        font = pygame.font.SysFont("timesnewroman", 20)

        # Define text
        player_text = "Simplified Player"
        points_text = f"points: {points}"

        # Render text surfaces
        player_surface = font.render(player_text, True, styles.WHITE)
        points_surface = font.render(points_text, True, styles.WHITE)

        # Text positions
        player_x = 10
        separator_1_x = player_x + player_surface.get_width() + 11
        points_x = separator_1_x + 10
        separator_2_x = points_x + points_surface.get_width() + 33

        # Draw text
        screen.blit(player_surface, (player_x, 808))
        screen.blit(points_surface, (points_x, 808))

        # Draw vertical separators
        pygame.draw.line(screen, styles.WHITE, (separator_1_x, 770), (separator_1_x, 840), 2)
        pygame.draw.line(screen, styles.WHITE, (separator_2_x, 770), (separator_2_x, 840), 2)
        

    def drawTopRack(self, screen, rack):
        for i in range(len(rack)):
            rack[i].draw(screen, 280 + i * 40, 0)
        
    def drawBottomRack(self, screen, rack):
        for i in range(len(rack)):
            rack[i].draw(screen, 280 + i * 40, 800)

    def drawTiles(self, screen, tiles):
        for tile in tiles:
            tile.draw(screen, tile.getX() * 40, tile.getY() * 40 + 40)