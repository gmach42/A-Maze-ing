from enum import IntFlag


class Border(IntFlag):
    EMPTY = 0
    NORTH = 0b0001  # NORTH = 1
    EAST = 0b0010  # EAST = 2
    SOUTH = 0b0100  # SOUTH = 4
    WEST = 0b1000  # WEST = 8


def str_to_decimal(maze: str) -> list[list[int]]:
    """
    Parse string to list[list[char]] then transform each value into decimal
    """
    maze_lst = [list(line) for line in maze.splitlines()]
    return hex_to_decimal(maze_lst)


def hex_to_decimal(maze: list[list[str]]) -> list[list[int]]:
    """Parse hexadecimal maze into a decimal one readable by the algorithm"""
    for cells in maze:
        for i, hex_value in enumerate(cells):
            try:
                cells[i] = int(hex_value, 16)
                if cells[i] < 0 or cells[i] > 15:
                    raise ValueError(f"Impossible Value for cell {cells[i]}")
            except TypeError as e:
                print(f"can't convert {cells[i]}: {e}")
    return maze


def parse_maze_str(maze_str: str) -> list[list[int]]:
    """Convert hex string maze to integer grid"""
    lines = maze_str.strip().split("\n")
    try:
        res = [[int(char, 16) for char in line] for line in lines]
        return res
    except ValueError as e:
        return f"Error while parsing maze_str: {e}"


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


def reconstruct_path(
    node: tuple, came_from: dict[tuple, tuple]
) -> list[tuple]:
    """
    Return the list of nodes of the correct path from the start
    """
    path = [node]
    while node in came_from:
        node = came_from[node]
        path.append(node)
    # reverse result to get from beginning to end
    path.reverse()
    return path


def a_star_algorithm(
    maze: list[list[int]], start: tuple, end: tuple
) -> list | None:
    """
    The A* algorithm assign a cost to each cell and calculate the shortest
    path from this
    The cost of a cell is defined by
    ```math
    f(n) = g(n) + h(n)
    ```
    with
    - f(n): total cost to reach cell n -> Priority, the lower the better!
    - g(n): actual cost to reach cell n from start
    - h(n): heuristic (or estimated) cost to reach the goal from cell n
    """
    # open_paths: list[(f_score, node)] is a heap to rappidly find the
    # node with the lowest score. Faster than using a classic list
    open_paths: list[(int, tuple)] = [(h(start, end), start)]

    # register the precedent node of each newly accessed node
    came_from: dict[tuple, tuple] = {}

    # regiter the "cost" (g(n)) to each cell visited
    path_cost: dict[tuple, int] = {start: 0}

    while len(open_paths) > 0:
        # get the best next cell to visit (the one with the lowest priority)
        open_paths.sort()
        _, curr_node = open_paths.pop()
        if curr_node == end:
            goal_path = reconstruct_path(end, came_from)
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

    return None


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
        ["A", "C", "4", "6"],
        ["4", "3", "7", "0"],
        ["F", "E", "9", "2"],
    ]
    # testing if the hexa transformation works well
    print("\nTesting a decimal converter for a maze input in hexadecimal")
    print(hex_to_decimal(test_hexa))
    print("\nTesting solver for the maze: ")
    maze = [[9, 7, 11, 9, 1, 5, 3, 11, 13, 3, 11, 9, 3, 13, 3, 11, 11, 9, 5, 3], [12, 5, 0, 6, 14, 13, 4, 2, 13, 2, 10, 10, 12, 3, 10, 8, 6, 14, 11, 10], [11, 9, 6, 13, 3, 9, 3, 12, 1, 0, 6, 10, 13, 2, 8, 0, 5, 7, 10, 10], [12, 4, 1, 7, 8, 2, 12, 7, 10, 12, 5, 2, 13, 2, 14, 12, 1, 3, 8, 6], [9, 7, 10, 9, 2, 8, 7, 13, 4, 1, 3, 12, 7, 12, 5, 5, 2, 14, 8, 7], [10, 13, 4, 6, 10, 14, 11, 15, 13, 6, 10, 15, 15, 15, 11, 9, 0, 7, 8, 3], [8, 1, 3, 11, 12, 3, 10, 15, 13, 5, 0, 5, 7, 15, 8, 2, 8, 5, 6, 10], [10, 10, 8, 4, 5, 0, 2, 15, 15, 15, 10, 15, 15, 15, 10, 10, 12, 7, 9, 6], [14, 14, 10, 9, 5, 6, 12, 1, 7, 15, 10, 15, 13, 5, 2, 8, 7, 11, 8, 3], [13, 5, 6, 8, 3, 11, 13, 0, 7, 15, 14, 15, 15, 15, 10, 10, 11, 10, 10, 14], [11, 9, 5, 6, 14, 10, 13, 2, 11, 9, 3, 13, 3, 11, 10, 12, 2, 12, 2, 11], [10, 8, 1, 1, 3, 10, 11, 12, 4, 2, 14, 13, 0, 0, 4, 7, 14, 13, 4, 2], [8, 2, 14, 14, 10, 8, 4, 7, 13, 2, 9, 1, 6, 10, 11, 13, 5, 1, 7, 10], [14, 14, 9, 5, 4, 0, 3, 9, 7, 10, 14, 8, 7, 8, 4, 1, 1, 2, 11, 10], [13, 5, 6, 13, 5, 6, 14, 12, 5, 4, 7, 14, 13, 6, 13, 6, 14, 12, 6, 14]]
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

    print("Test splitlines :")
    print(str_to_decimal("ABCDEF\n132\n"))

    print("Test parse_maze_str:")
    print(parse_maze_str("ABC2344Ai\ndwkodw"))
    print(parse_maze_str("ABC2-3044A\n8"))
    print(parse_maze_str("ABC23044A\n844"))
    print(parse_maze_str("ABC230"))

    print(Border(1))
    print(Border(2))
    print(Border(4))
    print(Border(8))
    print(Border(15))


if __name__ == "__main__":
    main()
