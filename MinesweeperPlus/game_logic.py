#game_logic.py
# Main game logic and state management
import pygame
import random
from constants import *
from cell import Cell

class Game:
    def __init__(self):
        self.grid = [[Cell(row, col) for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
        self.game_over = False
        self.game_won = False
        self.first_click = True
        self.start_time = None
        self.time_remaining = TIME_LIMIT
        self.flags_placed = 0
        # Power-up variables
        self.radar_uses_left = 0  # Start with 0 power-ups for radar
        self.radar_active = False
        self.radar_start_time = 0
        self.radar_center_row = -1
        self.radar_center_col = -1
        self.radar_mine_count = 0
        self.shield_uses_left = 0  # Start with 0 power-ups for shield
        self.shield_active = False
        self.shield_start_time = 0
        self.hint_uses_left = 0  # Start with 0 power-ups for hint
        self.hint_cell = None
        self.hint_start_time = 0
        # Score system
        self.score = 0
        self.combo = 0  # Track consecutive correct reveals
        self.last_reveal_time = 0  # Track time of last reveal for combo timing
        # Power-up tiles
        self.power_up_tiles = []  # List to store power-up tile positions and types
        # Track potential correct flags for scoring
        self.potential_correct_flags = []

    def place_mines(self, safe_row, safe_col):
        """Place mines, avoiding the first clicked cell (Basic Minesweeper rule hehe)"""
        mines_placed = 0
        while mines_placed < MINE_COUNT:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            if (row == safe_row and col == safe_col) or self.grid[row][col].is_mine:
                continue
            self.grid[row][col].is_mine = True
            mines_placed += 1
        # Calculate neighbor mines
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if not self.grid[row][col].is_mine:
                    self.grid[row][col].neighbor_mines = self.count_neighbor_mines(row, col)
        # Place power-ups after mines are placed
        self.place_power_ups()

    def place_power_ups(self):
        """Place power-ups randomly on the grid (ide dari temen)"""
        power_up_types = ["radar", "shield", "hint"]
        power_up_count = 15 # Number of power-ups to place
        for _ in range(power_up_count):
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            # Ensure the tile is not a mine and not already a power-up
            while self.grid[row][col].is_mine or any(p[0] == (row, col) for p in self.power_up_tiles):
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - 1)
            power_up_type = random.choice(power_up_types)
            self.power_up_tiles.append(((row, col), power_up_type))
            self.grid[row][col].is_power_up = True
            self.grid[row][col].power_up_type = power_up_type

    def activate_power_up(self, power_up_type):
        """Activate the power-up based on its type"""
        if power_up_type == "radar":
            self.radar_uses_left += 1
        elif power_up_type == "shield":
            self.shield_uses_left += 1
        elif power_up_type == "hint":
            self.hint_uses_left += 1

    def count_neighbor_mines(self, row, col):
        """Count mines in the 8 neighboring cells"""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                    if self.grid[new_row][new_col].is_mine:
                        count += 1
        return count

    def activate_radar(self, mouse_x, mouse_y, grid_x, grid_y):
        """Activate radar scan at mouse position"""
        if self.radar_uses_left <= 0 or self.first_click or self.game_over or self.game_won:
            return
        # Calculate grid position relative to the centered grid
        adjusted_x = mouse_x - grid_x
        adjusted_y = mouse_y - grid_y
        # Ensure adjusted_x and adjusted_y are within the grid bounds
        if 0 <= adjusted_x < GRID_SIZE * CELL_SIZE and 0 <= adjusted_y < GRID_SIZE * CELL_SIZE:
            col = adjusted_x // CELL_SIZE
            row = adjusted_y // CELL_SIZE
            mine_count = 0
            for dr in range(-RADAR_RADIUS, RADAR_RADIUS + 1):
                for dc in range(-RADAR_RADIUS, RADAR_RADIUS + 1):
                    check_row = row + dr
                    check_col = col + dc
                    if 0 <= check_row < GRID_SIZE and 0 <= check_col < GRID_SIZE:
                        if self.grid[check_row][check_col].is_mine:
                            mine_count += 1
            self.radar_active = True
            self.radar_start_time = pygame.time.get_ticks()
            self.radar_center_row = row
            self.radar_center_col = col
            self.radar_mine_count = mine_count
            self.radar_uses_left -= 1

    def update_radar(self):
        """Check if radar should be deactivated"""
        if self.radar_active:
            elapsed = pygame.time.get_ticks() - self.radar_start_time
            if elapsed >= RADAR_DURATION:
                self.radar_active = False

    def toggle_shield(self):
        """Activate/deactivate shield"""
        if self.shield_uses_left > 0 and not self.first_click and not self.game_over and not self.game_won:
            if not self.shield_active:
                # Activate shield
                self.shield_active = True
                self.shield_start_time = pygame.time.get_ticks()
            else:
                # Deactivate manually and subtract usage
                self.shield_active = False
                self.shield_uses_left -= 1  # subtract usage immediately

    def update_shield(self):
        """Check if shield should expire"""
        if self.shield_active:
            elapsed = pygame.time.get_ticks() - self.shield_start_time
            if elapsed >= SHIELD_DURATION:
                self.shield_active = False
                if self.shield_uses_left > 0:
                    self.shield_uses_left -= 1

    def use_hint(self):
        """Reveal one random safe cell"""
        if self.hint_uses_left <= 0 or self.first_click or self.game_over or self.game_won:
            return
        safe_cells = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.grid[row][col]
                if not cell.is_revealed and not cell.is_mine and not cell.is_flagged:
                    safe_cells.append((row, col))
        if safe_cells:
            row, col = random.choice(safe_cells)
            self.reveal_cell(row, col)
            self.hint_cell = (row, col)
            self.hint_start_time = pygame.time.get_ticks()
            self.hint_uses_left -= 1

    def update_hint(self):
        """Check if hint glow should disappear"""
        if self.hint_cell:
            elapsed = pygame.time.get_ticks() - self.hint_start_time
            if elapsed >= HINT_GLOW_DURATION:
                self.hint_cell = None

    def reveal_cell(self, row, col):
        """Reveal a cell and cascade if it has no neighboring mines"""
        if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
            return
        cell = self.grid[row][col]
        if cell.is_revealed or cell.is_flagged:
            return
        if self.first_click:
            self.place_mines(row, col)
            self.first_click = False
            self.start_time = pygame.time.get_ticks()
            self.last_reveal_time = pygame.time.get_ticks()
        cell.is_revealed = True
        current_time = pygame.time.get_ticks()
        # Combo logic: Reward faster reveals
        if current_time - self.last_reveal_time < 1000:  # Less than 1 second between reveals
            self.combo += 1
        else:
            self.combo = 0  # Reset combo if too slow
        self.last_reveal_time = current_time
        # Score for revealing a cell
        self.score += 10 + (self.combo * 2)  # Base + combo bonus
        # Check if the revealed cell is a power-up tile
        for power_up_tile in self.power_up_tiles:
            ((power_row, power_col), power_up_type) = power_up_tile
            if power_row == row and power_col == col:
                self.activate_power_up(power_up_type)
                self.power_up_tiles.remove(power_up_tile)  # Remove the power-up tile
                break
        if cell.is_mine:
            if self.shield_active:
                self.shield_active = False
                self.shield_uses_left -= 1
                return
            else:
                self.game_over = True
                self.reveal_all_mines()
                return
        if cell.neighbor_mines == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    self.reveal_cell(row + dr, col + dc)
        self.check_win()

    def reveal_all_mines(self):
        """Reveal all mines when game is lost"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col].is_mine:
                    self.grid[row][col].is_revealed = True

    def toggle_flag(self, row, col):
        """Toggle flag on a cell"""
        if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
            return
        cell = self.grid[row][col]
        if cell.is_revealed:
            return
        if cell.is_flagged:
            cell.is_flagged = False
            self.flags_placed -= 1
            # Remove from potential correct flags if it was tracked
            if (row, col) in self.potential_correct_flags:
                self.potential_correct_flags.remove((row, col))
        else:
            cell.is_flagged = True
            self.flags_placed += 1
            # Track potential correct flags (do not award points yet)
            self.potential_correct_flags.append((row, col))

    def validate_flags(self):
        """Award points for correctly flagged mines at the end of the game"""
        for (row, col) in self.potential_correct_flags:
            if self.grid[row][col].is_mine:
                self.score += 20  # Award points only after validation

    def check_win(self):
        """Check if all non-mine cells are revealed"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.grid[row][col]
                if not cell.is_mine and not cell.is_revealed:
                    return
        self.game_won = True
        self.validate_flags()  # Award points for correct flags only now
        # Time bonus: More points for finishing faster
        time_bonus = self.time_remaining * 5  # 5 points per second remaining
        self.score += time_bonus

    def update_timer(self):
        """Update the countdown timer"""
        if self.first_click or self.game_over or self.game_won:
            return
        elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
        self.time_remaining = TIME_LIMIT - elapsed
        if self.time_remaining <= 0:
            self.time_remaining = 0
            self.game_over = True
            self.reveal_all_mines()
