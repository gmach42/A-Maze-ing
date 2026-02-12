__authors__ = "Gildas", "Bruno"
__version__ = "0.1.0"

from .core import XVar, MLXImage
from .maze_algorithm import Border, MazeManager, MazeGenerator, Solver
from .rendering import (
    Background,
    ColorManager,
    Maze,
    MazeUIManager,
    SolutionPath,
    draw_maze_walls_anim,
    draw_maze_walls,
    render_frame,
)
from .events import manage_close, manage_key, get_key_press
from .parsing import EnvVariables, parsing, errors


__all__ = [
    "XVar",
    "MLXImage",
    "Border",
    "MazeManager",
    "MazeGenerator",
    "Solver",
    "Background",
    "ColorManager",
    "Maze",
    "MazeUIManager",
    "SolutionPath",
    "draw_maze_walls_anim",
    "draw_maze_walls",
    "render_frame",
    "manage_close",
    "manage_key",
    "get_key_press",
    "EnvVariables",
    "parsing",
    "errors",
]
