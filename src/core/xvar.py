from typing import Any
from mlx import Mlx
from src.maze import Maze
from src.solver import SolutionPath
from .img_data import ImgData


class XVar:
    """Structure for main vars"""

    def __init__(self):
        self.mlx: Mlx | None = None
        self.mlx_ptr: Any = None
        self.screen_w: int = 0
        self.screen_h: int = 0
        self.win: Any = None
        self.img: ImgData = None
        self.cell_size: int = 50
        self.maze: Maze = None
        self.col: int = 0
        self.row: int = 0
        self.maze_width: int = 0
        self.maze_height: int = 0
        self.animation: bool = False
        self.speed: str = "medium"
        self.solution: SolutionPath = None

    def set_img(self, img: ImgData):
        self.img = img
