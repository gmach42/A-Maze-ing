__authors__ = "Gildas", "Bruno"
__version__ = "0.1.0"

from .ui.border import Border
from .maze import Maze
from .maze.maze_generator import MazeGenerator
from .rendering.image import Image
from .solver.path import Path
from .solver import Solver
from .rendering.color_manager import ColorManager
from .core.xvar import XVar, setup_image_buffer, change_maze_color, change_path_color

__all__ = [
    "Border",
    "Maze",
    "MazeGenerator",
    "Image",
    "Path",
    "Solver",
    "ColorManager",
    "XVar",
    "setup_image_buffer",
    "change_maze_color",
    "change_path_color",
]
