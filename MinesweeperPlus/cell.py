#cell.py
# Cell class for individual grid cells
import pygame
from constants import *

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0
        self.is_power_up = False
        self.power_up_type = None

    def draw(self, surface, font_medium, x, y):
        # Draw cell background
        if self.is_revealed:
            pygame.draw.rect(surface, DARK_GRAY, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
            # Draw mine or number
            if self.is_mine:
                pygame.draw.circle(surface, RED, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 15)
            elif self.neighbor_mines > 0:
                colors = {
                    1: BLUE, 2: GREEN, 3: RED, 4: (0,0,128),
                    5: (128,0,0), 6: (0,128,128), 7: BLACK, 8: GRAY
                }
                color = colors.get(self.neighbor_mines, BLACK)
                text = font_medium.render(str(self.neighbor_mines), True, color)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                surface.blit(text, text_rect)
        else:
            pygame.draw.rect(surface, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)

        # Draw flag if flagged
        if self.is_flagged:
            pygame.draw.polygon(surface, RED, [
                (x + 15, y + 10),
                (x + 35, y + 20),
                (x + 15, y + 30)
            ])
            pygame.draw.line(surface, BLACK, (x + 15, y + 10), (x + 15, y + 40), 3)

        # Draw power-up icon in the bottom-right corner
        if self.is_revealed and self.is_power_up:
            power_up_size = CELL_SIZE // 4  # smaller to avoid blocking number
            padding = 4
            center_x = x + CELL_SIZE - power_up_size // 2 - padding
            center_y = y + CELL_SIZE - power_up_size // 2 - padding

            color_map = {
                "radar": CYAN,
                "shield": GOLD,
                "hint": LIME
            }
            color = color_map.get(self.power_up_type, WHITE)
            pygame.draw.circle(surface, color, (center_x, center_y), power_up_size // 2)

