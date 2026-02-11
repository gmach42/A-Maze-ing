__authors__ = "Gildas", "Bruno"
__version__ = "0.1.0"

from .core import XVar, ImgData
from .maze import Maze, MazeGenerator, MazeManager
from .solver import Border, Solver, SolutionPath
from .rendering import (
    ColorManager,
    Image,
    draw_rectangle,
    draw_maze_walls,
    render_frame,
    setup_image_buffer,
    draw_maze_walls_anim,
)
from .events import manage_key, get_key_press, manage_close

__all__ = [
    "XVar",
    "ImgData",
    "Border",
    "Maze",
    "MazeGenerator",
    "MazeManager",
    "Solver",
    "SolutionPath",
    "ColorManager",
    "Image",
    "draw_rectangle",
    "draw_maze_walls",
    "render_frame",
    "setup_image_buffer",
    "draw_maze_walls_anim",
    "manage_key",
    "get_key_press",
    "manage_close",
]
