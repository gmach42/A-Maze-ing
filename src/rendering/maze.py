from ..core import XVar, MLXImage
from .render_functions import draw_maze_walls


class Maze(MLXImage):

    def __init__(
        self,
        xvar: XVar,
        entry: tuple,
        exit: tuple,
        rows: int,
        cols: int,
        maze_matrix: list[list[int]],
        cell_size: int,
        wall_width: int,
        color: int,
    ):
        pixel_width = cols * cell_size + wall_width + 1
        pixel_height = rows * cell_size + wall_width + 1

        super().__init__(xvar, pixel_width, pixel_height)

        self.rows = rows
        self.cols = cols
        self.entry = entry
        self.exit = exit
        self.maze_matrix = maze_matrix
        self.cell_size = cell_size
        self.wall_width = wall_width
        self.color = color

    def change_color(self, new_color: int, xvar: XVar) -> None:
        self.color = new_color
        self.clear_buffer()
        self.regen(xvar)

    def change_42_color(self, new_color: int, xvar: XVar) -> None:
        self.color = new_color
        self.clear_buffer()
        self.regen(xvar)

    def regen(self, xvar: XVar) -> None:
        self.clear_buffer()
        draw_maze_walls(xvar)
