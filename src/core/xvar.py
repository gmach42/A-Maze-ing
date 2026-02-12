from typing import Any, TYPE_CHECKING
from mlx import Mlx

if TYPE_CHECKING:
    from ..rendering import Maze, SolutionPath


class XVar:
    """Structure for main vars"""

    def __init__(self):
        self.mlx: Mlx = None
        self.mlx_ptr: Any = None
        self.screen_w: int = 0
        self.screen_h: int = 0
        self.win: Any = None
        self.maze: "Maze | None" = None
        self.solution: "SolutionPath | None" = None
        self.animation: bool = False
        self.speed: str = "medium"
        self.row: int = 0
        self.col: int = 0
