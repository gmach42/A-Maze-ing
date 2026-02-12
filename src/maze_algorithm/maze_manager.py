from mlx import Mlx
from src.core import MLXImage


class MazeManager:
    def __init__(self, format_file: str, mlx: Mlx, img: MLXImage):
        self.format_file: str = format_file
        self.mlx: Mlx = mlx
        self.img: MLXImage = img
