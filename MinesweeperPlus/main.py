# main.py
# Entry point and main game loop
import pygame
import sys
from constants import *
from game_logic import Game
from renderer import Renderer
from menu import draw_main_menu, draw_pause_menu
from how_to_play import how_to_play_screen

def main():
    pygame.init()
    # Create window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Minesweeper+")
    clock = pygame.time.Clock()
    # Initialize game and renderer
    game = Game()
    renderer = Renderer(screen)
    # Game state control
    game_state = "menu"  # "menu", "gameplay", "tutorial", "paused"
    running = True
    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        # === Handle events ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # --- MENU STATE ---
            elif game_state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    buttons = [
                        {"text": "Start Game", "y": 300},
                        {"text": "How to Play", "y": 400},
                        {"text": "Quit", "y": 500},
                    ]
                    for b in buttons:
                        rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, b["y"], 300, 60)
                        if rect.collidepoint(mouse_pos):
                            if b["text"] == "Start Game":
                                game = Game()  # reset game
                                game_state = "gameplay"
                            elif b["text"] == "How to Play":
                                game_state = "tutorial"
                            elif b["text"] == "Quit":
                                running = False
            # --- GAMEPLAY STATE ---
            elif game_state == "gameplay":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not game.game_over and not game.game_won:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        grid_x = mouse_x - renderer.grid_x
                        grid_y = mouse_y - renderer.grid_y
                        if 0 <= grid_x < GRID_SIZE * CELL_SIZE and 0 <= grid_y < GRID_SIZE * CELL_SIZE:
                            col = grid_x // CELL_SIZE
                            row = grid_y // CELL_SIZE
                            if event.button == 1:  # Left click
                                game.reveal_cell(row, col)
                            elif event.button == 3:  # Right click
                                game.toggle_flag(row, col)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if game.game_over or game.game_won:
                            game = Game()  # Restart
                    elif event.key == pygame.K_r:
                        if not game.game_over and not game.game_won:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            game.activate_radar(mouse_x, mouse_y, renderer.grid_x, renderer.grid_y)
                    elif event.key == pygame.K_s:
                        game.toggle_shield()
                    elif event.key == pygame.K_h:
                        game.use_hint()
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "menu"  # Return to menu anytime
                    elif event.key == pygame.K_p:
                        game_state = "paused"  # Pause the game
            # --- PAUSED STATE ---
            elif game_state == "paused":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    buttons = draw_pause_menu(screen)
                    for b in buttons:
                        rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, b["y"], 300, 60)
                        if rect.collidepoint(mouse_pos):
                            if b["text"] == "Resume":
                                game_state = "gameplay"
                            elif b["text"] == "Restart":
                                game = Game()  # Reset game
                                game_state = "gameplay"
                            elif b["text"] == "Main Menu":
                                game_state = "menu"
            # --- TUTORIAL STATE ---
            elif game_state == "tutorial":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_state = "menu"

        # === DRAW ===
        if game_state == "menu":
            draw_main_menu(screen)
        elif game_state == "gameplay":
            game.update_timer()
            game.update_radar()
            game.update_shield()
            game.update_hint()
            renderer.draw_game(game)
        elif game_state == "paused":
            draw_pause_menu(screen)
        elif game_state == "tutorial":
            how_to_play_screen(screen, clock)
            game_state = "menu"  # Return to menu after tutorial

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
