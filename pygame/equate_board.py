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
   
    def initBoard(self):
        for i in range(19):
            self.board.append([])
            for j in range(19):
                self.board[i].append(None)

    def generateTiles(self, tile_values, x_positions=None, y_positions=None):
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

    def seedPlays(self):
        with open("game.json", "r") as file:
            game_data = json.load(file)
        
        plays = []
        playData = {}
        for play in game_data:
            if play == game_data[0]:
                playData = {
                    "player1Rack": self.generateTiles(play["player1"]),
                    "player2Rack": self.generateTiles(play["player2"]),
                }
            else:
                playData = {
                    "player": play["player"],
                    "beforeRack": self.generateTiles(play["beforeRack"]),
                    "afterRack": self.generateTiles(play["afterRack"]),
                    "play": self.generateTiles(play["play"], play["xPositions"], play["yPositions"]),
                    "points": play["points"],
                }
            plays.append(playData)
        return plays

    def drawTopInfo(self, screen, points, rack):
        font = pygame.font.SysFont("timesnewroman", 20) 

        # Render text surfaces
        player_surface = font.render("Advanced Player", True, styles.WHITE)
        points_surface = font.render(f"Points: {points}", True, styles.WHITE)
 
        # Draw text
        screen.blit(player_surface, (10, 10))
        screen.blit(points_surface, (170, 10))

        # Draw vertical separator
        pygame.draw.line(screen, styles.WHITE, (160, 0), (160, 40), 2)
        
        # Draw Advanced Player's rack
        for i in range(len(rack)):
            rack[i].draw(screen, 280 + i * 40, 0)

    def drawBottomInfo(self, screen, points, rack):
        font = pygame.font.SysFont("timesnewroman", 20)

        # Render text surfaces
        player_surface = font.render("Simplified Player", True, styles.WHITE)
        points_surface = font.render(f"Points: {points}", True, styles.WHITE)

        # Draw text
        screen.blit(player_surface, (10, 808))
        screen.blit(points_surface, (170, 808))

        # Draw vertical separator
        pygame.draw.line(screen, styles.WHITE, (160, 800), (160, 840), 2)
        
        # Draw Simplified Player's rack
        for i in range(len(rack)):
            rack[i].draw(screen, 280 + i * 40, 800)

    def drawBoard(self, screen, tiles):
                    
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
            tile.draw(screen, tile.getX() * 40, tile.getY() * 40 + 40)