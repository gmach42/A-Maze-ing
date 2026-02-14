from ..core import XVar, MLXImage
from .render_functions import draw_maze_walls, draw_42
from .color_manager import ColorManager


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
        self.regen(xvar)

    def reset_draw(self, xvar: XVar) -> None:
        temp_color: int = self.color
        self.color = ColorManager.BLACK
        draw_maze_walls(xvar)
        draw_42(xvar)
        self.color = temp_color

    def regen(self, xvar: XVar) -> None:
        draw_maze_walls(xvar)
