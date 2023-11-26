
import pygame
from resman import ResourceManager
from equate_board import EquateBoard

class EquateGame:
    def __init__(self):
        pygame.init()

        self.rman = ResourceManager()

    def play(self):
        SIZE = (760, 840)
        screen = pygame.display.set_mode(SIZE)
        clock = pygame.time.Clock()
        running = True
        
        pygame.display.set_caption("Equate Board Game")
        board = EquateBoard()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    pass
                
            screen.fill((0, 0, 0)) # clear screen
            board.drawBoard(screen)
            pygame.display.flip() # update screen
            # clock.tick(60)

        pygame.quit()

game = EquateGame()
game.play()