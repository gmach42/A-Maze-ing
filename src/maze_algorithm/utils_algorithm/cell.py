class Cell:
    def __init__(self, number: int, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.north: int = 1
        self.east: int = 2
        self.south: int = 4
        self.west: int = 8
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
