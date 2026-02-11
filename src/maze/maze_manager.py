from mlx import Mlx

from src.core import ImgData


class MazeManager:
    def __init__(self, format_file: str, mlx: Mlx, img: ImgData):
        self.format_file: str = format_file
        self.mlx: Mlx = mlx
        self.img: ImgData = img
