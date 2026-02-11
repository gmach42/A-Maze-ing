from src.core import ImgData
from src.rendering import draw_maze_walls


class Maze:
    def __init__(
        self,
        img_maze: ImgData,
        rows: int,
        cols: int,
        maze_matrix: list[list[int]],
        cell_size: int,
        wall_width: int,
        color: int,
    ):
        self.img_maze = img_maze
        self.rows = rows
        self.cols = cols
        self.maze_matrix = maze_matrix
        self.cell_size = cell_size
        self.wall_width = wall_width
        self.color = color

    def change_color(self, color: int) -> None:
        self.color = color
        # Clear image buffer
        self.img_maze.clear_buffer()
        self.regen_maze()

    def change_dimensions(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols

    def regen_maze(self) -> None:
        self.img_maze.clear_buffer()
        draw_maze_walls(self.img_maze, self.maze_matrix, self.cell_size,
                        self.wall_width, self.color)
