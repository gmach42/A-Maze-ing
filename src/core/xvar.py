from typing import Any, TYPE_CHECKING
from mlx import Mlx
from ..mazegen import MazeGenerator, Solver

if TYPE_CHECKING:
    from ..rendering import MazeImage, SolutionPath, MazeUIManager


class XVar:
    """
    Main class to store all the variables used in the program. It is passed to
    all the functions and classes that need access to these variables.
    Mandatory for callback functions that cannot take additional parameters.

    Attributes:
        mlx (Mlx): The MLX instance for graphics operations
        mlx_ptr (Any): Pointer to the MLX instance
        screen_w (int): Screen width in pixels
        screen_h (int): Screen height in pixels
        win (Any): The MLX window instance
        generator (MazeGenerator): The maze generator instance
        solver (Solver): The maze solver instance
        maze (Maze): The maze instance
        solution (SolutionPath): The solution path instance
        animation (bool): Flag to indicate if animation is enabled
        speed (str): Speed of the animation ("slow", "medium", "fast")
        row (int): Current row for animation
        col (int): Current column for animation
    """

    def __init__(self) -> None:
        """
        Initialize all attributes to their default values. The actual values
        will be set later during the program setup.
        """
        self.mlx: "Mlx" = None
        self.mlx_ptr: Any = None
        self.screen_w: int = 0
        self.screen_h: int = 0
        self.win: Any = None
        self.generator: MazeGenerator
        self.solver: Solver
        self.maze: "MazeImage"
        self.solution: "SolutionPath"
        self.animation: bool = False
        self.speed: str = "medium"
        self.row: int = 0
        self.col: int = 0
        self.manager: "MazeUIManager"
        self.output: str
