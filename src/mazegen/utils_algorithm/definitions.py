from enum import Enum


class Orientation(Enum):
    """Enum representing the orientation of a wall in the maze."""
    HORIZONTAL = "Horizontal"
    VERTICAL = "Vertical"


class NoSolutionError(Exception):
    pass
