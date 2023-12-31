import pygame
import styles

class Tile:
    def __init__(self, value, points, x, y):
        self.value = value
        self.points = points
        self.x = x
        self.y = y

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def draw(self, screen, x, y):
        tile_size = 40
        divider_size = 2 

        # Adjusted rectangle size for the tile (leaving space for divider)
        adjusted_tile_rect = pygame.Rect(x + divider_size, y + divider_size, tile_size - 2*divider_size, tile_size - 2*divider_size)
        pygame.draw.rect(screen, styles.TILE, adjusted_tile_rect)

        # Create font objects
        value_font = pygame.font.SysFont("timesnewroman", 20, bold=True)
        points_font = pygame.font.SysFont("timesnewroman", 10)

        # Render the value text
        value_text = value_font.render(str(self.value), True, styles.BLACK)
        value_text_rect = value_text.get_rect(center=(x + tile_size // 2, y + tile_size // 2))
        screen.blit(value_text, value_text_rect)

        # Render the points text
        points_text = points_font.render(str(self.points), True, styles.BLACK)

        # Adjust bottom right position for points text
        points_text_x = x + tile_size - divider_size - 3
        points_text_y = y + tile_size - divider_size
        points_text_rect = points_text.get_rect(bottomright=(points_text_x, points_text_y))
        screen.blit(points_text, points_text_rect)