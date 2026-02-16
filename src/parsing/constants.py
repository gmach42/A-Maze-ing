from typing import Final

"""
Module to define all the constants used throughout the program.

Centralize all constants in one place for better maintainability
and readability.

Using `Final` ensures that these constants cannot be modified after
their initial assignment
"""

MIN_PIXEL_WIDTH: Final[int] = 200
MIN_PIXEL_HEIGHT: Final[int] = 90
MIN_ROWS: Final[int] = 3
MIN_COLS: Final[int] = 3
PANEL_WIDTH: Final[int] = 550

MIN_BUTTON_WIDTH: Final[int] = 230
MIN_BUTTON_HEIGHT: Final[int] = 25

MIN_ROW_42: Final[int] = 7
MIN_COL_42: Final[int] = 9

DEFAULT_CELL_SIZE: Final[int] = 40
DEFAULT_WALL_WIDTH: Final[int] = 10
