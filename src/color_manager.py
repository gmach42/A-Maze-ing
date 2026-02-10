class Colors:
    def __init__(
        self,
        start: int | str,
        end: int | str,
        path: int | str,
        forty_two: int | str,
    ):
        self.start: int = start
        self.end = end
        self.path = path
        self.forty_two = forty_two


class ColorManager:
    """Pre-enregistered colors in MLX format (0xAARRGGBB)"""

    # Basic colors
    WHITE = 0xFFFFFFFF
    BLACK = 0xFF000000
    RED = 0xFFFF0000
    GREEN = 0xFF00FF00
    BLUE = 0xFF0000FF

    # Extended colors
    MAGENTA = 0xFFFF00FF
    CYAN = 0xFF00FFFF
    YELLOW = 0xFFFFFF00
    ORANGE = 0xFFFFA500
    PURPLE = 0xFF800080
    PINK = 0xFFFFC0CB

    # Maze-specific colors
    WALL = 0xFFFFFFFF  # White walls
    BACKGROUND = 0xFF000000  # Black background
    START = 0xFFFF0000  # Red start
    END = 0xFFFF00FF  # Magenta end
    PATH = 0xFF7B68EE  # Medium slate blue path
    OBSTACLE = 0xFF808080  # Gray obstacles
