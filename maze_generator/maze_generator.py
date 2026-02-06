from maze_generator import Orientation as o
import random

class MazeGenerator:

    def choose_orientation(width: int, height: int):
        if width < height:
            return o.HORIZONTAL
        elif width > height:
            return o.VERTICAL
        else:
            return o.HORIZONTAL if random.randint(0, 1) == 0 else o.VERTICAL

    def divide(grid: list, )