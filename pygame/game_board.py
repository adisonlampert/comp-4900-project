
import pygame

# Initialize Pygame
pygame.init()

# Set up the display window
width, height = 800, 600  # Window dimensions
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., black)
    screen.fill((0, 0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
