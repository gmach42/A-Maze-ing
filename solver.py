from enum import IntFlag, auto
from heapq import heappop, heappush


class Border(IntFlag):
    EMPTY = 0
    TOP = auto()  # 0001 = 1
    BOTTOM = auto()  # 0010 = 2
    LEFT = auto()  # 0100 = 4
    RIGHT = auto()  # 1000 = 8

    @property
    def corner(self) -> bool:
        """Return a corn if it's a cell with 2 walls"""
        return self in (
            self.TOP | self.LEFT,
            self.TOP | self.RIGHT,
            self.BOTTOM | self.LEFT,
            self.BOTTOM | self.RIGHT,
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
    for cell in maze:
        cell = int(cell, 16)
        if cell < 0 or cell > 15:
            raise ValueError(f"Impossible Value for cell {cell}")
    return maze


def get_neighbors(maze: list[list[int]], cell: tuple) -> list[tuple]:
    row, col = cell
    cell_walls: int = Border(maze[row][col])
    neighbors: list[tuple] = []

    # If no top wall -> there's a top neighbor (checking diff 0001)
    if not (cell_walls & Border.TOP):
        neighbors.append((row - 1, col))

    # If no bottom wall -> there's a bottom neighbor (checking diff 0010)
    if not (cell_walls & Border.BOTTOM):
        neighbors.append((row + 1, col))

    # If no left wall -> there's a left neighbor (checking diff 0100)
    if not (cell_walls & Border.LEFT):
        neighbors.append((row, col - 1))

    # If no right wall -> there's a right neighbor (checking diff 1000)
    if not (cell_walls & Border.RIGHT):
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

    def reconstruct_path(node):
        path = [node]
        while node in came_from:
            node = came_from[node]
            path.append(node)
        # reverse result to get from beginning to end
        path.reverse()
        return path

    while (len(open_paths) > 0):
        # get the best next cell to visit (the one with the lowest priority)
        _, curr_node = heappop(open_paths)
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
                heappush(open_paths, (priority, neighbor))
                came_from[neighbor] = curr_node


def main():
    maze = [
        [7, 1, 11, 13],
        [5, 8, 5, 10],
        [14, 6, 8, 13],
        [7, 3, 2, 10]
    ]
    start = (0, 0)
    end = (3, 3)
    print(a_star_algorithm(maze, start, end))


if __name__ == "__main__":
    main()
