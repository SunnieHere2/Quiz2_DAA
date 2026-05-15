# menu.py
# Menu rendering functions
import pygame
from constants import *

def draw_main_menu(screen):
    screen.fill(DARK_GRAY)
    # Fonts
    title_font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 50)
    # Title text
    title_text = title_font.render("MINESWEEPER+", True, GOLD)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
    screen.blit(title_text, title_rect)
    # Buttons (rectangles + text)
    buttons = [
        {"text": "Start Game", "y": 300},
        {"text": "How to Play", "y": 400},
        {"text": "Quit", "y": 500},
    ]
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for b in buttons:
        rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, b["y"], 300, 60)
        color = ORANGE if rect.collidepoint(mouse_x, mouse_y) else GRAY
        pygame.draw.rect(screen, color, rect, border_radius=15)
        text = button_font.render(b["text"], True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
    return buttons

def draw_pause_menu(screen):
    screen.fill(DARK_GRAY)
    title_font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 50)

    # Title
    title_text = title_font.render("PAUSED", True, GOLD)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
    screen.blit(title_text, title_rect)

    # Buttons
    buttons = [
        {"text": "Resume", "y": 300},
        {"text": "Restart", "y": 400},
        {"text": "Main Menu", "y": 500},
    ]

    mouse_x, mouse_y = pygame.mouse.get_pos()
    for b in buttons:
        rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, b["y"], 300, 60)
        color = ORANGE if rect.collidepoint(mouse_x, mouse_y) else GRAY
        pygame.draw.rect(screen, color, rect, border_radius=15)
        text = button_font.render(b["text"], True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    return buttons
