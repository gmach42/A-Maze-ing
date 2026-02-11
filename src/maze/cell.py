class Cell:
    def __init__(self, number: int):
        self.north: int = 1
        self.east: int = 2
        self.south: int = 4
        self.west: int = 8
        self.index: int = number
        self.forty_two: bool = False

    def set_forty_two(self):
        self.forty_two = self.forty_two is False

    def del_north(self):
        self.north = 0

    def del_east(self):
        self.east = 0

    def del_south(self):
        self.south = 0

    def del_west(self):
        self.west = 0

    def get_walls(self):
        return self.north + self.east + self.south + self.west

    def set_number(self, number: int):
        self.number = number

    def is_forty_two(self):
        return self.forty_two
