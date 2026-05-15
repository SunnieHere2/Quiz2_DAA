# constants.py
# Game configuration and constant values

# Window settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

# Grid settings
GRID_SIZE = 15
CELL_SIZE = 40
MINE_COUNT = 35

# Game timing
TIME_LIMIT = 180  # seconds

# Radar power-up
RADAR_RADIUS = 2       # 5x5 area (2 cells in each direction)
RADAR_DURATION = 3000  # 3 seconds in milliseconds
RADAR_USES = 3

# Shield power-up
SHIELD_USES = 2
SHIELD_DURATION = 5000  # 5 seconds in milliseconds

# Hint power-up
HINT_USES = 3
HINT_GLOW_DURATION = 2000  # 2 seconds glow effect

# Colors
WHITE = (255, 255, 255)
GRAY = (189, 189, 189)
DARK_GRAY = (123, 123, 123)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (138, 43, 226)
LIME = (50, 205, 50)
GOLD = (255, 215, 0)
