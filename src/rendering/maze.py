from ..core import XVar, MLXImage
from .render_functions import draw_maze_walls, draw_42
from .color_manager import ColorManager


class Maze(MLXImage):
    """
    Class to represent the maze, inheriting from MLXImage.

    Attributes:
        rows (int): Number of rows in the maze
        cols (int): Number of columns in the maze
        entry (tuple[int, int]): Coordinates of the maze entry point
        exit (tuple[int, int]): Coordinates of the maze exit point
        maze_matrix (list[list[int]]): 2D list representing the maze structure
        cell_size (int): Size of each cell in pixels
        wall_width (int): Width of the walls in pixels
        color (int): Color used to draw the maze walls
    """

    def __init__(
        self,
        xvar: XVar,
        entry: tuple[int, int],
        exit: tuple[int, int],
        rows: int,
        cols: int,
        maze_matrix: list[list[int]],
        cell_size: int,
        wall_width: int,
        color: int,
    ):
        """
        Initialize the Maze with the given parameters and create the image
        buffer.

        Args:
            xvar (XVar): The main variable containing all necessary data
            entry (tuple[int, int]): Coordinates of the maze entry point
            exit (tuple[int, int]): Coordinates of the maze exit point
            rows (int): Number of rows in the maze
            cols (int): Number of columns in the maze
            maze_matrix (list[list[int]]): 2D list representing the maze
                structure
            cell_size (int): Size of each cell in pixels
            wall_width (int): Width of the walls in pixels
            color (int): Color used to draw the maze walls
        """
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
        """Change maze wall color and redraw the maze."""
        self.color = new_color
        self.regen(xvar)

    def reset_draw(self, xvar: XVar) -> None:
        """Reset maze by redrawing it in Black color."""
        temp_color: int = self.color
        self.color = ColorManager.BLACK
        draw_maze_walls(xvar)
        draw_42(xvar)
        self.color = temp_color

    def regen(self, xvar: XVar) -> None:
        draw_maze_walls(xvar)
