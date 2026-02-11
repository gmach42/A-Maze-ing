__authors__ = "Gildas", "Bruno"
__version__ = "0.1.0"

from .solver.border import Border
from .maze.maze import Maze
from .maze.maze_generator import MazeGenerator
from .maze.maze_manager import MazeManager
from .rendering.image import Image
from solver import SolutionPath
from .solver.solver import Solver
from .rendering.color_manager import ColorManager
from .core.xvar import XVar

__all__ = [
    "Border",
    "Maze",
    "MazeGenerator",
    "MazeManager",
    "Image",
    "SolutionPath",
    "Solver",
    "ColorManager",
    "XVar",
]
