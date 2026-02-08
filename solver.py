from enum import IntFlag, auto


class Border(IntFlag):
    EMPTY = 0
    NORTH = auto()  # 0001 = 1
    SOUTH = auto()  # 0010 = 2
    WEST = auto()  # 0100 = 4
    EAST = auto()  # 1000 = 8

    @property
    def corner(self) -> bool:
        """Return a corn if it's a cell with 2 walls"""
        return self in (
            self.NORTH | self.WEST,
            self.NORTH | self.EAST,
            self.SOUTH | self.WEST,
            self.SOUTH | self.EAST,
        )

    @property
    def deadend(self) -> bool:
        """Return a deadend if it's a cell with 3 walls"""
        return self.bit_count == 3

    @property
    def intersection(self) -> bool:
        """Return an intersection if it's a cell with at least 2 entries"""
        return self.bit_count < 2


def transform_to_decimal(maze: list[list[str]]) -> list[list[int]]:
    for cells in maze:
        for i, hex_value in enumerate(cells):
            try:
                cells[i] = int(hex_value, 16)
                if cells[i] < 0 or cells[i] > 15:
                    raise ValueError(f"Impossible Value for cell {cells[i]}")
            except TypeError as e:
                print(f"can't convert {cells[i]}: {e}")
    return maze


def get_neighbors(maze: list[list[int]], cell: tuple) -> list[tuple]:
    row, col = cell
    cell_walls: int = Border(maze[row][col])
    neighbors: list[tuple] = []

    # If no NORTH wall -> there's a NORTH neighbor (checking diff 0001)
    if not (cell_walls & Border.NORTH):
        neighbors.append((row - 1, col))

    # If no SOUTH wall -> there's a SOUTH neighbor (checking diff 0010)
    if not (cell_walls & Border.SOUTH):
        neighbors.append((row + 1, col))

    # If no WEST wall -> there's a WEST neighbor (checking diff 0100)
    if not (cell_walls & Border.WEST):
        neighbors.append((row, col - 1))

    # If no EAST wall -> there's a EAST neighbor (checking diff 1000)
    if not (cell_walls & Border.EAST):
        neighbors.append((row, col + 1))

    return neighbors


def h(cell1: tuple[int, int], cell2: tuple[int, int]):
    """
    Heuristic function chosen here is the manhattan distance
    Calculate the distance between 2 points on a grid by summing the
    absolute differences in their x and y coordinates
    """
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_algorithm(maze: list[list[int]], start: tuple, end: tuple) -> list | None:
    """
    A heap queue (also called a priority queue) is a special data structure
    that allows quick access to the smallest (min-heap) or largest (max-heap) element
    the A* algorithm assign a cost to each cell and calculate the shortest path from this
    the cost of a cell is defined by
    ```math
    f(n) = g(n) + h(n)
    ```
    with
    - f(n): total cost to reach cell n -> The priority of the cell, the lower the better!
    - g(n): actual cost to reach cell n from start
    - h(n): heuristic (or estimated) cost to reach the goal from cell n
    """
    # open_paths: list[(f_score, node)] is a heap to rappidly find the
    # node with the lowest score. Faster than using a classic list
    open_paths: list[(int, tuple)] = [(h(start, end), start)]

    # register the precedent node of each newly accessed node
    came_from = {}

    # regiter the "cost" (g(n)) to each cell visited
    path_cost = {start: 0}

    def reconstruct_path(node: tuple) -> list[tuple]:
        """return the list of nodes of the correct path to reach the end from the start"""
        path = [node]
        while node in came_from:
            node = came_from[node]
            path.append(node)
        # reverse result to get from beginning to end
        path.reverse()
        return path

    while (len(open_paths) > 0):
        # get the best next cell to visit (the one with the lowest priority)
        open_paths.sort()
        _, curr_node = open_paths.pop()
        if curr_node == end:
            goal_path = reconstruct_path(end)
            return goal_path
        neighbors = get_neighbors(maze, curr_node)

        # check all possible neighbor of the current cell and register new ones
        for neighbor in neighbors:
            new_cost = path_cost.get(curr_node) + 1
            if neighbor not in path_cost or new_cost < path_cost[neighbor]:
                path_cost[neighbor] = new_cost
                # f(n) = g(n) + h(n)
                priority = new_cost + h(neighbor, end)
                open_paths.append((priority, neighbor))
                came_from[neighbor] = curr_node


def cardinal_direction(path: list[tuple]) -> str:
    """transform the path into a string of direction"""
    # iterate on the whole path except last node
    directions: str = ""
    for i in range(len(path) - 1):
        curr_row, curr_col = path[i]
        next_row, next_col = path[i + 1]

        # Compare row change
        if next_row < curr_row:
            directions += "N"
        elif next_row > curr_row:
            directions += "S"
        # Compare col change
        elif next_col < curr_col:
            directions += "W"
        elif next_col > curr_col:
            directions += "E"

    return directions


def display_list(lst: list[list]) -> None:
    for line in lst:
        print(line)


def main():
    test_hexa = [
        ['A', 'C', '4', '6'],
        ['4', '3', '7', '0'],
        ['F', 'E', '9', '2']
    ]
    # testing if the hexa transformation works well
    print("\nTesting a decimal converter for a maze input in hexadecimal")
    print(transform_to_decimal(test_hexa))
    print("\nTesting solver for the maze: ")
    maze = [
        [7, 1, 11, 13],
        [5, 8, 5, 10],
        [14, 6, 8, 13],
        [7, 3, 2, 10]
    ]
    start = (0, 0)
    end = (3, 3)
    print("Maze:")
    display_list(maze)
    print(f"\nstart: {start}")
    print(f"end: {end}\n")
    print("Solution:")
    solution = a_star_algorithm(maze, start, end)
    print(solution)
    print(cardinal_direction(solution))


if __name__ == "__main__":
    main()
