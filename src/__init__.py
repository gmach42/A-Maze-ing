__authors__ = "Gildas", "Bruno"
__version__ = "0.1.0"

from .core import XVar, MLXImage
from .mazegen import Border, MazeGenerator, Solver, output_maze
from .rendering import (
    ColorManager,
    MazeImage,
    MazeUIManager,
    SolutionPath,
    draw_maze_walls_anim,
    draw_maze_walls,
    render_frame,
    render_init,
)
from .events import manage_close, manage_key, handle_click
from .parsing import EnvVariables, parsing_config, ConfigError, errors, ExecutionError

__all__ = [
    "XVar",
    "MLXImage",
    "Border",
    "MazeGenerator",
    "Solver",
    "output_maze",
    "ColorManager",
    "ConfigError",
    "MazeImage",
    "MazeUIManager",
    "SolutionPath",
    "draw_maze_walls_anim",
    "draw_maze_walls",
    "render_frame",
    "manage_close",
    "manage_key",
    "get_key_press",
    "EnvVariables",
    "parsing_config",
    "errors",
    "ExecutionError",
    "handle_click",
    "parsing",
    "render_init",
]
