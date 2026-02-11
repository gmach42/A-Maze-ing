from enum import IntFlag


class Border(IntFlag):
    EMPTY = 0
    NORTH = 0b0001  # NORTH = 1
    EAST = 0b0010  # EAST = 2
    SOUTH = 0b0100  # SOUTH = 4
    WEST = 0b1000  # WEST = 8
