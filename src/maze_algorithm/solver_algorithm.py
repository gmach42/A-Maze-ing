from .utils_algorithm import Border


class Solver:
    def __init__(
        self,
        maze: list[list[int]],
        start: tuple[int, int],
        end: tuple[int, int],
        is_42: list[tuple[int, int]],
    ):
        self.maze = maze
        self.start = start
        self.end = end
        self.is_42 = is_42
        if not self.is_valid_maze():
            raise ValueError(
                "The maze is not valid: "
                "Start and End are out of bound or in 42 obstacle"
            )

    @staticmethod
    def parse_maze_str(maze_str: str) -> list[list[int]]:
        """Convert hex string maze to integer grid"""
        lines = maze_str.strip().split("\n")
        try:
            res = [[int(char, 16) for char in line] for line in lines]
            return res
        except ValueError as e:
            return f"Error while parsing maze_str: {e}"

    def get_neighbors(self, cell: tuple) -> list[tuple]:
        row, col = cell
        cell_walls: int = Border(self.maze[row][col])
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

    @staticmethod
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
        self, node: tuple, came_from: dict[tuple, tuple]
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

    def a_star_algorithm(self) -> list[tuple[int, int]]:
        """
        The A* algorithm assign a cost to each cell and calculate the shortest
        SolutionPath from this
        The cost of a cell is defined by
        ```math
        f(n) = g(n) + h(n)
        ```
        with
        - f(n): total cost to reach cell n -> Priority, the lower the better!
        - g(n): actual cost to reach cell n from start
        - h(n): heuristic (or estimated) cost to reach the goal from cell n
        """

        # open_paths: list[(f_score, node)] is the list of cells path opened to
        # explore, sorted by priority (f_score)
        open_paths: list[(int, tuple)] = [
            (self.h(self.start, self.end), self.start)
        ]

        # Register the precedent node of each newly accessed node
        came_from: dict[tuple, tuple] = {}

        # Register the "cost" or progress already made g(n)
        # for each cell visited
        path_cost: dict[tuple, int] = {self.start: 0}

        while len(open_paths) > 0:
            # get the best next cell to visit: the one with the lowest priority
            open_paths.sort(reverse=True)
            _, curr_node = open_paths.pop()
            if curr_node == self.end:
                goal_path = self.reconstruct_path(self.end, came_from)
                return goal_path
            neighbors = self.get_neighbors(curr_node)

            # Check all possible neighbors of the current cell
            # and register new ones
            for neighbor in neighbors:
                new_cost = path_cost.get(curr_node) + 1
                if neighbor not in path_cost or new_cost < path_cost[neighbor]:
                    path_cost[neighbor] = new_cost
                    # f(n) = g(n) + h(n)
                    priority = new_cost + self.h(neighbor, self.end)
                    open_paths.append((priority, neighbor))
                    came_from[neighbor] = curr_node

        return None

    def is_valid_maze(self) -> bool:
        """Check if the maze is valid (start and end are within bounds)"""
        rows = len(self.maze)
        cols = len(self.maze[0]) if rows > 0 else 0
        start_row, start_col = self.start
        end_row, end_col = self.end

        return (
            0 <= start_row < rows
            and 0 <= start_col < cols
            and 0 <= end_row < rows
            and 0 <= end_col < cols
            and self.start not in self.is_42
            and self.end not in self.is_42
        )
