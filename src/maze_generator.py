import random as rand
import numpy as np
from src.definitions import Orientation
from src.errors import MazeGenerationErrors


class MazeGenerator:

    def __init__(self, height: int, width: int):
        self.grid: list = np.zeros((height, width), np.int_)
        self.width: int = width
        self.height: int = height
        self.cardinal_points: dict = {
            "North": 1,
            "East": 2,
            "South": 4,
            "West": 8
            }
        for n in range(height):
            for i in range(width):
                if n == 0:
                    self.grid[n][i] |= self.cardinal_points.get("North", 1)
                if n == height - 1:
                    self.grid[n][i] |= self.cardinal_points.get("South", 4)
                if i == 0:
                    self.grid[n][i] |= self.cardinal_points.get("West", 8)
                if i == width - 1:
                    self.grid[n][i] |= self.cardinal_points.get("East", 2)

    @staticmethod
    def chose_orientation(width: int, height: int) -> Orientation:
        if width < height:
            return Orientation.HORIZONTAL
        elif width > height:
            return Orientation.VERTICAL
        else:
            return Orientation.HORIZONTAL if rand.randint(0, 1) == 0 else\
                Orientation.VERTICAL

    def divide(
            self, grid: list[int], x: int, y: int, width: int, height: int,
            orientation: Orientation
            ) -> None:
        if width < 2 or height < 2:
            return
        horizontal: bool = orientation == Orientation.HORIZONTAL
        chosen_line_card: int = self.cardinal_points.get("South", 4) if\
            horizontal else self.cardinal_points.get("East", 2)
        next_line_card: int = self.cardinal_points.get("North", 1) if\
            horizontal else self.cardinal_points.get("West", 8)

        # -2 because we treat it as index AND we want both halves have at
        #  least one cell of width or length
        wx: int = x + (0 if horizontal else rand.randint(0, width - 2))
        wy: int = y + (rand.randint(0, height - 2) if horizontal else 0)

        # Where will be the passage in the wall
        px: int = wx + (rand.randint(0, width - 1) if horizontal else 0)
        py: int = wy + (0 if horizontal else rand.randint(0, height - 1))

        # What direction for the wall
        dx: int = 1 if horizontal else 0
        dy: int = 0 if horizontal else 1

        # Length of wall
        length: int = width if horizontal else height

        # Determines which line or column will be modify
        nl: int = 1 if horizontal else 0
        nc: int = 0 if horizontal else 1

        for _ in range(length):
            # À voir pour le and, peut-être or
            if (wx != px or wy != py):
                try:
                    self.grid[wy][wx] |= chosen_line_card
                except IndexError:
                    raise MazeGenerationErrors(
                        "IndexError in that line 'self.grid[wx][wy] |="
                        f"chosen_line_card' with {wx=}, {wy=}, {nc=} and"
                        f" {nl=}")
                try:
                    self.grid[wy + nl][wx + nc] |= next_line_card
                except IndexError:
                    raise MazeGenerationErrors(
                        "IndexError in that line 'self.grid[wx + nc][wy + nl]"
                        f" |= next_line_card' with {wx=}, {wy=}, {nc=} and"
                        f" {nl=}")
            wx += dx
            wy += dy

        # Call for first new side
        nx: int = x
        ny: int = y
        nw: int = width if horizontal else (wx - x + 1)
        nh: int = (wy - y + 1) if horizontal else height
        self.divide(self.grid, nx, ny, nw, nh, self.chose_orientation(nw, nh))

        # Call for second side
        nx, ny = [x, wy + 1] if horizontal else [wx + 1, y]
        nw, nh = [width, height - (wy - y) - 1] if horizontal else\
            [width - (wx - x) - 1, height]
        self.divide(self.grid, nx, ny, nw, nh, self.chose_orientation(nw, nh))

    def get_maze(self) -> list:
        orientation: Orientation = self.chose_orientation(self.width,
                                                          self.height)
        self.divide(self.grid, 0, 0, self.width, self.height, orientation)
        return self.grid


def main():
    generator = MazeGenerator(5, 5)
    print(generator.grid)
    print(generator.get_maze())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
