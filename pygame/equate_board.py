import pygame
import colors

class EquateBoard:
    def __init__(self):
        self.board = []
        self.initBoard()
   
    def initBoard(self):
        # make board 2d array 19x19
        for i in range(19):
            self.board.append([])
            for j in range(19):
                self.board[i].append(None)
    
    def drawBoard(self, screen):
                    
        grid_size = 19 
        square_size = 40

        start_y = 40
        end_y = 800  

        board_area = pygame.Rect(0, start_y, 760, end_y - start_y)
        pygame.draw.rect(screen, colors.BKGD, board_area)

        for i in range(grid_size + 1):
            y = start_y + i * square_size
            pygame.draw.aaline(screen, colors.BLACK, (0, y), (760, y))

        for i in range(grid_size):
            x = i * square_size
            pygame.draw.aaline(screen, colors.BLACK, (x, start_y), (x, end_y))

        pygame.draw.aaline(screen, colors.BLACK, (759, start_y), (759, end_y))

        with open("board_data.txt", "r") as file:
            board_data = [line.split() for line in file.readlines()]

        for row in range(19):
            for col in range(19):
                x = col * 40
                y = 40 + row * 40
                tile_rect = pygame.Rect(x, y, 40, 40)

                if board_data[row][col] == "2S":
                    pygame.draw.rect(screen, colors.TWO_S, tile_rect)
                elif board_data[row][col] == "3S":
                    pygame.draw.rect(screen, colors.THREE_S, tile_rect)
                elif board_data[row][col] == "2E":
                    pygame.draw.rect(screen, colors.TWO_E, tile_rect)
                elif board_data[row][col] == "3E":
                    pygame.draw.rect(screen, colors.THREE_E, tile_rect)