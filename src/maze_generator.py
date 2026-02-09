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
        mid_height: int = int(height / 2) - 2
        mid_width: int = int(width / 2) - 3
        self.forty_two_gps: list[tuple] = [
            (mid_height + 0, mid_width + 0),
            (mid_height + 1, mid_width + 0),
            (mid_height + 2, mid_width + 0),
            (mid_height + 2, mid_width + 1),
            (mid_height + 2, mid_width + 2),
            (mid_height + 3, mid_width + 2),
            (mid_height + 4, mid_width + 2),
            (mid_height + 0, mid_width + 4),
            (mid_height + 0, mid_width + 5),
            (mid_height + 0, mid_width + 6),
            (mid_height + 1, mid_width + 6),
            (mid_height + 2, mid_width + 6),
            (mid_height + 2, mid_width + 5),
            (mid_height + 2, mid_width + 4),
            (mid_height + 3, mid_width + 4),
            (mid_height + 4, mid_width + 4),
            (mid_height + 4, mid_width + 5),
            (mid_height + 4, mid_width + 6)
        ]
        for coord in self.forty_two_gps:
            y: int
            x: int
            y, x = coord
            self.grid[y][x] |= 15
        # self.forty_two_gps.append((mid_height + 1, mid_width + 3))
        # self.forty_two_gps.append((mid_height + 2, mid_width + 3))
        # self.forty_two_gps.append((mid_height + 3, mid_width + 3))
        # self.forty_two_gps.append((mid_height + 4, mid_width + 3))
        # self.forty_two_gps.append((mid_height + 1, mid_width + 4))
        # self.forty_two_gps.append((mid_height + 1, mid_width + 5))
        # self.forty_two_gps.append((mid_height + 2, mid_width + 5))
        # self.forty_two_gps.append((mid_height + 3, mid_width + 6))

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
            self, x: int, y: int, width: int, height: int,
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

        # Length of wall
        length: int = width if horizontal else height

        # What direction for the wall
        dx: int = 1 if horizontal else 0
        dy: int = 0 if horizontal else 1
        # Direction vers la cellule voisine séparée par le mur
        nx_offset, ny_offset = (0, 1) if horizontal else (1, 0)

        # Where will be the passage in the wall
        # px: int = wx + (rand.randint(0, width - 1) if horizontal else 0)
        # py: int = wy + (0 if horizontal else rand.randint(0, height - 1))
        valid_passages = []
        for i in range(length):
            cx, cy = wx + i * dx, wy + i * dy
            # Un passage est valide si ni la cellule actuelle ni sa voisine de l'autre côté du mur ne sont dans le "42"
            if (cy, cx) not in self.forty_two_gps and (cy + ny_offset, cx + nx_offset) not in self.forty_two_gps:
                valid_passages.append((cx, cy))

        # Si aucun passage n'est possible sur cette ligne, on change de ligne ou on annule la division
        if not valid_passages:
            return

        px, py = rand.choice(valid_passages)

        # # Determines which line or column will be modify
        # nl: int = 1 if horizontal else 0
        # nc: int = 0 if horizontal else 1

        # for _ in range(length):
        #     if (wx != px or wy != py):
        #         try:
        #             self.grid[wy][wx] |= chosen_line_card
        #         except IndexError:
        #             raise MazeGenerationErrors(
        #                 "IndexError in that line 'self.grid[wx][wy] |="
        #                 f"chosen_line_card' with {wx=}, {wy=}, {nc=} and"
        #                 f" {nl=}")
        #         try:
        #             self.grid[wy + nl][wx + nc] |= next_line_card
        #         except IndexError:
        #             raise MazeGenerationErrors(
        #                 "IndexError in that line 'self.grid[wx + nc][wy + nl]"
        #                 f" |= next_line_card' with {wx=}, {wy=}, {nc=} and"
        #                 f" {nl=}")
        #     wx += dx
        #     wy += dy

        # # Call for first new side
        # nx: int = x
        # ny: int = y
        # nw: int = width if horizontal else (wx - x + 1)
        # nh: int = (wy - y + 1) if horizontal else height
        # self.divide(self.grid, nx, ny, nw, nh, self.chose_orientation(nw, nh))

        # # Call for second side
        # nx, ny = [x, wy + 1] if horizontal else [wx + 1, y]
        # nw, nh = [width, height - (wy - y) - 1] if horizontal else\
        #     [width - (wx - x) - 1, height]
        # self.divide(self.grid, nx, ny, nw, nh, self.chose_orientation(nw, nh))

        for i in range(length):
            cx, cy = wx + i * dx, wy + i * dy
            if (cx != px or cy != py):
                self.grid[cy][cx] |= chosen_line_card
                self.grid[cy + ny_offset][cx + nx_offset] |= next_line_card

        # Appels récursifs (ajustement des dimensions)
        if horizontal:
            self.divide(x, y, width, wy - y + 1, self.chose_orientation(width, wy - y + 1))
            self.divide(x, wy + 1, width, height - (wy - y) - 1, self.chose_orientation(width, height - (wy - y) - 1))
        else:
            self.divide(x, y, wx - x + 1, height, self.chose_orientation(wx - x + 1, height))
            self.divide(wx + 1, y, width - (wx - x) - 1, height, self.chose_orientation(width - (wx - x) - 1, height))

    def get_maze(self) -> list:
        orientation: Orientation = self.chose_orientation(self.width,
                                                          self.height)
        self.divide(0, 0, self.width, self.height, orientation)
        return self.grid


def main():
    generator = MazeGenerator(20, 15)
    print(generator.grid)
    print(generator.get_maze())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
