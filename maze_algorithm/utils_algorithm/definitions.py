from enum import Enum


class Orientation(Enum):
    HORIZONTAL = "Horizontal"
    VERTICAL = "Vertical"


class NoSolutionError(Exception):
    pass
