import random as rand
from .utils_algorithm import Cell


class MazeGenerator:
    def __init__(self, height: int, width: int):
        self.grid: list[list[Cell]] = []
        self.width: int = width
        self.height: int = height
        self.sets: list[int] = []
        self.cardinal_points: dict = {
            "North": 1,
            "East": 2,
            "South": 4,
            "West": 8,
        }

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
            (mid_height + 4, mid_width + 6),
        ]

    def find(self, index: int) -> int:
        """Search for the cell's boss. If it isn't its own boss, it will find
        the place of its boss.

        Returns:
            _type_: The cell's boss
        """
        set: int = self.sets[index]
        if set == index:
            return index
        self.sets[index] = self.find(set)
        return self.sets[index]

    def union(self, index_1: int, index_2: int) -> bool:
        """Find the cells's bosses. If they are the same, it do nothing. Else,
        the first cell's boss become the employee of second cell's boss.
        """
        boss_1: int = self.find(index_1)
        boss_2: int = self.find(index_2)
        if boss_1 != boss_2:
            self.sets[boss_1] = boss_2
            return True
        return False

    def generate(self):
        walls_to_broke: list[tuple] = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].is_forty_two():
                    continue
                if x < self.width - 1:
                    if not self.grid[y][x + 1].is_forty_two():
                        walls_to_broke.append((y, x, y, x + 1, "East"))
                if y < self.height - 1:
                    if not self.grid[y + 1][x].is_forty_two():
                        walls_to_broke.append((y, x, y + 1, x, "South"))
        rand.shuffle(walls_to_broke)
        for wall in walls_to_broke:
            cy_1: int
            cx_1: int
            cy_2: int
            cx_2: int
            direction: str
            cy_1, cx_1, cy_2, cx_2, direction = wall
            cell_1 = self.grid[cy_1][cx_1]
            cell_2 = self.grid[cy_2][cx_2]
            if self.union(cell_1.index, cell_2.index):
                match direction:
                    case "East":
                        cell_1.del_east()
                        cell_2.del_west()
                    case "South":
                        cell_1.del_south()
                        cell_2.del_north()

    def get_maze(self) -> list:
        self.grid = []
        for y in range(self.height):
            row: list = []
            for x in range(self.width):
                index: int = y * self.width + x
                cell: Cell = Cell(index)
                row.append(cell)
                if (y, x) in (self.forty_two_gps):
                    cell.set_forty_two()
            self.grid.append(row)
        self.sets = list(range(self.width * self.height))
        self.generate()
        return [[cell.get_walls() for cell in line] for line in self.grid]

    # def divide(
    #         self, x: int, y: int, width: int, height: int,
    #         orientation: Orientation
    #         ) -> None:
    #     if width < 2 or height < 2:
    #         return
    #     horizontal: bool = orientation == Orientation.HORIZONTAL
    #     chosen_line_card: int = self.cardinal_points.get("South", 4) if\
    #         horizontal else self.cardinal_points.get("East", 2)
    #     next_line_card: int = self.cardinal_points.get("North", 1) if\
    #         horizontal else self.cardinal_points.get("West", 8)

    #     # -2 because we treat it as index AND we want both halves have at
    #     #  least one cell of width or length
    #     wx: int = x + (0 if horizontal else rand.randint(0, width - 2))
    #     wy: int = y + (rand.randint(0, height - 2) if horizontal else 0)

    #     # Length of wall
    #     length: int = width if horizontal else height

    #     # What direction for the wall
    #     dx: int = 1 if horizontal else 0
    #     dy: int = 0 if horizontal else 1
    #     # Direction vers la cellule voisine séparée par le mur
    #     nx_offset, ny_offset = (0, 1) if horizontal else (1, 0)

    #     # Where will be the passage in the wall
    #     # px: int = wx + (rand.randint(0, width - 1) if horizontal else 0)
    #     # py: int = wy + (0 if horizontal else rand.randint(0, height - 1))
    #     valid_passages = []
    #     for i in range(length):
    #         cx, cy = wx + i * dx, wy + i * dy

    #         # Un passage est valide si ni la cellule actuelle ni sa voisine de
    #         # l'autre côté du mur ne sont dans le "42"
    #         if (cy, cx) not in self.forty_two_gps and\
    #                 (cy + ny_offset, cx + nx_offset) not in self.forty_two_gps:
    #             valid_passages.append((cx, cy))

    #     # Si aucun passage n'est possible sur cette ligne, on change de ligne
    #     # ou on annule la division
    #     if not valid_passages:
    #         return

    #     px, py = rand.choice(valid_passages)

    #     # # Determines which line or column will be modify in second part of
    #     # # for loop
    #     # nl: int = 1 if horizontal else 0
    #     # nc: int = 0 if horizontal else 1

    #     for i in range(length):
    #         cx, cy = wx + i * dx, wy + i * dy
    #         if (cx != px or cy != py):
    #             try:
    #                 self.grid[cy][cx] |= chosen_line_card
    #             except IndexError:
    #                 raise MazeGenerationErrors(
    #                     "IndexError in that line 'self.grid[wx][wy] |="
    #                     f"chosen_line_card' with {wx=}, {wy=}, {ny_offset=}"
    #                     f" and {nx_offset=}")
    #             try:
    #                 self.grid[cy + ny_offset][cx + nx_offset] |= next_line_card
    #             except IndexError:
    #                 raise MazeGenerationErrors(
    #                     "IndexError in that line 'self.grid[wx + nc][wy + nl]"
    #                     f" |= next_line_card' with {cx=}, {cy=}, {ny_offset=}"
    #                     f" and {nx_offset=}")

    #     # Call for first new side
    #     nx: int = x
    #     ny: int = y
    #     nw: int = width if horizontal else (wx - x + 1)
    #     nh: int = (wy - y + 1) if horizontal else height
    #     self.divide(nx, ny, nw, nh, self.chose_orientation(nw, nh))

    #     # Call for second side
    #     nx, ny = [x, wy + 1] if horizontal else [wx + 1, y]
    #     nw, nh = [width, height - (wy - y) - 1] if horizontal else\
    #         [width - (wx - x) - 1, height]
    #     self.divide(nx, ny, nw, nh, self.chose_orientation(nw, nh))


def main():
    generator = MazeGenerator(20, 15)
    print(generator.grid)
    print(generator.get_maze())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
