# from .maze_generator import MazeGenerator
from mlx import Mlx
from .window import ImgData


class MazeManager():
    def __init__(self, format_file: str, mlx: Mlx, img: ImgData):
        self.format_file: str = format_file
        self.mlx: Mlx = mlx
        self.img: ImgData = img
