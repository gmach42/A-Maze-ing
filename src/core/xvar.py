from typing import Any, TYPE_CHECKING
from mlx import Mlx
from ..maze_algorithm import MazeGenerator, Solver

if TYPE_CHECKING:
    from ..rendering import Maze, SolutionPath, MazeUIManager


class XVar:
    """Structure for main vars"""

    def __init__(self) -> None:
        self.mlx: "Mlx" = None
        self.mlx_ptr: Any = None
        self.screen_w: int = 0
        self.screen_h: int = 0
        self.win: Any = None
        self.generator: MazeGenerator
        self.solver: Solver
        self.maze: "Maze"
        self.solution: "SolutionPath"
        self.animation: bool = False
        self.speed: str = "medium"
        self.row: int = 0
        self.col: int = 0
        self.manager: "MazeUIManager"
