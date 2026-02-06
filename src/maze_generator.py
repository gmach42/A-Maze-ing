import random
import numpy as np
from .enum2 import Orientation


class MazeGenerator:

    grid: list = np.zeros((20, 15), np.int_)

    def choose_orientation(width: int, height: int) -> Orientation:
        if width < height:
            return Orientation.HORIZONTAL
        elif width > height:
            return Orientation.VERTICAL
        else:
            return Orientation.HORIZONTAL if random.randint(0, 1) == 0 else\
                Orientation.VERTICAL

    def divide(
            grid: list[int], x: int, y: int, width: int, height: int,
            orientation: Orientation
            ):
        pass


def main():
    print(MazeGenerator.grid)


if __name__ == "__main__":
    main()
