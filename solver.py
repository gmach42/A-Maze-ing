from enum import IntFlag, auto
from heapq import heappop, heappush


class Border(IntFlag):
    EMPTY = 0
    TOP = auto()
    BOTTOM = auto()
    LEFT = auto()
    RIGHT = auto()

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


def find_path(
    g: dict, start_node: tuple[int, int], goal_node: tuple[int, int]
) -> list | None:
    open_set = [(0, start_node)]
    came_from = {}
    cost_so_far = {start_node: 0}

    def heuristic(node: tuple[int, int], goal: tuple[int, int]):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def rebuild_path(n):
        p = [n]
        while n in came_from:
            n = came_from[n]
            p.append(n)
        return p

    while len(open_set) > 0:
        curr_cost, curr_node = heappop(open_set)
        if curr_node == goal_node:
            goal_path = rebuild_path(goal_node)
            return goal_path

        for neighbor in g[curr_node]:
            new_cost = cost_so_far.get(curr_node) + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal_node)
                heappush(open_set, (priority, neighbor))
                came_from[neighbor] = curr_node

    return None


def h(cell1: tuple[int, int], cell2: tuple[int, int]):
    """
    Heuristic function chosen here is the manhattan distance
    Calculate the distance between 2 points on a grid by summing the
    absolute differences in their x and y coordinates
    """
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)


def find_path(maze: dict, start: tuple, end: tuple) -> list | None:
    """
    A heap queue (also called a priority queue) is a special data structure
    that allows quick access to the smallest (min-heap) or largest (max-heap) element
    the A* algorithm assign a cost to each cell and calculate the shortest path from this
    the cost of a cell is defined by
    ```math
    f(n) = g(n) + h(n)
    ```
    with
    - f(n): total cost to reach cell n
    - g(n): actual cost to reach cell n from start
    - h(n): heuristic (or estimated) cost to reach the goal from cell n
    """
    # open_paths: list[(g_score, f_score, node)]
    open_paths: list[(int, int, tuple)] = [(0, h(start, end), start)]
    came_from = {}
    cost_so_far = 0

    while(open_paths):
        curr_node = heappop(open_paths)












    while (len(open_paths) > 0):
        curr_cost, curr_node = heappop(open_paths)
        if curr_node == end:
            return reconstruct_path(came_from, curr_node)




