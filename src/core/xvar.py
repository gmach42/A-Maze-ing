from mlx import Mlx
from src.core.img_data import ImgData
from src.maze.maze import Maze


class XVar:
    """Structure for main vars"""
    def __init__(self):
        self.mlx: Mlx | None = None
        self.mlx_ptr: int | None = None
        self.screen_w: int = 0
        self.screen_h: int = 0
        self.win: int | None = None
        self.maze: Maze = None
        self.img_path: ImgData = None
        self.img_background: ImgData = None
