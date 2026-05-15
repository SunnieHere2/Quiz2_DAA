import pygame
from constants import *

def how_to_play_screen(screen, clock):
    running = True
    font_title = pygame.font.Font(None, 70)
    font_text = pygame.font.Font(None, 40)
    powerup_font = pygame.font.Font(None, 35)

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Draw background
        screen.fill(DARK_GRAY)

        # Title
        title = font_title.render("HOW TO PLAY", True, GOLD)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # Instructions
        instructions = [
            "Left Click: Reveal a cell",
            "Right Click: Place/Remove flag",
            "R: Use Radar",
            "S: Activate Shield",
            "H: Hint",
            "ESC: Return to Main Menu",
        ]

        for i, line in enumerate(instructions):
            text_surf = font_text.render(line, True, WHITE)
            screen.blit(text_surf, (50, 200 + i * 50))

        # Power-up section
        powerup_start_y = 200 + len(instructions) * 50 + 40
        screen.blit(font_text.render("Power-ups on tiles:", True, WHITE), (50, powerup_start_y))

        # Power-up visuals
        powerups = [
            {"color": CYAN, "name": "Radar", "desc": "Shows nearby mines 5x5 area"},
            {"color": LIME, "name": "Hint", "desc": "Reveals a random safe cell"},
            {"color": GOLD, "name": "Shield", "desc": "Protects from mine hit"},
        ]

        for i, pu in enumerate(powerups):
            # Draw a small square representing the power-up
            pygame.draw.rect(screen, pu["color"], (70, powerup_start_y + 50 + i*60, 40, 40))
            # Draw description text
            desc_text = powerup_font.render(f"{pu['name']}: {pu['desc']}", True, WHITE)
            screen.blit(desc_text, (130, powerup_start_y + 50 + i*60 + 5))

        pygame.display.flip()
