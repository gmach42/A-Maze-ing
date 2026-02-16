from enum import IntFlag


class Border(IntFlag):
    """
    Bitmap for the borders of a cell in a maze.

        Each bit represents a direction:
    ```
        - Bit 0 (1): North
        - Bit 1 (2): East
        - Bit 2 (4): South
        - Bit 3 (8): West
    ```
    """
    EMPTY = 0
    NORTH = 0b0001  # NORTH = 1
    EAST = 0b0010  # EAST = 2
    SOUTH = 0b0100  # SOUTH = 4
    WEST = 0b1000  # WEST = 8
