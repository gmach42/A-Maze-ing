from .maze_generator import MazeGenerator
from .output import output_maze
from .solver_algorithm import Solver


class MazeManager:
    def __init__(self):
        self.forty_two: list[tuple[int, int]]

    def get_maze(
        self,
        height: int,
        width: int,
        perfect: bool,
        seed: str | None = None,
        algo: int | None = 1,
    ) -> list[list[int]]:
        generator: MazeGenerator = MazeGenerator(height, width, perfect, seed,
                                                 algo)
        self.forty_two = generator.forty_two_gps
        return generator.get_maze()

    def solve_maze(
        self, maze: list[list[int]], start: tuple[int, int],
        end: tuple[int, int]
    ) -> list[tuple[int, int]]:
        solver: Solver = Solver(maze, start, end, self.forty_two)
        return solver.a_star_algorithm()

    def create_output_file(
        maze_matrix: list[list[int]], sol_matrix: list[tuple[int, int]]
    ) -> None:
        output_maze(maze_matrix, sol_matrix)
