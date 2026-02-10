from enum import IntFlag
from .maze_generator import MazeGenerator


class Border(IntFlag):
    EMPTY = 0
    NORTH = 0b0001  # NORTH = 1
    EAST = 0b0010  # EAST = 2
    SOUTH = 0b0100  # SOUTH = 4
    WEST = 0b1000  # WEST = 8


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

    # TODO check if start and end are in maze

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
    print("\nTesting solver for the maze: ")
    tmaze = [[7, 1, 11, 13], [5, 8, 5, 10], [14, 6, 8, 13], [7, 3, 2, 10]]
    display_list(tmaze)

    generator = MazeGenerator(5, 5)
    array = generator.get_maze()
    maze = array.tolist()
    display_list(maze)
    print(type(maze))
    start = (0, 0)
    end = (4, 4)
    print("Maze:")
    print(f"\nstart: {start}")
    print(f"end: {end}\n")
    print("Solution:")
    solution = a_star_algorithm(maze, start, end)
    print(solution)
    if solution:
        print(cardinal_direction(solution))

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
