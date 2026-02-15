class ColorManager:
    """Pre-enregistered colors in MLX format (0xAARRGGBB)"""

    # Basic colors
    WHITE = 0xFFFFFFFF
    GRAY = 0xFF808080
    BLACK = 0xFF000000
    RED = 0xFFFF0000
    GREEN = 0xFF00FF00
    BLUE = 0xFF0000FF

    # Extended colors
    MAGENTA = 0xFFFF00FF
    LIGHTCORAL = 0xFFF08080
    CYAN = 0xFF00FFFF
    SLATEBLUE = 0xFF7B68EE
    YELLOW = 0xFFFFFF00
    SANDYBROWN = 0xFFF4A460
    ORANGE = 0xFFFFA500
    PURPLE = 0xFF800080
    PINK = 0xFFFFC0CB
    LIGHTBLUE = 0xBB5000FF
    LIGHTPURPLE = 0xFF8060C0

    # Pastel colors
    PASTEL_RED = 0xFFFF6961
    PASTEL_GREEN = 0xFF77DD77
    PASTEL_BLUE = 0xFFAEC6CF

    # Terrain colors
    DARKGRASS = 0xFF7C8D4C
    LIGHTGRASS = 0xFFB5BA61
    EARTH = 0xFF725428
    BEIGE = 0xFFE5D9C2
    SKY = 0xFFB6E3DB

    # Maze-default colors
    WALL = WHITE
    BACKGROUND = BLACK
    START = RED
    END = MAGENTA
    PATH = SLATEBLUE
    OBSTACLE = GRAY
    BUTTON = LIGHTBLUE
    PANEL = LIGHTPURPLE

    # Predefined color lists for cycling through colors for the maze and 42
    COLOR_LIST = [
        WHITE,
        GRAY,
        BEIGE,
        RED,
        PASTEL_RED,
        LIGHTCORAL,
        ORANGE,
        SANDYBROWN,
        EARTH,
        YELLOW,
        LIGHTGRASS,
        GREEN,
        DARKGRASS,
        PASTEL_GREEN,
        SKY,
        CYAN,
        PASTEL_BLUE,
        LIGHTBLUE,
        LIGHTPURPLE,
        SLATEBLUE,
        BLUE,
        PURPLE,
        MAGENTA,
        PINK,
    ]

    # Predefined color combinations for the solution path (start, end, path)
    PATH_COLOR_LIST = [
        (START, END, PATH),
        (RED, GREEN, BLUE),
        (PASTEL_RED, PASTEL_GREEN, PASTEL_BLUE),
        (LIGHTCORAL, LIGHTGRASS, SKY),
        (ORANGE, DARKGRASS, EARTH),
        (SANDYBROWN, BEIGE, CYAN),
        (YELLOW, GRAY, SLATEBLUE),
        (EARTH, LIGHTGRASS, SANDYBROWN),
    ]

    # Mapping of color values to their names for display purposes
    COLOR_NAMES = {
        WHITE: "White",
        GRAY: "Gray",
        BLACK: "Black",
        PURPLE: "Purple",
        MAGENTA: "Magenta",
        PINK: "Pink",
        LIGHTCORAL: "LightCoral",
        SANDYBROWN: "SandyBrown",
        RED: "Red",
        ORANGE: "Orange",
        YELLOW: "Yellow",
        GREEN: "Green",
        CYAN: "Cyan",
        SLATEBLUE: "SlateBlue",
        BLUE: "Blue",
        PASTEL_RED: "Pastel Red",
        PASTEL_GREEN: "Pastel Green",
        PASTEL_BLUE: "Pastel Blue",
        DARKGRASS: "Dark Grass",
        LIGHTGRASS: "Light Grass",
        EARTH: "Earth",
        BEIGE: "Beige",
        SKY: "Sky",
        LIGHTBLUE: "Light Blue",
        LIGHTPURPLE: "Light Purple",
    }

    @classmethod
    def get_color_name(cls, color: int) -> str:
        """Return the name of the color given its MLX integer value."""
        return cls.COLOR_NAMES.get(color, f"Unknown color: {color:#0{10}X}")
