from .maze_generator import MazeGenerator
from .output import output_maze
from .solver_algorithm import Solver


class MazeManager:
    """
    MazeManager class that handles the creation, solving, and output of mazes.

    Attributes:
        forty_two (list[tuple[int, int]]): List of coordinates representing 42
            obstacles in the maze, which is used by the solver to avoid these
            cells when finding the solution path.
    """

    def __init__(self) -> None:
        """Initialize the MazeManager with an empty list for 42 obstacle"""
        self.forty_two: list[tuple[int, int]] = []

    def get_maze(
        self,
        height: int,
        width: int,
        perfect: bool,
        seed: str | None = None,
        algo: int | None = 1,
    ) -> list[list[int]]:
        """Generate a maze using the MazeGenerator and store the 42 obstacle"""
        generator: MazeGenerator = MazeGenerator(height, width, perfect, seed,
                                                 algo)
        self.forty_two = generator.forty_two_gps
        return generator.get_maze()

    def solve_maze(self, maze: list[list[int]], start: tuple[int, int],
                   end: tuple[int, int]) -> list[tuple[int, int]]:
        """Solve the maze using the Solver and return the solution path"""
        solver: Solver = Solver(maze, start, end, self.forty_two)
        return solver.a_star_algorithm()

    @staticmethod
    def create_output_file(maze_matrix: list[list[int]],
                           sol_matrix: list[tuple[int, int]],
                           file_name: str) -> None:
        """Create an output file for the maze and its solution"""
        output_maze(maze_matrix, sol_matrix, file_name)

    def create_complete_maze(
        self,
        height: int,
        width: int,
        perfect: bool,
        start: tuple[int, int],
        end: tuple[int, int],
        file_name: str,
        seed: str | None = None,
        algo: int | None = 1,
    ):
        """Create a complete maze, solve it, and generate an output file"""
        maze: list[list[int]] = self.get_maze(height, width, perfect, seed,
                                              algo)
        solve: list[tuple[int, int]] = self.solve_maze(maze, start, end)
        self.create_output_file(maze, solve, file_name)
