# renderer.py
# Handles all drawing and rendering
import pygame
from constants import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font_small = pygame.font.Font(None, 30)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_large = pygame.font.Font(None, 60)
        # Calculate centered grid position
        self.grid_x = (WINDOW_WIDTH - GRID_SIZE * CELL_SIZE) // 2
        self.grid_y = (WINDOW_HEIGHT - GRID_SIZE * CELL_SIZE) // 2

    def draw_shield_icon(self, x, y, size, active):
        """Draw a shield icon"""
        color = GOLD if active else GRAY
        points = [
            (x, y),
            (x - size // 2, y + size // 4),
            (x - size // 2, y + size * 3 // 4),
            (x, y + size),
            (x + size // 2, y + size * 3 // 4),
            (x + size // 2, y + size // 4)
        ]
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, BLACK, points, 2)

    def draw_game(self, game):
        """Draw the entire game state"""
        self.screen.fill(DARK_GRAY)
        # Draw title
        title = self.font_large.render("MINESWEEPER+", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
        # Draw score
        score_text = self.font_medium.render(f"Score: {game.score}", True, GOLD)
        self.screen.blit(score_text, (20, 20))
        # Draw grid
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell_x = self.grid_x + col * CELL_SIZE
                cell_y = self.grid_y + row * CELL_SIZE
                game.grid[row][col].draw(self.screen, self.font_medium, cell_x, cell_y)
        # Draw special effects and UI
        self._draw_hint_glow(game)
        self._draw_shield_border(game)
        self._draw_radar_overlay(game)
        self._draw_stats(game)
        self._draw_powerups(game)
        self._draw_end_screen(game)

    def _draw_hint_glow(self, game):
        """Draw the hint glow effect"""
        if game.hint_cell:
            row, col = game.hint_cell
            x = self.grid_x + col * CELL_SIZE
            y = self.grid_y + row * CELL_SIZE
            elapsed = pygame.time.get_ticks() - game.hint_start_time
            alpha = int(255 * (1 - elapsed / HINT_GLOW_DURATION))
            glow = pygame.Surface((CELL_SIZE, CELL_SIZE))
            glow.set_alpha(alpha)
            glow.fill(LIME)
            self.screen.blit(glow, (x, y))
            pygame.draw.rect(self.screen, LIME, (x, y, CELL_SIZE, CELL_SIZE), 5)
            hint_text = self.font_small.render("HINT!", True, LIME)
            hint_rect = hint_text.get_rect(center=(x + CELL_SIZE // 2, y - 15))
            self.screen.blit(hint_text, hint_rect)

    def _draw_shield_border(self, game):
        """Draw shield border when active"""
        if game.shield_active:
            elapsed = pygame.time.get_ticks() - game.shield_start_time
            time_left = (SHIELD_DURATION - elapsed) / 1000
            if time_left > 3:
                border_color = GOLD
            elif time_left > 1:
                border_color = ORANGE
            else:
                border_color = RED
            grid_rect = pygame.Rect(self.grid_x, self.grid_y, GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
            pygame.draw.rect(self.screen, border_color, grid_rect, 5)
            shield_text = self.font_medium.render(f"SHIELD ACTIVE! {time_left:.1f}s", True, border_color)
            shield_rect = shield_text.get_rect(center=(WINDOW_WIDTH // 2, self.grid_y - 20))
            self.screen.blit(shield_text, shield_rect)

    def _draw_radar_overlay(self, game):
        """Draw radar overlay when active"""
        if game.radar_active:
            for dr in range(-RADAR_RADIUS, RADAR_RADIUS + 1):
                for dc in range(-RADAR_RADIUS, RADAR_RADIUS + 1):
                    check_row = game.radar_center_row + dr
                    check_col = game.radar_center_col + dc
                    if 0 <= check_row < GRID_SIZE and 0 <= check_col < GRID_SIZE:
                        x = self.grid_x + check_col * CELL_SIZE
                        y = self.grid_y + check_row * CELL_SIZE
                        overlay = pygame.Surface((CELL_SIZE, CELL_SIZE))
                        overlay.set_alpha(80)
                        overlay.fill(CYAN)
                        self.screen.blit(overlay, (x, y))
                        pygame.draw.rect(self.screen, CYAN, (x, y, CELL_SIZE, CELL_SIZE), 3)
            center_x = self.grid_x + game.radar_center_col * CELL_SIZE + CELL_SIZE // 2
            center_y = self.grid_y + game.radar_center_row * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(self.screen, ORANGE, (center_x, center_y), 25)
            pygame.draw.circle(self.screen, BLACK, (center_x, center_y), 25, 2)
            mine_text = self.font_medium.render(str(game.radar_mine_count), True, BLACK)
            mine_rect = mine_text.get_rect(center=(center_x, center_y))
            self.screen.blit(mine_text, mine_rect)
            time_left = (RADAR_DURATION - (pygame.time.get_ticks() - game.radar_start_time)) / 1000
            radar_timer_text = self.font_small.render(f"Radar: {time_left:.1f}s", True, CYAN)
            self.screen.blit(radar_timer_text, (WINDOW_WIDTH - 180, 15))

    def _draw_stats(self, game):
        """Draw timer, mines, and flags"""
        timer_text = self.font_medium.render(f"Time: {game.time_remaining}s", True, BLACK)
        self.screen.blit(timer_text, (20, WINDOW_HEIGHT - 50))
        mines_text = self.font_medium.render(f"Mines: {MINE_COUNT}", True, BLACK)
        self.screen.blit(mines_text, (200, WINDOW_HEIGHT - 50))
        flags_text = self.font_medium.render(f"Flags: {game.flags_placed}/{MINE_COUNT}", True, BLACK)
        self.screen.blit(flags_text, (380, WINDOW_HEIGHT - 50))

    def _draw_powerups(self, game):
        """Draw power-up status indicators"""
        # Position power-up texts above the grid
        radar_color = CYAN if game.radar_uses_left > 0 else GRAY
        radar_text = self.font_small.render(f"[R] Radar: {game.radar_uses_left}", True, radar_color)
        self.screen.blit(radar_text, (self.grid_x + GRID_SIZE * CELL_SIZE + 25, self.grid_y + 20))

        shield_color = GOLD if game.shield_uses_left > 0 else GRAY
        shield_text = self.font_small.render(f"[S] Shield: {game.shield_uses_left}", True, shield_color)
        self.screen.blit(shield_text, (self.grid_x + GRID_SIZE * CELL_SIZE + 25, self.grid_y + 50))

        hint_color = LIME if game.hint_uses_left > 0 else GRAY
        hint_text = self.font_small.render(f"[H] Hint: {game.hint_uses_left}", True, hint_color)
        self.screen.blit(hint_text, (self.grid_x + GRID_SIZE * CELL_SIZE + 25, self.grid_y + 80))

        # Draw shield icon to the right of the shield text
        shield_icon_x = self.grid_x + GRID_SIZE * CELL_SIZE + 12
        shield_icon_y = self.grid_y + 50
        self.draw_shield_icon(shield_icon_x, shield_icon_y, 15, game.shield_active)

    def _draw_end_screen(self, game):
        """Draw game over or victory screen"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        if game.game_over and not game.game_won:
            self.screen.blit(overlay, (0, 0))
            text = self.font_large.render("GAME OVER!", True, RED)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            self.screen.blit(text, text_rect)
            score_text = self.font_medium.render(f"Final Score: {game.score}", True, GOLD)
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
            self.screen.blit(score_text, score_rect)
            restart_text = self.font_medium.render("Press SPACE to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
            self.screen.blit(restart_text, restart_rect)
        elif game.game_won:
            self.screen.blit(overlay, (0, 0))
            text = self.font_large.render("YOU WIN!", True, GREEN)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            self.screen.blit(text, text_rect)
            score_text = self.font_medium.render(f"Final Score: {game.score}", True, GOLD)
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
            self.screen.blit(score_text, score_rect)
            restart_text = self.font_medium.render("Press SPACE to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
            self.screen.blit(restart_text, restart_rect)
