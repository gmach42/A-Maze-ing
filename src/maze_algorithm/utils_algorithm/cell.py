from .border import Border


class Cell:
    """
    Cell class used in the maze generation algorithm. It represents a single
    cell in the maze grid with its coordinates, walls, and other properties.

    Attributes:
        x (int): The x-coordinate of the cell in the maze grid
        y (int): The y-coordinate of the cell in the maze grid
        north (int): Value representing the presence of a north wall
        east (int): Value representing the presence of an east wall
        south (int): Value representing the presence of a south wall
        west (int): Value representing the presence of a west wall
        index (int): Unique index of the cell in the maze grid
        forty_two (bool): Flag to indicate if the cell is a 42 obstacle
        visited (bool): Flag to indicate if the cell has been visited during
            maze generation
    """
    def __init__(self, number: int, x: int, y: int):
        """
        Initialize the Cell with its coordinates and index. All walls are
        initially present, and the cell is not visited.

        Args:
            number (int): Unique index of the cell in the maze grid
            x (int): The x-coordinate of the cell in the maze grid
            y (int): The y-coordinate of the cell in the maze grid
        """
        self.x: int = x
        self.y: int = y
        self.north: int = Border.NORTH
        self.east: int = Border.EAST
        self.south: int = Border.SOUTH
        self.west: int = Border.WEST
        self.index: int = number
        self.forty_two: bool = False
        self.visited: bool = False

    def set_forty_two(self) -> None:
        self.forty_two = True

    def set_is_visited(self) -> None:
        self.visited = True

    def del_north(self) -> None:
        self.north = 0

    def del_east(self) -> None:
        self.east = 0

    def del_south(self) -> None:
        self.south = 0

    def del_west(self) -> None:
        self.west = 0

    def get_walls(self) -> int:
        return self.north + self.east + self.south + self.west

    def set_number(self, number: int) -> None:
        self.number = number

    def is_forty_two(self) -> bool:
        return self.forty_two

    def is_visited(self) -> bool:
        return self.visited
