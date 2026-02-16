import random as rand
from .utils_algorithm import Cell

# Available to standalone mazegen module
MIN_ROW_42 = 7
MIN_COL_42 = 9


class MazeGenerator:
    """
    The center of maze generation. It contains both algorithms, the usefull
    variables (perfect, width, etc...) and helpfull functions to create maze.

    Attributes:
        grid (list[list[Cell]]): The grid of cells representing the maze
        width (int): The width of the maze in number of cells
        height (int): The height of the maze in number of cells
        boss_list (list[int]): List used for the union-find structure in
            Kruskal's algorithm
        perfect (bool): Flag indicating if the maze should be perfect or not
        list_cells (list[Cell]): List of all cells in the maze
        algo (int): The algorithm to use for maze generation
            (1 for Kruskal, 2 for Depth First Search)
        forty_two_gps (list[tuple[int, int]]): List of coordinates
            of the cells forming the 42 obstacle. If the maze is too small,
            this list will be empty.
    """

    def __init__(self,
                 height: int,
                 width: int,
                 perfect: bool,
                 seed: str | None = None,
                 algo: int = 1):
        """
        Initialize the MazeGenerator with the given parameters and create the
        grid of cells.

        Args:
            height (int): The height of the maze in number of cells
            width (int): The width of the maze in number of cells
            perfect (bool): Flag indicating if the maze should be perfect or
                not
            seed (str | None): Optional seed for random number generation to
                ensure reproducibility
        """
        self.grid: list[list[Cell]] = []
        self.width: int = width
        self.height: int = height
        self.boss_list: list[int] = []
        self.perfect: bool = perfect
        self.list_cells: list[Cell] = []
        self.algo: int = algo
        self.seed: str | None = seed

        mid_height: int = int(height / 2) - 2
        mid_width: int = int(width / 2) - 3
        self.forty_two_gps: list[tuple[int, int]] = [
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
        ] if width >= MIN_COL_42 and height >= MIN_ROW_42 else []

    def find(self, index: int) -> int:
        """Search for the cell's boss. If it isn't its own boss, it will find
        the place of its boss.

        Returns:
            _type_: The cell's boss
        """
        set: int = self.boss_list[index]
        if set == index:
            return index
        self.boss_list[index] = self.find(set)
        return self.boss_list[index]

    def union(self, index_1: int, index_2: int) -> bool:
        """Find the cells's bosses. If they are the same, it do nothing. Else,
        the first cell's boss become the employee of second cell's boss.
        """
        boss_1: int = self.find(index_1)
        boss_2: int = self.find(index_2)
        if boss_1 != boss_2:
            self.boss_list[boss_1] = boss_2
            return True
        return False

    def kruskal(self) -> None:
        """This one will create a list of all breakable walls by checking if
        they belong to the 42 shape or not.
        Then, it will take wall by wall and check if the neighboring cells have
        the same 'boss' (assigned during cell's creation (self.boss_list)). If
        so, it does nothing. If not, it assigns the cell_a's boss to cell_b,
        break the wall between both, and move on to the next wall. The loop
        stops when all cells have the same boss.
        """
        print("Kruskal algorithm in action!!")
        walls_to_broke: list[tuple[int, int, int, int, str]] = []
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

    @staticmethod
    def check_neighbors(right: Cell, left: Cell, top: Cell,
                        bottom: Cell) -> bool:
        """It checks if cell is the center of a 3x3 area.
        """
        return right.get_walls() == 2 and left.get_walls(
        ) == 8 and top.get_walls() == 1 and bottom.get_walls() == 4

    def unperfect(self) -> None:
        """When env variable perfect is False, it take 1/3 of all walls and
        break them while being careful to not open too much areas.
        """
        list_breakable_cells: list[Cell] = [
            cell for cells in self.grid for cell in cells
            if not cell.is_forty_two() and 0 < cell.x < self.width -
            1 and 0 < cell.y < self.height - 1
        ]
        rand.shuffle(list_breakable_cells)
        i: int = 0
        while i < round(len(list_breakable_cells) * 0.3):
            y: int = list_breakable_cells[0].y
            x: int = list_breakable_cells[0].x
            right: Cell = self.grid[y][x + 1]
            left: Cell = self.grid[y][x - 1]
            top: Cell = self.grid[y - 1][x]
            bottom: Cell = self.grid[y + 1][x]
            actual_walls: int = list_breakable_cells[0].get_walls()
            if list_breakable_cells[0].south != 0 and not (
                    actual_walls - list_breakable_cells[0].south
                    == 0) and not bottom.is_forty_two():
                if (bottom.get_walls() - bottom.north) != 0:
                    list_breakable_cells[0].del_south()
                    bottom.del_north()
            elif list_breakable_cells[0].north != 0 and not (
                    actual_walls - list_breakable_cells[0].north
                    == 0) and not top.is_forty_two():
                if (top.get_walls() - top.south) != 0:
                    list_breakable_cells[0].del_north()
                    top.del_south()
            elif list_breakable_cells[0].east != 0 and not (
                    actual_walls - list_breakable_cells[0].east
                    == 0) and not right.is_forty_two():
                if (right.get_walls() - right.west) != 0:
                    list_breakable_cells[0].del_east()
                    right.del_west()
            elif list_breakable_cells[0].west != 0 and not (
                    actual_walls - list_breakable_cells[0].west
                    == 0) and not left.is_forty_two():
                if (left.get_walls() - left.east) != 0:
                    list_breakable_cells[0].del_west()
                    left.del_east()
            else:
                i -= 1
            if list_breakable_cells[0].get_walls() == 0:
                if self.check_neighbors(right, left, top, bottom):
                    list_breakable_cells[0].south = 4
            list_breakable_cells.pop(0)
            i += 1

    def get_maze(self) -> list[list[int]]:
        """It empties the grid before recreate it with new cells. Then it calls
        asked algorithm and break more walls if perfect is false.

        Returns:
            list[list[int]]: The maze in the form of a list of lists of
            integers
        """
        if self.seed:
            rand.seed(self.seed)
        self.grid = []
        for y in range(self.height):
            row: list[Cell] = []
            for x in range(self.width):
                index: int = y * self.width + x
                cell: Cell = Cell(index, x, y)
                row.append(cell)
                if (y, x) in (self.forty_two_gps):
                    cell.set_forty_two()
                    cell.set_is_visited()
            self.grid.append(row)
        if self.algo == 1:
            self.boss_list = list(range(self.width * self.height))
            self.kruskal()
        if self.algo == 2:
            rand_cell: Cell = rand.choice([
                cell for cells in self.grid for cell in cells
                if not cell.is_visited()
            ])
            self.depth_first_search(rand_cell)
        if not self.perfect:
            self.unperfect()
        return [[cell.get_walls() for cell in line] for line in self.grid]

    def depth_first_search(self, start_cell: Cell) -> None:
        """This algo will check all neighbors of the current cell and, if they
        aren't visited yet, break the wall between both and do the same logic
        to the neighbor until all cells are visited.

        Args:
            start_cell (Cell): A randomly cell in all maze
        """
        print("Depth First Search algorithm in action!!")
        stack: list[Cell] = [start_cell]
        start_cell.set_is_visited()

        while stack:
            current: Cell = stack[-1]
            x: int
            y: int
            x, y = current.x, current.y
            neighbors: list[tuple[str, Cell]] = []

            if x > 0:
                neighbor: Cell = self.grid[y][x - 1]
                if not neighbor.is_visited() and not neighbor.is_forty_two():
                    neighbors.append(('W', neighbor))

            if y > 0:
                neighbor = self.grid[y - 1][x]
                if not neighbor.is_visited() and not neighbor.is_forty_two():
                    neighbors.append(('N', neighbor))

            if x < self.width - 1:
                neighbor = self.grid[y][x + 1]
                if not neighbor.is_visited() and not neighbor.is_forty_two():
                    neighbors.append(('E', neighbor))

            if y < self.height - 1:
                neighbor = self.grid[y + 1][x]
                if not neighbor.is_visited() and not neighbor.is_forty_two():
                    neighbors.append(('S', neighbor))

            if neighbors:
                # Chosing neighbor randomly
                direction: str
                next_cell: Cell
                direction, next_cell = rand.choice(neighbors)

                # Deleting walls between cells
                if direction == 'W':
                    current.del_west()
                    next_cell.del_east()
                elif direction == 'N':
                    current.del_north()
                    next_cell.del_south()
                elif direction == 'E':
                    current.del_east()
                    next_cell.del_west()
                elif direction == 'S':
                    current.del_south()
                    next_cell.del_north()

                next_cell.set_is_visited()
                stack.append(next_cell)
            else:
                stack.pop()
